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

from sqlalchemy import Table, Column, Integer, String
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
    __tablename__ = 'songs'

    persistent_id = Column(String(20), primary_key=True)
    last_playcount = Column(Integer, nullable=False)

    def __repr__(self):
        return f"{self.persistent_id=} {self.last_playcount=}"

    def get_delta(self, xml_pc, bpstat_pc):
        xml_diff = xml_pc-self.last_playcount  # New plays on XML side
        bpstat_diff = bpstat_pc-self.last_playcount  # New plays on BP side
        delta = xml_diff + bpstat_diff

        if delta < 0:
            logger.error(f"Playcount for {persistent_id=} has gone down? {self.last_playcount=} {xml_pc=} {bpstat_pc=}")

        return delta

    def update_playcount(self, xml_pc, bpstat_pc):
        delta = self.get_delta(xml_pc, bpstat_pc)
        self.last_playcount += delta

def initialize_engine(filepath):
    """
    Initialize the engine to the specified path, where songs.db is the default filename.
    
    This *must* be called before performing any database actions.

    Also initializes a sessionmaker."""
    global engine, Session

    filename = Path(filepath).stem
    if filename:
        engine = create_engine(f"sqlite+pysqlite:///{filepath}", echo=True, future=True)
    else:
        output_path = os.path.join(filepath, "songs.db")
        engine = create_engine(f"sqlite+pysqlite:///{output_path}", echo=True, future=True)
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
    new_songs = [StoredSong(id=song.persistent_id, 
                            last_playcount=song.play_count if song.play_count else 0)
                 for song in songs]
    with Session() as session:
        session.bulk_save_objects(new_songs)
        session.commit()

def commit_changes():
    """Commit changes to database."""
    with Session() as session:
        session.commit()
