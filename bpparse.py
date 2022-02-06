import time
from datetime import datetime
import logging
import os

logger = logging.getLogger(__name__)


class BPSong:
    """
    Represents an entry in a .bpstat file.

    All fields are present in order in a .bpstat file and are required.
    For internal purposes, note that `filepath` should be unique across all BPSong objects.
    """

    def __init__(self, plays, plays_this_month, title, artist, album, filepath, addition_date, last_played):
        self.total_plays = int(plays)
        self.plays_this_month = int(plays_this_month)
        self.title = title
        self.artist = artist
        self.album = album
        self.filepath = filepath
        self.addition_date = datetime.utcfromtimestamp(int(addition_date) / 1000)
        self.last_played = datetime.utcfromtimestamp(int(last_played) / 1000)

    @classmethod
    def from_song(cls, song):
        """Initialize BPSong from a libpytunes Song object."""
        total_plays = song.play_count if song.play_count else 0
        title = song.name
        artist = song.artist
        album = song.album
        filepath = song.persistent_id + ".mp3"  # This is assumed
        addition_date = time.mktime(song.date_added) * 1000  # Make conversion back into milliseconds
        last_played = time.mktime(song.lastplayed) * 1000 if song.lastplayed else 1000000000  # Random time in 1970 supported by OS

        # No way to determine plays this month from XML data
        return cls(total_plays, 0, title, artist, album, filepath, addition_date, last_played)

    def as_bpstat_line(self, prefix_path):
        """Write as bpstat line with specified prepended filepath."""
        # Convert back to timestamp in milliseconds
        addition_date = int(datetime.timestamp(self.addition_date) * 1000)
        last_played = 0

        # Support for songs that have never been played before to be exported to bpstat
        if self.total_plays == 0:
            last_played = addition_date
        else:
            last_played = int(datetime.timestamp(self.last_played) * 1000)

        path = os.path.join(prefix_path, self.filepath)

        return f"{self.total_plays};{self.plays_this_month};{self.title};{self.artist};" \
               f"{self.album};{path};{addition_date};{last_played}"


def get_songs(filepath):
    """
    Parse a .bpstat file, returning an array of BPSong objects.

    :param filepath: The filepath of the .bpstat file.
    :return: An array containing a list of BPSong objects.
    """
    with open(filepath, 'rb') as file:
        contents = file.read().decode('utf-8')
    lines = contents.split("\n")

    # If there are the wrong number of fields/semicolons in a bpstat thing, it will not import correctly
    # This also holds true in BlackPlayer itself; it can export a song with semicolons in its metadata,
    # but will importing it because there are too many fields
    songs = []
    for entry in lines:
        fields = entry.split(";")
        if len(fields) > 8:
            logger.error(
                f"Tried to import a song with an extra semicolon in its metadata - please remove it ({entry=})")
            continue
        elif len(fields) < 8:
            # shouldn't ever happen unless the bpstat's been messed with, or an empty line was parsed
            logging.error(f"Song has less than 8 fields?! ({entry=})")
            continue
        song = BPSong(*fields)
        songs.append(song)

    return songs
