"""
Various convenience functions and objects
"""

import os
import platform
import subprocess
import logging
import hashlib
import time
import xml
import re

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
from mutagen.easyid3 import EasyID3
import sqlalchemy.orm.exc
import libpytunes

from bpsyncwidgets import SongView
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
    ffmpeg/libav.
    """
    # affirm output_folder (and any parent folders, if specified) exists, and make it if it doesn't exist
    # https://docs.python.org/3/library/pathlib.html#pathlib.Path.mkdir
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    # define output paths
    _, file_extension = os.path.splitext(song.location)
    output_path = os.path.join(output_folder, song.persistent_id + ".mp3")

    try:
        if file_extension != ".mp3" or song.start_time or song.stop_time or song.volume_adjustment:
            logger.info(f"{song.persistent_id} needs to be processed by ffmpeg ({output_path})")
            ffmpeg = ['ffmpeg', '-loglevel', 'fatal', '-y', '-i', song.location]

            if song.start_time:
                ffmpeg += ['-ss', f'{song.start_time / 1000:g}']
                logger.info(f"Trimmed Start {song.persistent_id}")

            if song.stop_time:
                ffmpeg += ['-to', f'{song.stop_time / 1000:g}']
                logger.info(f"Trimmed End {song.persistent_id}")
            
            # avoid reencoding for insignificant volume changes. values can be adjusted if need be
            if song.volume_adjustment and (song.volume_adjustment < -2 or song.volume_adjustment > 2):
                # internally stored as an integer between -255 and 255
                # but can physically be adjusted past 255
                gain_factor = (song.volume_adjustment + 255)/255
                decibel_change = 20 * log10(gain_factor)

                # run ffmpeg once to detect peak dB of song. this costs ~0.4s per file, but solves clipping distortion
                # non-windows os should use '/dev/null' in place of 'NUL' in the ffmpeg parameters below
                ffmpeg_pipe = subprocess.run(['ffmpeg', '-i', song.location, '-af', 'volumedetect', '-vn', '-sn', '-dn', '-f', 'null', 'NUL'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                ffmpeg_pipe = re.search(r"max_volume: (\S+) dB", str(ffmpeg_pipe))
                if ffmpeg_pipe is not None:
                    decibel_peak = float(ffmpeg_pipe.group(1))
                
                if ffmpeg_pipe is not None and decibel_peak + decibel_change > 0:
                    # technically acompressor would be more accurate here, but im too lazy to implement it and alimiter is close enough
                    # TODO: consider lowering alimiter 'attack' to 1 (ms) (default is 5 ms)
                    # TODO: implement acompressor instead
                    ffmpeg += ['-af', f'alimiter=limit={-decibel_change}dB']
                else:
                    ffmpeg += ['-af', f'volume={decibel_change}dB']
                logger.info(f"Changed {song.name} gain factor by {gain_factor} ({decibel_change} dB)")

            # volume changes/mp3 conversions require reencoding
            if file_extension != ".mp3" or song.volume_adjustment:
                ffmpeg += ['-q:a', '0']
            else:
                ffmpeg += ['-c', 'copy']
            ffmpeg += ['-id3v2_version', '3', output_path]

            subprocess.run(ffmpeg)

            # '-ss' throws away any data before the timestamp which includes
            # the thumbnail, so it must be readded and reprocessed, but
            # `-c copy` is fast, so speed shouldn't be significantly affected
            if song.start_time:
                temp_output = os.path.join(output_folder, "out.mp3")
                subprocess.run(['ffmpeg', '-loglevel', 'fatal', '-y', '-i', song.location, '-i', output_path, '-map', '0:v:0', '-map', '1:a:0', '-c', 'copy', '-id3v2_version', '3', temp_output])
                # ffmpeg can't write over itself, so a temp file
                # must be made and then replaced afterwards
                os.replace(temp_output, output_path)
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
    out_file = EasyID3(song_path)
    for field_name in ["title", "artist", "album"]:
        out_file[field_name] = [out_file[field_name][0].replace(";", ";")]

    out_file.save()

def check_for_semicolons(song):
    """
    Check for semicolons in a given Song object, warn and return True if present.

    :param song: The libpytunes Song object to use for processing.
    """

    for field in [song.artist, song.name, song.album]:
        if field and ";" in field:
            logger.warning(f"Semicolon detected in {song.name=} ({song.persistent_id=})")
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

    logger.info(f"Attempting write of ExportImport file with fields {selected_fields}")

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

    logger.info(f"ExportImport write complete")

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

def standard_sync_arrays_from_data(library, bpstat_songs, calculate_file_hashes):
    """
    Creates the two 2D arrays used to create the standard sync tables.

    :param library: A dictionary of track IDs to libpytunes Song objects.
    :param bpstat_songs: A list of BPSong objects.
    :param calculate_file_hashes: Whether to calculate file hashes (a long operation) to determine if reprocessing is needed.

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
    for track_id, song in library.items():
        # check if the song exists in both the bpstat and the database
        try:
            stored_song = session.query(models.StoredSong).filter(models.StoredSong.persistent_id==song.persistent_id).scalar()
            bpstat_song = bpsongs.get(song.persistent_id, None)

            if not stored_song and bpstat_song is not None:
                # This should only ever happen due to user error
                logger.error(f"{song.persistent_id} exists in bpstat but not in the database")
                continue
            elif not stored_song and bpstat_song is None:
                logger.info(f"{song.name} ({song.persistent_id}) is a new song")
                # The song doesn't exist in the StoredSong and wasn't in the bpstat.
                # Check if the song was previously ignored (i.e.) a corresponding IgnoredSong entry exists.
                # If so, then do not attempt to add it to the new song table.
                ignored_song = session.query(models.IgnoredSong).filter(
                    models.IgnoredSong.persistent_id == song.persistent_id).scalar()

                if not ignored_song:
                    new_songs[track_id] = song

                # In all cases, since the song is not being tracked, move on to the next song.
                continue
            elif stored_song and bpstat_song is None:
                # The song doesn't exist in the bpstat but exists in StoredSong.
                # This happens since Blackplayer doesn't export tracks with 0 plays into bpstat.
                assert stored_song.last_playcount == 0, f"{song.name} ({song.persistent_id}) has a playcount higher than 0 but does not appear within bpstat"
                logger.info(f"{song.name} ({song.persistent_id}) is already in the database but isn't in bpstat")
                # Songs with 0 plays in bpstat should have no changes and don't need a checkbox
                reprocess = -1
                existing_songs_rows.append([track_id, reprocess, song.name, song.artist, song.album, stored_song.last_playcount, 0,
                                        0, 0, stored_song.last_playcount, song.persistent_id])
                continue
            else:
                pass
        except sqlalchemy.orm.exc.MultipleResultsFound:
            logger.error("Database has multiple entries of the same ID?")
            continue

        # if it gets here, then the song is being tracked
        # note that songs are added to this table/2D array regardless of its playcount has changed or not
        # ["Track ID", "Reprocess", "Title", "Artist", "Album", "Base plays", "XML plays", "BP plays", "Delta", "New playcount", "Persistent ID"]
        play_count = song.play_count if song.play_count else 0
        delta = stored_song.get_delta(play_count, bpstat_song.total_plays)
        
        # Default to not drawing checkbox by default. -1 indicates "no checkbox"
        # to the underlying widgets. 
        reprocess = -1
        if stored_song.needs_reprocessing(song, calculate_file_hashes):
            # This StoredSong method takes in a libpytunes Song object and compares the
            # relevant fields to see if reprocessing is needed. If it returns true,
            # which occurs if ANY qualifying field has changed, then set the checkbox
            # to equal 1.
            #
            # calculate_file_hashes is an optional argument that skips calculating file
            # hashes, since it is a long operation.
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
    
    # Assert that there actually is array_data; else, just return stats which defaults to 0
    if not array_data:
        return stats

    # Assert tracking_column and processing_column in range
    num_columns = len(array_data[0])
    if tracking_column and (tracking_column < 1 or tracking_column >= num_columns):
        raise RuntimeError("tracking_column out of range")
    if processing_column and (processing_column < 1 or processing_column >= num_columns):
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

