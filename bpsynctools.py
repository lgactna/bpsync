import os
from shutil import copy2
from datetime import datetime
import logging

from pydub import AudioSegment
from pydub.utils import mediainfo
from eyed3 import load

import bpparse

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

def strip_semicolons(song_path):
    """
    Replace semicolons in specific ID3 tags in the specified song path.

    This check is used to prevent .bpstat files from failing to import.
    """
    out_file = load(song_path)
    for field in [out_file.tag.artist, out_file.tag.title, out_file.tag.album]:
        field = field.replace(";", "")

    out_file.tag.save(version=(2,3,0))

def add_to_bpstat(song, target_folder, bpstat_path):
    """
    Append a song to a line in the specified .bpstat.
    
    :param song: The libpytunes Song object to use for processing.
    :param target_folder: The folder used within the .bpstat for its filepath field.
    :param bpstat_path: The full location of the .bpstat itself.
    """
    bpsong = bpparse.BPSong.from_song(song)
    output = bpsong.as_bpstat_line(target_folder) + "\n"

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