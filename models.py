"""
Information that needs to be present:
- Persistent ID (PK)
- Last (synchronized) playcount recorded

in the future, if it's ever necessary to make this more robust:
- store a program-level ID in a custom ID3 tag
- add more fields that can try to identify a song if a persistent ID is busted
"""

import logging
import os
from pathlib import Path

from sqlalchemy import Table, Column, Integer, String, Boolean, Text
from sqlalchemy import create_engine

from sqlalchemy.orm import declarative_base, sessionmaker

logger = logging.getLogger(__name__)

# setup/config
# https://stackoverflow.com/questions/63368099/a-proper-place-for-sql-alchemys-engine-global
# https://docs.sqlalchemy.org/en/13/orm/session_basics.html#session-frequently-asked-questions
engine = None
Session = None
Base = declarative_base()

class StoredSong(Base):
    """Main class representing a tracked song"""
    __tablename__ = 'songs'

    persistent_id = Column(String(20), primary_key=True)
    last_playcount = Column(Integer, nullable=False)

    # hex digest representation (not pure bytes)
    blake2b_hash = Column(String(128))

    # Below are definitions of all libpytunes Song fields that would require a reprocess
    # Fields are nullable by default, i.e. nullable=True so these fields can be empty unless specified otherwise
    # Arbitrary-length text fields should use type Text, not the fixed-width field String (which is usually a VARCHAR)
    # Many of these *should* never change but it's better to assume they can
    #
    # These fields should only be updated if the song is actually reprocessed. In other words,
    # they reflect the ID3 tags of the most recently generated .mp3 of a given song.
    start_time = Column(Integer)
    stop_time = Column(Integer)
    disc_number = Column(Integer)
    disc_count = Column(Integer)
    track_number = Column(Integer)
    track_count = Column(Integer)
    year = Column(Integer)
    bit_rate = Column(Integer)
    sample_rate = Column(Integer)
    volume_adjustment = Column(Integer)
    compilation = Column(Boolean) # reason: a change to True indicates more than one artist in the album, so the album artist probably needs to be changed
    track_type = Column(Text)
    name = Column(Text)
    artist = Column(Text)
    album_artist = Column(Text)
    composer = Column(Text)
    album = Column(Text)
    grouping = Column(Text)
    genre = Column(Text)
    kind = Column(Text)
    equalizer = Column(Text)  # not supported but still tracked if a solution is found later on
    sort_album = Column(Text)
    work = Column(Text)
    movement_name = Column(Text)
    movement_number = Column(Integer)
    movement_count = Column(Integer)

    def __repr__(self):
        return f"{self.persistent_id=} {self.last_playcount=}"

    def get_delta(self, xml_pc, bpstat_pc):
        xml_diff = xml_pc-self.last_playcount  # New plays on XML side
        bpstat_diff = bpstat_pc-self.last_playcount  # New plays on BP side
        delta = xml_diff + bpstat_diff

        if delta < 0:
            logger.error(f"Playcount for self.{self.persistent_id=} has gone down? {self.last_playcount=} {xml_pc=} {bpstat_pc=}")

        return delta

    def update_playcount(self, xml_pc, bpstat_pc):
        delta = self.get_delta(xml_pc, bpstat_pc)
        self.last_playcount += delta

    def needs_reprocessing(self, libpysong):
        """
        Takes in a libpysong and checks if the relevant fields are equal.
        
        These fields indicate a change in a tag that needs to be reflected in BlackPlayer,
        and therefore the song should be reprocessed.
        """
        # python's `or` short-circuits so this *should* be efficient?
        # although not exactly pretty, maybe there's a better way
        # the fields that require a reprocess are unlikely to ever change
        # (i.e., track number will not suddenly stop being an ID3 tag)
        if self.start_time != libpysong.start_time \
        or self.stop_time != libpysong.stop_time \
        or self.disc_number != libpysong.disc_number \
        or self.disc_count != libpysong.disc_count \
        or self.track_number != libpysong.track_number \
        or self.track_count != libpysong.track_count \
        or self.year != libpysong.year \
        or self.bit_rate != libpysong.bit_rate \
        or self.sample_rate != libpysong.sample_rate \
        or self.volume_adjustment != libpysong.volume_adjustment \
        or self.compilation != libpysong.compilation \
        or self.track_type != libpysong.track_type \
        or self.name != libpysong.name \
        or self.artist != libpysong.artist \
        or self.album_artist != libpysong.album_artist \
        or self.composer != libpysong.composer \
        or self.album != libpysong.album \
        or self.grouping != libpysong.grouping \
        or self.genre != libpysong.genre \
        or self.kind != libpysong.kind \
        or self.sort_album != libpysong.sort_album \
        or self.work != libpysong.work \
        or self.movement_name != libpysong.movement_name \
        or self.movement_number != libpysong.movement_number \
        or self.movement_count != libpysong.movement_count \
        or self.blake2b_hash != calculate_file_hash(libpysong.location):
            return True
        else:
            return False

        # Not supported
        # or self.equalizer != libpysong.equalizer \

