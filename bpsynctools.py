"""
Various convenience functions
"""

import os
from shutil import copy2
from datetime import datetime
from math import log10
import logging

from pydub import AudioSegment
from pydub.utils import mediainfo
from eyed3 import load

import bpparse

logger = logging.getLogger(__name__)

def copy_and_process_song(song, output_folder='tmp'):
    """
    Copy and rename the song to its persistent ID, doing extra processing if necessary.
    
    :param song: The libpytunes Song object to use for processing.
    :param output_folder: The folder to output the copied/processed song to. `/tmp` by default.

    This function works with libpytunes Song objects. It will copy the song from the Song.location
    attribute, renaming it to its persistent ID and placing it in a flat folder. By default,
    this output folder is `/tmp` relative to the run location.

    If the Song object is not an mp3 file or has been trimmed, the song is processed using
    pydub and requires ffmpeg/libav.
    """
    _, file_extension = os.path.splitext(song.location)
    output_path = os.path.join(output_folder, song.persistent_id + ".mp3")

    try:
        if file_extension != ".mp3" or song.start_time or song.stop_time or song.volume_adjustment:
            obj = AudioSegment.from_file(song.location)

            if song.start_time or song.stop_time:
                start_time = 0 if not song.start_time else song.start_time
                stop_time = len(obj) if not song.stop_time else song.stop_time

                obj = obj[start_time:stop_time]

                logging.info(f"Trimmed {song.persistent_id} ({output_path})")
            
            if song.volume_adjustment:
                # internally stored as an integer between -255 and 255
                # but can physically be adjusted past 255
                if song.volume_adjustment <= -255:
                    obj = obj - 100  # essentially silent
                    logging.warning(f"The song {song.name} has a volume adjustment value less than -255 and is silent!")
                else:
                    gain_factor = (song.volume_adjustment + 255)/255
                    decibel_change = 10 * log10(gain_factor)
                    obj = obj + decibel_change
                    logging.info(f"Changed {song.name} gain factor by {gain_factor} ({decibel_change} dB)")

            # tags parameter is used for retaining metadata
            obj.export(output_path, format="mp3", tags=mediainfo(song.location)['TAG'])
        else:
            copy2(song.location, output_path)
    except FileNotFoundError as e:
        logging.error(f"Couldn't find {song.location}")
    
    if check_for_semicolons(song):
        strip_semicolons(output_path)    

def strip_semicolons(song_path):
    """
    Replace semicolons in specific ID3 tags in the specified song path.

    This check is used to prevent .bpstat files from failing to import.
    """
    # TODO: check if this actually works
    out_file = load(song_path)
    for field in [out_file.tag.artist, out_file.tag.title, out_file.tag.album]:
        field = field.replace(";", "")

    out_file.tag.save(version=(2,3,0))

def check_for_semicolons(song):
    """
    Check for semicolons in a given Song object, warn and return True if present.

    :param song: The libpytunes Song object to use for processing.
    """

    for field in [song.artist, song.name, song.album]:
        if field and ";" in field:
            logging.warn(f"Semicolon detected in {song.name=} ({song.persistent_id=})! "
                         f"This can cause .bpstat imports to fail.")
            return True
    return False

def add_to_bpstat(song, bpstat_prefix, bpstat_path):
    """
    Append a song to a line in the specified .bpstat.
    
    :param song: The libpytunes Song object to use for processing.
    :param bpstat_prefix: The folder used within the .bpstat for its filepath field.
    :param bpstat_path: The full location of the .bpstat itself.
    """
    bpsong = bpparse.BPSong.from_song(song)
    output = bpsong.as_bpstat_line(bpstat_prefix) + "\n"

    with open(bpstat_path, "ab") as fp:
        fp.write(output.encode('utf-8'))

def create_backup(file_path, output_folder='backups'):
    """
    Creates a backup of the specified file, usually a bpstat or XML.

    :param file_path: The full location of the file to backup.
    :param output_folder: :param output_folder: The folder to output the copied/processed song to. `/backups` by default.
    
    The file is named `backup-%Y-%m-%d %H-%M-%S` with its original extension.

    Backups are stored in /backups relative to the run location by default. 
    """
    _, file_extension = os.path.splitext(file_path)
    file_name = datetime.now().strftime("backup-%Y-%m-%d %H-%M-%S"+file_extension)
    
    out_path = os.path.join(output_folder, file_name)

    copy2(file_path, out_path)

def first_sync_array_from_lib(lib):
    """
    Creates a 2D array suitable for use with the SongView in the first-time sync window.

    :param lib: A libpytunes Library object.

    Assumes copying and tracking should be enabled.
    """
    # TODO: Decide on using *(length) or Y/N(length-length)
    headers = ["Track ID", "Copy?", "Track?", "Title", "Artist", "Album", "Plays", "Trimmed?", "Volume%", "Filepath"]

    data = []
    for track_id, song in lib.songs.items():
        play_count = song.play_count if song.play_count else 0
        trimmed = bool(song.start_time or song.stop_time)
        volume = 100
        if song.volume_adjustment:
            gain_factor = ((song.volume_adjustment + 255)/255)
            volume = gain_factor*100
        
        data.append([track_id, 1, 1, song.name, song.artist, song.album, play_count, trimmed, volume, song.location])

    return data