import logging
import os
from datetime import datetime

from libpytunes import Library
from pydub import AudioSegment
from pydub.utils import mediainfo
import eyed3

import bpparse
import models
import bpsynctools

logger = logging.getLogger(__name__)

# dev constants

LIBRARY = 'iTunes_Music_Library.xml'
DATA_FOLDER = 'data'
SONGS_FOLDER = 'tmp'

TARGET_FOLDER = '/storage/sdcard1/imported-music/'

# TODO: Separate functions for each part of the process
#       - Calculating accessible files by filepath, removing inaccessible Song objects
#       - Calculating files that need to be trimmed
#       - Strip ID3 of semicolons
#       - Create db
#       - Calculate deltas

if __name__ == "__main__":
    lib = Library('iTunes_Music_Library.xml')
    # TODO: dict with key:value of persistent id:Song
    
    # bpstat generation and processing can happen at the same time
    for _, song in lib.songs.items():
        #bpsynctools.copy_and_process_song(song)

        bpstat_name = datetime.now().strftime("%Y-%m-%d %H-%M-%S (new).bpstat")
        bpstat_path = os.path.join(DATA_FOLDER, bpstat_name)

        bpsynctools.add_to_bpstat(song, TARGET_FOLDER, bpstat_path)

    # Create database with new songs
    song_arr = [song for _, song in lib.songs.items()]
    models.create_db(song_arr)

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