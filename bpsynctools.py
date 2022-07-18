"""
Various convenience functions and objects
"""

import os
import platform
import subprocess
import logging
import hashlib
import time

from collections import namedtuple
from shutil import copy2
from datetime import datetime
from math import log10
from pathlib import Path
from dataclasses import dataclass

from PySide6 import QtWidgets
from pydub import AudioSegment
from pydub.utils import mediainfo
from eyed3 import load
import sqlalchemy.orm.exc

import bpparse
import models

logger = logging.getLogger(__name__)

# Dataclass for easy statistics use
@dataclass
class TableStatistics:
    total_size: int = 0
    num_tracking: int = 0
    num_processing: int = 0
    size_processing: int = 0 

    def __add__(self, rhs):
        if isinstance(rhs, self.__class__):
            self.total_size += rhs.total_size
            self.num_tracking += rhs.num_tracking
            self.num_processing += rhs.num_processing
            self.size_processing += rhs.size_processing
            return self
        else:
            raise NotImplementedError("Can't add anything other than two TableStatistics")

# region Processing

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
    # affirm output_folder (and any parent folders, if specified) exists, and make it if it doesn't exist
    # https://docs.python.org/3/library/pathlib.html#pathlib.Path.mkdir
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    # define output paths
    _, file_extension = os.path.splitext(song.location)
    output_path = os.path.join(output_folder, song.persistent_id + ".mp3")

    try:
        if file_extension != ".mp3" or song.start_time or song.stop_time or song.volume_adjustment:
            logger.info(f"{song.persistent_id} needs to be processed by pydub ({output_path})")
            obj = AudioSegment.from_file(song.location)

            if song.start_time or song.stop_time:
                start_time = 0 if not song.start_time else song.start_time
                stop_time = len(obj) if not song.stop_time else song.stop_time

                obj = obj[start_time:stop_time]

                logger.info(f"Trimmed {song.persistent_id}")
            
            if song.volume_adjustment:
                # internally stored as an integer between -255 and 255
                # but can physically be adjusted past 255
                if song.volume_adjustment <= -255:
                    obj = obj - 100  # essentially silent
                    logger.warning(f"The song {song.name} has a volume adjustment value less than -255 and is silent!")
                else:
                    gain_factor = (song.volume_adjustment + 255)/255
                    decibel_change = 10 * log10(gain_factor)
                    obj = obj + decibel_change
                    logger.info(f"Changed {song.name} gain factor by {gain_factor} ({decibel_change} dB)")

            # tags parameter is used for retaining metadata
            obj.export(output_path, format="mp3", tags=mediainfo(song.location)['TAG'])
        else:
            logger.info(f"{song.persistent_id} does not need to be processed and was directly copied ({output_path})")
            copy2(song.location, output_path)
    except FileNotFoundError as e:
        logger.error(f"Couldn't find {song.location}")
    
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
            logger.warning(f"Semicolon detected in {song.name=} ({song.persistent_id=})! "
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

def add_to_exportimport(lib, selected_fields, output_path):
    """
    Append a song to a line in the specified text file.

    For use with https://samsoft.org.uk/iTunes/scripts.asp#ExportImport.
    
    :param lib: The libpytunes library to use.
    :param selected_fields: A list of strings with the field names.
    :param output_path: The full location of the txt file to use.
    """
    # Map of tagName to libpysong attributes, used with getattr
    attrs = {
        "Location": "location",
        "DateAdded": "date_added",
        "Name": "name",
        "Album": "album",
        "SortAlbum": "sort_album",
        "AlbumArtist": "album_artist",
        "Artist": "artist",
        "Composer": "composer",
        "Grouping": "grouping",
        "Genre": "genre",
        "Compilation": "compilation",
        "DiscNumber": "disc_number",
        "DiscCount": "disc_count",
        "TrackNumber": "track_number",
        "TrackCount": "track_count",
        "Year": "year",
        "Plays": "play_count",
        "Played": "lastplayed",
        "Skips": "skip_count",
        "Skipped": "skip_date",
        "Comment": "comments",
        "BitRate": "bit_rate",
        "KindAsString": "kind",
        "BPM": "bpm",
        "EQ": "equalizer",
        "VA": "volume_adjustment",
        "Start": "start_time",
        "Finish": "stop_time",
    }

    logger.debug(f"Attempting write of ExportImport file with fields {selected_fields}")

    # Overwrite the file if needed
    with open(output_path, "w", encoding="utf-16") as fp:
        fp.write("")

    # This adds the BOM if needed
    # ExportImport files are in utf-16, *not* utf-8
    with open(output_path, "a", encoding="utf-16") as fp:
        for _, song in lib.songs.items():
            fp.write(f"<ID>{song.persistent_id[0:8]}-{song.persistent_id[8:16]}\n")
            
            for field in selected_fields:
                try:
                    attr_name = attrs[field]
                except KeyError:
                    logger.error(f"Tried to look up {field}, but it doesn't exist in the available fields; skipping")
                    continue
            
                try:
                    field_value = getattr(song, attr_name)
                except AttributeError:
                    logger.error(f"Song object doesn't have attribute {attr_name}? (programming error)")
                    continue

                # Special processing for specific fields
                if attr_name in ["date_added", "skip_date", "lastplayed"]:
                    # If no date is set, then default to "12:00:00 AM"
                    if field_value == None:
                        field_value = "12:00:00 AM"
                    else:
                        # If a date is set, convert it to the format 1/6/2022 5:32:11 PM
                        # Unfortunately platform support for no-padding is implementation-dependent,
                        # so it's not exact
                        field_value = time.strftime("%m/%d/%Y %I:%M:%S %p", field_value)
                elif attr_name in ["play_count", "skip_count"]:
                    # If no playcount or skipcount field exists, that's equivalent
                    # to 0 playcount/skipcount
                    if field_value == None:
                        field_value = 0
                elif attr_name in ["start_time", "stop_time"]:
                    # The result is always rounded down to an integer (regardless of what
                    # the actual value in msec is).
                    #
                    # If no stop or start time has been set, either 0 (for start time)
                    # or the length of the song in seconds (for stop time) is printed out.
                    if field_value == None:
                        if attr_name == "start_time":
                            field_value = 0
                        else:
                            field_value = song.total_time // 100
                    else:
                        field_value = field_value // 100
                else:
                    if field_value == None:
                        field_value = ""

                fp.write(f"<{field}>{field_value}\n")

            # Separating newline
            fp.write("\n")

    logger.debug(f"ExportImport write complete")

# endregion

def create_backup(file_path, output_folder='backups'):
    """
    Creates a backup of the specified file, usually a bpstat or XML.

    :param file_path: The full location of the file to backup.
    :param output_folder: :param output_folder: The folder to output the copied/processed song to. `/backups` by default.
    
    The file is named `backup-%Y-%m-%d %H-%M-%S` with its original extension.

    Backups are stored in /backups relative to the run location by default. 
    """
    os.makedirs(output_folder, exist_ok=True)

    _, file_extension = os.path.splitext(file_path)
    file_name = datetime.now().strftime("backup-%Y-%m-%d %H-%M-%S"+file_extension)
    
    out_path = os.path.join(output_folder, file_name)

    copy2(file_path, out_path)

# region Utility

def first_sync_array_from_libpysongs(songs):
    """
    Creates a 2D array suitable for use with the SongView in the first-time sync window.

    :param lib: A dict of libpytunes Song objects, with the track ID as keys.

    Assumes copying and tracking should be enabled.
    """
    # TODO: Decide on using *(length) or Y/N(length-length)
    headers = ["Track ID", "Copy?", "Track?", "Title", "Artist", "Album", "Plays", "Trimmed?", "Volume%", "Filepath"]

    data = []
    for track_id, song in songs.items():
        play_count = song.play_count if song.play_count else 0
        trimmed = bool(song.start_time or song.stop_time)
        volume = 100
        if song.volume_adjustment:
            gain_factor = ((song.volume_adjustment + 255)/255)
            volume = gain_factor*100
        
        data.append([track_id, 1, 1, song.name, song.artist, song.album, play_count, trimmed, volume, song.location])

    return data

def standard_sync_arrays_from_data(library, bpstat_songs):
    """
    Creates the two 2D arrays used to create the standard sync tables.

    :param library: A dictionary of track IDs to libpytunes Song objects.
    :param bpstat_songs: A list of BPSong objects.

    Occurs in about four steps, two of which are done in the UI function:
    - Start by trying to load/open all three files. Raise RuntimeError (or another exception) if fail.
    - Get all internal database song objects.

    The following are done here:
    - For each song in the XML:
        - If there exists an entry by persistent ID in both the bpstat and database:
            - Calculate (but do not update) the delta and create a row for the first table.
        - If not:
            - Add that specific Song entry to a separate dictionary, which is (eventually) passed into
              first_sync_array_from_libpysongs()
        Additionally, if the songs requires reprocessing through ffmpeg (due to an ID3 tag
        change or other qualifying change, like a change in volume or song length):
            - Add a checkbox in the "Reprocess" column.
    - Call first_sync_array_from_libpysongs() to create the second table's rows.
    """
    # this function can only possibly be called after the database has been initialized
    if models.Session:
        session = models.Session() 
    else:
        logger.error("Attempted call to make standard sync array when session hadn't been established yet.")
        raise AssertionError()

    # create dict for bpstat songs, by persistent id
    bpsongs = {}
    for bpsong in bpstat_songs:
        bpsongs[bpsong.get_persistent_id()] = bpsong

    # start checking in both
    new_songs = {}
    existing_songs_rows = []
    for track_id, song in library.songs.items():
        # check if the song exists in both the bpstat and the database
        try:
            stored_song = session.query(models.StoredSong).filter(models.StoredSong.persistent_id==song.persistent_id).scalar()
            bpstat_song = bpsongs[song.persistent_id]

            if not stored_song:
                raise KeyError()  # same behavior as bpstat_song throwing a KeyError upon no result found
        except sqlalchemy.orm.exc.MultipleResultsFound:
            logger.error("Database has multiple entries of the same ID?")
            continue
        except KeyError:
            # The song doesn't exist in the StoredSong or wasn't in the bpstat.
            # Check if the song was previously ignored (i.e.) a corresponding IgnoredSong entry exists.
            # If so, then do not attempt to add it to the new song table.
            ignored_song = session.query(models.IgnoredSong).filter(
                models.IgnoredSong.persistent_id == song.persistent_id).scalar()

            if not ignored_song:
                new_songs[track_id] = song

            # In all cases, since the song is not being tracked, move on to the next song.
            continue

        # if it gets here, then the song is being tracked
        # note that songs are added to this table/2D array regardless of its playcount has changed or not
        # ["Track ID", "Reprocess", "Title", "Artist", "Album", "Base plays", "XML plays", "BP plays", "Delta", "New playcount", "Persistent ID"]
        play_count = song.play_count if song.play_count else 0
        delta = stored_song.get_delta(play_count, bpstat_song.total_plays)
        
        # Default to not drawing checkbox by default. -1 indicates "no checkbox"
        # to the underlying widgets. 
        reprocess = -1
        if stored_song.needs_reprocessing(song):
            # This StoredSong method takes in a libpytunes Song object and compares the
            # relevant fields to see if reprocessing is needed. If it returns true,
            # which occurs if ANY qualifying field has changed, then set the checkbox
            # to equal 1.
            reprocess = 1
        
        existing_songs_rows.append([track_id, reprocess, song.name, song.artist, song.album, stored_song.last_playcount, play_count,
                                   bpstat_song.total_plays, delta, stored_song.last_playcount+delta, song.persistent_id])

    # create data for first-time from dict
    new_songs_rows = first_sync_array_from_libpysongs(new_songs)

    return existing_songs_rows, new_songs_rows

def open_file(path):
    """
    Reveal a given path or file in the native file explorer.
    :param path: The filepath to "reveal".
    """
    # https://stackoverflow.com/questions/281888/open-explorer-on-a-file
    # https://stackoverflow.com/questions/6631299/python-opening-a-folder-in-explorer-nautilus-finder
    if platform.system() == "Windows":
        # For some reason, backslashes are required for this to work.
        # Forward slashes will just open in the "default" explorer location.
        subprocess.Popen(["explorer", "/select,", path.replace('/', '\\')])
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])

