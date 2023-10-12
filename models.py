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
import hashlib
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

    def update_from_libpy_song(self, libpysong):
        """
        Update a StoredSong to reflect the contents of a libpytunes Song object.

        :param self: A StoredSong() instance.
        :param libpysong: A libpytunes Song object with the data to copy over.
        """
        self.persistent_id = libpysong.persistent_id
        
        self.last_playcount = libpysong.play_count if libpysong.play_count else 0

        self.blake2b_hash = calculate_file_hash(libpysong.location)

        # The rest are all nullable, so None is ok to assign
        # It's also valid to be comparing null/None, since a change
        # from None to any value indicates that a value was
        # added that wasn't present before
        self.start_time = libpysong.start_time
        self.stop_time = libpysong.stop_time
        self.disc_number = libpysong.disc_number
        self.disc_count = libpysong.disc_count
        self.track_number = libpysong.track_number
        self.track_count = libpysong.track_count
        self.year = libpysong.year
        self.bit_rate = libpysong.bit_rate
        self.sample_rate = libpysong.sample_rate
        self.volume_adjustment = libpysong.volume_adjustment
        self.compilation = libpysong.compilation
        self.track_type = libpysong.track_type
        self.name = libpysong.name
        self.artist = libpysong.artist
        self.album_artist = libpysong.album_artist
        self.composer = libpysong.composer
        self.album = libpysong.album
        self.grouping = libpysong.grouping
        self.genre = libpysong.genre
        self.kind = libpysong.kind
        self.equalizer = libpysong.equalizer
        self.sort_album = libpysong.sort_album
        self.work = libpysong.work
        self.movement_name = libpysong.movement_name
        self.movement_number = libpysong.movement_number
        self.movement_count = libpysong.movement_count

    def needs_reprocessing(self, libpysong, calculate_file_hash=False):
        """
        Takes in a libpysong and checks if the relevant fields are equal.
        
        These fields indicate a change in a tag that needs to be reflected in BlackPlayer,
        and therefore the song should be reprocessed.
        """
        # although not exactly pretty, maybe there's a better way
        # the fields that require a reprocess are unlikely to ever change
        # (i.e., track number will not suddenly stop being an ID3 tag)

        fields_to_test = ["start_time", "stop_time", "disc_number", "disc_count",
                          "track_number", "year", "bit_rate", "sample_rate",
                          "volume_adjustment", "compilation", "track_type",
                          "name", "artist", "album_artist", "composer",
                          "album", "grouping", "genre", "kind",
                          "sort_album", "work", "movement_name",
                          "movement_number", "movement_count"]

        for field_name in fields_to_test:
            if getattr(self, field_name) != getattr(libpysong, field_name):
                logger.info(f"{self.name} ({self.persistent_id}) needs reprocessing because {field_name} is different")
                return True
        
        # Only try checking for file hash if explicitly requested
        if calculate_file_hash and self.blake2b_hash != calculate_file_hash(libpysong.location):
            logger.info(f"{self.name} ({self.persistent_id}) needs reprocessing because the hash has changed")
            return True
        
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

    logger.info(f"Adding {len(songs)} to database...")

    new_songs = []
    for song in songs:
        logger.info(f"Creating StoredSong object for {song.persistent_id=}...")
        new_song = StoredSong()

        new_song.update_from_libpy_song(song)

        new_songs.append(new_song)

    with Session() as session:
        logger.info("Saving new database elements...")
        session.bulk_save_objects(new_songs)
        session.commit()

    logger.info("New songs committed.")

def add_ignored_ids(song_ids):
    """
    Commit an array of persistent IDs to be excluded from the
    "new songs" table in a standard sync.
    """
    ignored_song_ids = [IgnoredSong(persistent_id=song_id)
                 for song_id in song_ids]

    with Session() as session:
        logger.info(f"Saving IgnoredSong objects...")
        session.bulk_save_objects(ignored_song_ids)
        session.commit()

def commit_changes():
    """Commit changes to database."""
    with Session() as session:
        session.commit()

def calculate_file_hash(filepath) -> str:
    # https://stackoverflow.com/questions/16874598/how-do-i-calculate-the-md5-checksum-of-a-file-in-python

    try:
        with open(filepath, "rb") as f:
            file_hash = hashlib.blake2b()
            while chunk := f.read(8192):
                file_hash.update(chunk)
    except FileNotFoundError:
        # Return a placeholder hash.
        # If the file doesn't exist for some reason, but the user
        # still explicitly requested to track it, then we can
        # just put a placeholder hash here instead.
        return "FILE_NOT_AVAILABLE"

    return file_hash.hexdigest() # len = 128