import logging
import os
from shutil import copy2
from datetime import datetime

from libpytunes import Library
from pydub import AudioSegment
from pydub.utils import mediainfo
import eyed3

import bpparse
import models

logger = logging.getLogger(__name__)

# dev constants

LIBRARY = 'iTunes_Music_Library.xml'
DATA_FOLDER = 'data'
SONGS_FOLDER = 'tmp'


def preprocess(lib):
    for track_id, song in lib.songs.items():
        # Strip semicolon character in relevant XML fields
        # Also needs to be done on id3 tmp (only) in the future
        for field in [song.name, song.artist, song.album, song.location]:
            # Some videos and files might not have this metadata
            if field is None:
                continue
            if ";" in field:
                field.replace(";", "")
                logger.info(f"Had to remove semicolon from {field=}, {song.track_id=}")

    # Copy songs over to a specified location as MP3 (preparing them to be moved to a phone), cutting if necessary
    # If stop/start time specified, then trim

        _, file_extension = os.path.splitext(song.location)
        output_path = os.path.join(DATA_FOLDER, song.persistent_id + ".mp3")
        try:
            # Only use pydub if necessary
            if file_extension != ".mp3" or song.start_time or song.stop_time:
                obj = AudioSegment.from_file(song.location)

                if song.start_time or song.stop_time:
                    start_time = 0 if not song.start_time else song.start_time
                    stop_time = len(obj) if not song.stop_time else song.stop_time

                    obj = obj[start_time:stop_time]

                    print(f"Trimmed {song.persistent_id} ({output_path})")

                # tags parameter is used for retaining metadata
                obj.export(output_path, format="mp3", tags=mediainfo(song.location)['TAG'])

            else:
                copy2(song.location, output_path)
        except FileNotFoundError as e:
            logging.error(f"Couldn't find {song.location}")


def make_db(lib):
    models.create_db()
    new_songs = [models.StoredSong(id=song.persistent_id, last_playcount=song.play_count)
                 for _, song in lib.songs.items()]
    models.commit_changes()


if __name__ == "__main__":
    lib = Library('iTunes_Music_Library.xml')
    # TODO: dict with key:value of persistent id:Song

    # first time (bpstat doesn't exist yet)? Iterate over Library.songs
    # Figure out if there are any songs that need to be cut or edited due to semicolon or time fields
    # TODO: Checks/process to ensure ID3 tmp (which BP uses) has no semicolons (and == XML tmp)
    # preprocess(lib)

    # Create database with new songs
    # make_db(lib)

    # Create provisional bpstat
    # For future syncs this should be a function dependent on libpytunes Song objects that have already been updated
    output = ""
    for _, song in lib.songs.items():
        bpsong = bpparse.BPSong.from_song(song)
        if bpsong.total_plays == 0:
            continue

        output += bpsong.as_bpstat_line() + "\n"

    bpstat_name = datetime.now().strftime("%Y-%m-%d %H-%M-%S (new).bpstat")
    bpstat_path = os.path.join(DATA_FOLDER, bpstat_name)
    with open(bpstat_path, "wb") as fp:
        fp.write(output.encode('utf-8'))

    #---------
    # bpstat already exists? Get both the XML and the bpstat file

    # Call the resolver, which works with the database to figure out what's changed

    # Then rerun everything with the new changes

    #---------
    # Recovering from a bpstat? Get the bpstat file (maybe just a extra one-way recovery thing)

    # Put the bpstat songs into unified format, using defaults where necessary

    # Make sure the user has all the music from their phone on disk

    # Create provisional XML using libpytunes

    # Write to database and tidy up