class IgnoredSong(Base):
    """
    Class used for self.storing songs unselected for self.tracking.
    
    Really, this is just an array holding persistent IDs of songs that weren't tracked
    for a given sync.
    """
    __tablename__ = 'ignoredsongs'

    persistent_id = Column(String(20), primary_key=True)

def initialize_engine(filepath):
    """
    Initialize the engine to the specified path, where songs.db is the default filename.
    
    This *must* be called before performing any database actions.

    Also initializes a sessionmaker."""
    global engine, Session

    # if we were given a file instead of a directory, then use that full filepath
    # but if we were just given a directory, then create an engine with songs.db.
    # This also implicitly makes the database file if it does not already exist.

    if os.path.isfile(filepath):
        #engine = create_engine(f"sqlite+pysqlite:///{filepath}", echo=True, future=True)
        engine = create_engine(f"sqlite+pysqlite:///{filepath}", future=True)
    else:
        output_path = os.path.join(filepath, "songs.db")
        #engine = create_engine(f"sqlite+pysqlite:///{output_path}", echo=True, future=True)
        engine = create_engine(f"sqlite+pysqlite:///{output_path}", future=True)
    Session = sessionmaker(engine)

def create_db():
    """
    Create a new database from an array of libpytunes Song objects.
    
    Should only be used on first-time sync, where the database does not already exist.
    """
    Base.metadata.create_all(engine)

def add_libpy_songs(songs):
    """Commit an array of libpytunes Song objects to the database."""
    # If playcount field isn't present, it's implied to be 0
    new_songs = []
    for song in songs:
        new_song = StoredSong()

        new_song.persistent_id = song.persistent_id
        new_song.last_playcount = song.play_count if song.play_count else 0

        new_song.blake2b_hash = calculate_file_hash(song.location)

        # The rest are all nullable, so None is ok to assign
        # It's also valid to be comparing null/None, since a change
        # from None to any value indicates that a value was
        # added that wasn't present before
        new_song.start_time = song.start_time
        new_song.stop_time = song.stop_time
        new_song.disc_number = song.disc_number
        new_song.disc_count = song.disc_count
        new_song.track_number = song.track_number
        new_song.track_count = song.track_count
        new_song.year = song.year
        new_song.bit_rate = song.bit_rate
        new_song.sample_rate = song.sample_rate
        new_song.volume_adjustment = song.volume_adjustment
        new_song.compilation = song.compilation
        new_song.track_type = song.track_type
        new_song.name = song.name
        new_song.artist = song.artist
        new_song.album_artist = song.album_artist
        new_song.composer = song.composer
        new_song.album = song.album
        new_song.grouping = song.grouping
        new_song.genre = song.genre
        new_song.kind = song.kind
        new_song.equalizer = song.equalizer
        new_song.sort_album = song.sort_album
        new_song.work = song.work
        new_song.movement_name = song.movement_name
        new_song.movement_number = song.movement_number
        new_song.movement_count = song.movement_count

        new_songs.append(new_song)

    with Session() as session:
        session.bulk_save_objects(new_songs)
        session.commit()

def add_ignored_ids(song_ids):
    """
    Commit an array of persistent IDs to be excluded from the
    "new songs" table in a standard sync.
    """
    ignored_song_ids = [IgnoredSong(persistent_id=song_id)
                 for song_id in song_ids]

    with Session() as session:
        session.bulk_save_objects(ignored_song_ids)
        session.commit()

def commit_changes():
    """Commit changes to database."""
    with Session() as session:
        session.commit()

def calculate_file_hash(filepath) -> str:
    # https://stackoverflow.com/questions/16874598/how-do-i-calculate-the-md5-checksum-of-a-file-in-python
    with open(filepath, "rb") as f:
        file_hash = hashlib.blake2b()
        while chunk := f.read(8192):
            file_hash.update(chunk)

    return file_hash.hexdigest() # len = 128