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
engine = create_engine("sqlite+pysqlite:///songs.db", echo=True, future=True)
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
    Base.metadata.create_all(engine)


def add_songs(songs):
    """Commit an array of StoredSongs to the database."""
    with Session(engine) as session:
        session.bulk_insert_mappings(StoredSong, songs)
        session.commit()


def commit_changes():
    with Session(engine) as session:
        session.commit()