def get_std_data(xml_path, bpstat_path, database_path):
    """
    Get the standard sync data from the specified filepaths.

    :param xml_path: Path to an exported XML.
    :param bpstat_path: Path to the newest bpstat file.
    :param database_bath: Path to the program database.
    """
    # try generating the libpytunes library from specified XML
    try:
        lib = libpytunes.Library(xml_path)
    except xml.parsers.expat.ExpatError as e:
        show_error_window("Invalid XML file!",
                            f"Couldn't parse XML file (if it is one) - {e}",
                            "Invalid XML file")
        return
    except FileNotFoundError:
        show_error_window("File not found!",
                            "The entered path doesn't appear to exist.",
                            "Invalid XML filepath")
        return

    ## try generating bpstat library
    bpsongs = bpparse.get_songs(bpstat_path)
    if not bpsongs:
        show_error_window(".bpstat malformed!",
                            "The program wasn't able to find any valid songs in this file.",
                            "Invalid .bpstat file")
        return

    ## try getting elements from db
    try:
        models.initialize_engine(database_path)
    except Exception as e:
        show_error_window("Something went wrong while connecting to the database!",
                            str(e),
                            "Database error")
        return
    with models.Session() as session:
        db_songs = session.query(models.StoredSong).all()
    if not db_songs:
        show_error_window("No songs in database!",
                    "A database query yielded no results.",
                    "Database error")
        return
    
    return lib, bpsongs, db_songs

