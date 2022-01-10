import logging
import os
from shutil import copy2

import bpparse
from libpytunes import Library
from pydub import AudioSegment
from pydub.utils import mediainfo
import eyed3

logger = logging.getLogger(__name__)

# dev constants

LIBRARY = 'iTunes_Music_Library.xml'
DATA_FOLDER = 'data'

sample = 'D:/Music/Music/Compilations/(J)Rock_Pop/01 Kagerou Daze.mp3'

if __name__ == "__main__":
    lib = Library('iTunes_Music_Library.xml')

    # first time (bpstat doesn't exist yet)? Iterate over Library.songs
    # Figure out if there are any songs that need to be cut or edited due to semicolon or time fields
    # TODO: Checks/process to ensure ID3 data (which BP uses) == XML data (which can be changed user-side)
    from pprint import pprint
    pprint(lib.songs.items())

    for track_id, song in lib.songs.items():
        # Strip semicolon character in relevant XML fields
        # Also needs to be done on id3 data (only) in the future
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

    # Create database with new songs

    # Also create an independent set of paths with the new filepaths and unnecessary fields stripped out

    # Create provisional bpstat using libpytunes (Library.songs)

    # And then throw the info into the database

    #---------
    # bpstat already exists? Get both the XML and the bpstat file

    # Call the resolver, which works with the database to figure out what's changed

    #---------
    # Recovering from a bpstat? Get the bpstat file

    # Put the bpstat songs into unified format, using defaults where necessary

    # Make sure the user has all the music from their phone on disk

    # Create provisional XML using libpytunes

    # Write to database and tidy up