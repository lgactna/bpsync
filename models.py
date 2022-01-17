"""
Information that needs to be present:
- Persistent ID (PK)
- Last (synchronized) playcount recorded

in the future, if it's ever necessary to make this more robust:
- store a program-level ID in a custom ID3 tag
- add more fields that can try to identify a song if a persistent ID is busted
"""

import logging

from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import create_engine

from sqlalchemy.orm import declarative_base, Session

logger = logging.getLogger(__name__)

# setup/config
# TODO: un-hardcode the database location
engine = create_engine("sqlite+pysqlite:///data\\songs.db", echo=True, future=True)
Base = declarative_base()


class StoredSong(Base):
    __tablename__ = 'songs'

    id = Column(String(20), primary_key=True)
    last_playcount = Column(Integer, nullable=False)

    def __repr__(self):
        return f"{self.id=} {self.last_playcount=}"

    def get_delta(self, xml_pc, bpstat_pc):
        xml_diff = xml_pc-self.last_playcount  # New plays on XML side
        bpstat_diff = bpstat_pc-self.last_playcount  # New plays on BP side
        delta = xml_diff + bpstat_diff

        if delta < 0:
            logger.error(f"Playcount for {id=} has gone down? {self.last_playcount=} {xml_pc=} {bpstat_pc=}")

        return delta

    def update_playcount(self, xml_pc, bpstat_pc):
        delta = self.get_delta(xml_pc, bpstat_pc)
        self.last_playcount += delta


def create_db():
    """Create a new database from an array of libpytunes Song objects."""
    Base.metadata.create_all(engine)

def add_libpy_songs(songs):
    """Commit an array of libpytunes Song objects to the database."""
    # If playcount field isn't present, it's implied to be 0
    new_songs = [StoredSong(id=song.persistent_id, 
                            last_playcount=song.play_count if song.play_count else 0)
                 for song in songs]
    with Session(engine) as session:
        session.bulk_save_objects(new_songs)
        session.commit()

def commit_changes():
    """Commit changes to database."""
    with Session(engine) as session:
        session.commit()