def return_spinbox_value_or_none(spinbox: QtWidgets.QAbstractSpinBox): 
    """
    Returns either the spinbox's current value or none, depending on if the min value is set.

    Supports QSpinBox and QDateTimeEdit - if minimumDateTime() is not available,
    then minimum() is used. 

    If it looks like a QDateTimeEdit, then it's automatically converted to a 
    time struct.
    """
    if hasattr(spinbox, "minimumDateTime"):
        # It's a QDateTimeEdit.
        if spinbox.dateTime() != spinbox.minimumDateTime():
            return time.gmtime(spinbox.dateTime().toSecsSinceEpoch())
        else:
            return None
    elif hasattr(spinbox, "minimum"):
        # It's a QSpinBox (probably).
        if spinbox.value() != spinbox.minimum():
            return spinbox.value()
        else:
            return None
    else:
        logger.error(f"return_value_or_none(): spinbox has no minimum function?")
        raise AssertionError("Spinbox argument does not have a minimum function/attribute")

def handle_updated_song_data(new_data, target_row, table:SongView, processing_column=1):
    """
    Handle any extra logic associated with updating the models from a
    song info window update.

    Assumed convention is that the processing column is at index 1.

    :param new_data: A 2D array of one row from a helper function representing a row in `data`.
    :param target_row: The index of the row (in `table.table_model`) to update.
    :param table: The relevant table to update (a bpsyncwidgets.SongView.)
    """
    data = table.table_model.array_data

    # Processing column handling
    if new_data[0][processing_column] == 1:
        if data[target_row][processing_column] == -1:
            # If this is a reprocessable song, and it was previously 
            # unprocessable, then set its checkbox to 0.
            new_data[0][processing_column] = 0
        else:
            # If this was previously reprocessable, and it still is, 
            # keep its checkbox as-is.
            new_data[0][processing_column] = data[target_row][processing_column]
    else:
        if data[target_row][processing_column] != -1:
            # If this was previously processable and now isn't,
            # use setData to set the table model data to 0
            # to force a stat update if needed.
            idx = table.table_model.index(target_row, processing_column)
            table.table_model.setData(idx, 0)
        else:
            # If this was previously unprocessable and still isn't,
            # do nothing.
            pass

    # Update row in data
    data[target_row] = new_data[0]

    # Tell the model to update
    # inefficient call?
    table.set_data(data)

# endregion