def humanbytes(B):
    # https://stackoverflow.com/questions/12523586/python-format-size-application-converting-b-to-kb-mb-gb-tb
    # note: just like windows, this technically refers to kibibytes, mebibytes, etc.
    """
    Return the given bytes as a human friendly KB, MB, GB, or TB string.

    :param B: The number of bytes.
    """
    B = float(B)
    KB = float(1024)
    MB = float(KB ** 2)  # 1,048,576
    GB = float(KB ** 3)  # 1,073,741,824
    TB = float(KB ** 4)  # 1,099,511,627,776

    if B < KB:
        return '{0} B'.format(B)
    elif KB <= B < MB:
        return '{0:.2f} KB'.format(B / KB)
    elif MB <= B < GB:
        return '{0:.2f} MB'.format(B / MB)
    elif GB <= B < TB:
        return '{0:.2f} GB'.format(B / GB)
    elif TB <= B:
        return '{0:.2f} TB'.format(B / TB)

def get_statistics(array_data, lib, tracking_column: int, processing_column: int):
    """
    Calculate statistics given a table's underlying data and the indexes of the tracking and processing columns.

    Pass None to tracking_column or processing_column to skip.

    This function assumes track IDs are available at column 0 of array_data.
    These are used to look sizes up against `lib`.

    :param array_data: The underlying table model data.
    :param lib: The libpytunes library represented by this data.
    :param tracking_column: The index of the column representing songs to track.
    :param processing_column: The index of the column representing songs to process.
    
    Returns a named tuple with the following fields:
    :retval total_size: Size (in bytes) of the songs represented in this table.
    :retval num_tracking: Number of songs being tracked.
    :retval num_processing: Number of songs being processed.
    :retval size_processing: Size (in bytes) of songs being processed.
    """
    stats = TableStatistics()
    
    # Assert tracking_column and processing_column in range
    num_columns = len(array_data[0])
    if tracking_column < 1 or tracking_column >= num_columns:
        raise RuntimeError("tracking_column out of range")
    if processing_column < 1 or processing_column >= num_columns:
        raise RuntimeError("processing_column out of range")

    for row in array_data:
        try:
            track_id = row[0]
            song = lib.songs[track_id]
        except KeyError:
            logger.error(f"Didn't find {track_id} in the underlying library, but it was in the table?")
            continue
        
        stats.total_size += song.size
        
        if tracking_column and row[tracking_column] == 1:
            stats.num_tracking += 1
        
        if processing_column and row[processing_column] == 1:
            stats.num_processing += 1
            stats.size_processing += song.size
                
    return stats

# endregion

# region UI

def show_error_window(text, informative_text, title):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText(text)
    msg.setInformativeText(informative_text)
    msg.setWindowTitle(title)
    msg.exec()

# endregion