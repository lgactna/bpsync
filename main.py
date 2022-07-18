# Standard library
import logging
import xml.parsers.expat
import sys

# Forked libpytunes
from libpytunes import Library

# Local imports
import bpsynctools
import bpsyncwidgets
import bpparse
import models

logging.basicConfig(filename='bpsync.log', 
                    encoding='utf-8', 
                    level=logging.DEBUG,
                    format='%(filename)s:%(lineno)d | %(asctime)s | [%(levelname)s] - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))

# dev constants - not used in program
LIBRARY = 'iTunes_Music_Library.xml'
DATA_FOLDER = 'data'
SONGS_FOLDER = 'tmp'

TARGET_FOLDER = '/storage/sdcard1/imported-music/'

from main_menu import Ui_MainMenuWindow
from first_time import Ui_FirstTimeWindow
from std_sync import Ui_StandardSyncWindow
from ignored_songs import Ui_IgnoredSongsDialog
from progress import Ui_ProcessingProgress
from exportimport import Ui_ExportImportWindow
from PySide6 import QtWidgets, QtCore, QtGui

class MainMenuWindow(QtWidgets.QWidget, Ui_MainMenuWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.launch_first_button.clicked.connect(self.open_first_sync)
        self.launch_std_button.clicked.connect(self.open_std_sync)
        self.launch_export_button.clicked.connect(self.open_export_dialog)
        self.launch_bpstat_button.clicked.connect(self.open_bpstat_converter)
        self.launch_m3u_button.clicked.connect(self.open_m3u_generator)

    # Note - these windows will disappear as soon as there are no references
    # to them, so we use self.window
    #
    # Before, this wasn't necessary, probably because of some lambda call leading
    # to a permanent reference out in space
    def open_first_sync(self):
        self.window = FirstTimeWindow()
        self.window.show()

    def open_std_sync(self):
        self.window = StandardSyncWindow()
        self.window.show()

    def open_export_dialog(self):
        self.window = ExportImportWindow()
        self.window.show()

    def open_bpstat_converter(self):
        pass

    def open_m3u_generator(self):
        pass

class FirstTimeWindow(QtWidgets.QWidget, Ui_FirstTimeWindow):
    def __init__(self):
        super().__init__()

        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setupUi(self)

        self.program_path = QtCore.QDir.currentPath()
        self.lib = None  # libpytunes Library object
        self.thread_manager = QtCore.QThreadPool()
        
        # Top-right statistics; all 0 at start.
        self.stats = bpsynctools.TableStatistics()

        # Prepopulate fields
        self.mp3_path_lineedit.setText('tmp')
        self.data_path_lineedit.setText('data')

        # Signals and slots
        # Buttons
        self.xml_browse_button.clicked.connect(self.xml_open_prompt)
        self.xml_load_button.clicked.connect(self.update_with_xml)
        self.mp3_browse_button.clicked.connect(self.mp3_save_prompt)
        self.data_browse_button.clicked.connect(self.data_save_prompt)
        self.start_button.clicked.connect(self.start_processing)
        # Table functionality
        # Note: the context menu policy must be changed to 
        # self.table_widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # for this to work
        self.table_widget.customContextMenuRequested.connect(lambda pos: self.table_widget.show_context_menu(pos, self.lib))
        self.table_widget.context_menu_enabled = True
        self.table_filter_lineedit.textChanged.connect(lambda text: self.table_widget.proxy.set_filter_text(text))
        self.table_widget.songChanged.connect(self.update_song_in_table_widget)

        # Table
        # In order: column headers, starting data, checkbox columns, columns to filter on with lineedit
        headers = ["Track ID", "Process?", "Track?", "Title", "Artist", "Album", "Plays", "Trimmed?", "Volume%", "Filepath"]
        data = [[1, 1, 1, "YU.ME.NO !", "ユメガタリ(ミツキヨ , shnva)", " ユメの喫茶店", 24, "No", "100%", "D:/Music/a.mp3"]]
        box_columns = [1, 2]
        filter_on = [3, 4, 5]

        column_sizes = [50, 100, 100, 200, 120, 120, 50, 100, 50, 200]

        ## Set up initial table contents and formatting
        self.table_widget.setup(headers, box_columns, filter_on)
        self.table_widget.set_data(data)
        self.table_widget.set_column_widths(column_sizes)

        # Enable updates from checkbox
        # Note that this breaks if the underlying table model is changed (which shouldn't change)
        self.table_widget.table_model.dataChanged.connect(lambda idx: self.update_stats_from_index(idx, self.table_widget))

    def xml_open_prompt(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open XML", self.program_path,
                "XML (*.xml);;All Files (*)")
        if file_name:
            self.xml_path_lineedit.setText(file_name)

    def mp3_save_prompt(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self,
                "Select processed mp3 directory", self.program_path)
        if directory:
            self.mp3_path_lineedit.setText(directory)

    def data_save_prompt(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self,
                "Select data directory", self.program_path)
        if directory:
            self.data_path_lineedit.setText(directory)

    def update_with_xml(self):
        # get contents of lineedit
        xml_path = self.xml_path_lineedit.text()
        if not xml_path:
            bpsynctools.show_error_window("Please enter an XML path!",
                              "You can do this by manually entering the path or selecting it by clicking Browse.",
                              "No XML path defined")
            return
        # generate library from it
        try:
            self.lib = Library(xml_path)
        except xml.parsers.expat.ExpatError as e:
            bpsynctools.show_error_window("Invalid XML file!",
                              f"Couldn't parse XML file (if it is one) - {e}",
                              "Invalid XML file")
            return
        except FileNotFoundError:
            bpsynctools.show_error_window("File not found!",
                              "The entered path doesn't appear to exist.",
                              "Invalid XML filepath")
            return
        
        # update table from it
        data = bpsynctools.first_sync_array_from_libpysongs(self.lib.songs)
        self.table_widget.set_data(data)

        # Generate initial statistics (overwrites current object)
        self.stats = bpsynctools.get_statistics(self.table_widget.table_model.array_data, self.lib, 2, 1)

        # Update stat labels
        self.update_statistics_labels()

    def update_song_in_table_widget(self, song):
        """
        Called when a Song object in self.lib is modified by any means.

        It is this window's responsibility to know how to handle the change
        of a song object in the underlying library.
        """
        # TODO: does this make more sense as a callback-based function in SongView?
        # honestly, it may make more sense to inherit SongView and just have a "new songs"
        # subclass of SongView and a "updated songs" subclass. on the other hand, this gives us
        # a little more control over the logic if something does need to happen
        # in one table that doesn't happen in the other
        #
        # alternatively, we could just set up a callback function that dictates where to
        # get data from
        #
        # also at this point songview should inherit from a generic "table with 
        # checkbox" class

        # Search for equivalent row in the underlying data
        # Linear is good enough
        data = self.table_widget.table_model.array_data
        target_index = -1
        for index, row in enumerate(data):
            if row[0] == song.track_id:
                target_index = index
                break

        if target_index == -1:
            logger.error(f"Tried looking up {song.track_id} in the model, but it wasn't there?")
            return

        # Generate a "fake" first_sync_array from the song
        temp_lib = {song.track_id: song}
        new_data = bpsynctools.first_sync_array_from_libpysongs(temp_lib)

        # Update row in data
        data[target_index] = new_data[0]

        # Tell the model to update
        # inefficient call?
        self.table_widget.set_data(data)

    def update_stats_from_index(self, index, table):
        """
        Update the top-right statistics from a checkbox tick/untick.
        """
        # Check if library has been loaded; else, ignore
        if not self.lib:
            return

        # Check if the index's column is in one of the checkbox columns; else, ignore
        if index.column() not in table.table_model.checkbox_columns:
            return
        
        # Get track ID in the same row as the index in column 0
        # Signature: createIndex(row, column, ptr)
        # ptr is quite interesting: https://doc.qt.io/qtforpython/PySide6/QtCore/QAbstractItemModel.html#PySide6.QtCore.PySide6.QtCore.QAbstractItemModel.createIndex
        track_id_index = table.table_model.createIndex(index.row(), 0, table)
        track_id = table.table_model.data(track_id_index, QtCore.Qt.DisplayRole)

        # Look it up in the library
        try:
            song = self.lib.songs[track_id]
        except KeyError:
            # If it doesn't exist (somehow), exit early
            logger.error(f"Couldn't find {track_id} when updating statistics?")
            return

        # Either increment or decrement counters as needed
        # It's the case that processing is always in column index 1,
        # and tracking is always in column index 2. This is hardcoded
        # because I don't expect this to change anytime soon.

        # Get new state of checkbox and update stats accordingly
        new_state = table.table_model.data(index, QtCore.Qt.DisplayRole)
        if index.column() == 1:
            if new_state == True:
                self.stats.num_processing += 1
                self.stats.size_processing += song.size                
            else:
                self.stats.num_processing -= 1
                self.stats.size_processing -= song.size
        elif index.column() == 2:
            if new_state == True:
                self.stats.num_tracking += 1      
            else:
                self.stats.num_tracking -= 1
        else:
            logger.error(f"Tried looking up column {index.column()} for statistics updates?")

        # Update statistics labels
        self.update_statistics_labels()
    
    def update_statistics_labels(self):
        """
        Update labels from self.stats. 
        
        Call after the XML has been loaded or a checkbox state has changed.
        """
        # Check if self.lib loaded; else, refuse.
        if not self.lib:
            logger.error(f"Tried to update statistics when the table wasn't ready yet?")
            return
        
        # len() is constant time in CPython.
        num_tracks = len(self.lib.songs)

        # Update all labels.
        self.tracks_found_label.setText(f"{num_tracks} tracks found")
        self.tracks_totalsize_label.setText(f"{bpsynctools.humanbytes(self.stats.total_size)} total size")
        self.tracks_synccount_label.setText(f"{self.stats.num_tracking} songs to track")
        self.tracks_copysize_label.setText(f"{bpsynctools.humanbytes(self.stats.size_processing)} to process")
        self.tracks_copycount_label.setText(f"{self.stats.num_processing} tracks to process")

    def start_processing(self):
        # Check if all necessary fields are (probably) filled out
        mp3_target_directory = self.mp3_path_lineedit.text()
        data_directory = self.data_path_lineedit.text()
        bpstat_prefix = self.bpstat_path_lineedit.text()

        if not(mp3_target_directory and data_directory and bpstat_prefix and self.lib):
            bpsynctools.show_error_window("Missing required fields!",
                              "Please make sure you've loaded an XML and set everything under Options.",
                              "Required fields missing")
            return

        # Data processing
        # Get track IDs of selected items by iterating over table widget's model data
        data = self.table_widget.table_model.array_data
        selected_ids_processing = []
        selected_ids_tracking = []
        ignored_ids_tracking = []
        for row in data:
            if row[1]:  # Check for mp3 processing
                selected_ids_processing.append(row[0])

            if row[2]:  # Check for db tracking
                selected_ids_tracking.append(row[0])
            else:
                # Add persistent ID to ignore list
                song = self.lib.songs[row[0]]
                ignored_ids_tracking.append(song.persistent_id)

        # Create progress bar for element processing (the longest operation)
        progress_window = bpsyncwidgets.ProgressWindow(len(selected_ids_processing))

        # Start processing thread
        song_worker = bpsyncwidgets.SongWorker(self.lib, selected_ids_processing, selected_ids_tracking, ignored_ids_tracking, mp3_target_directory, data_directory, bpstat_prefix)
        song_worker.signal_connection.songStartedProcessing.connect(lambda progress_val, song_string: progress_window.updateFields(progress_val, song_string))

        # Cancel thread availability
        progress_window.logger_connection.canceled.connect(lambda: song_worker.stop_thread())

        self.thread_manager.start(song_worker)

        progress_window.show()

class StandardSyncWindow(QtWidgets.QWidget, Ui_StandardSyncWindow):
    def __init__(self):
        super().__init__()

        # Init
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setupUi(self)

        # Window vars
        self.program_path = QtCore.QDir.currentPath()
        self.lib = None  # libpytunes Library object
        self.db_songs = None  # Array of StoredSong objects from querying database
        self.bpsongs = None # Array of BPSong objects.
        self.thread_manager = QtCore.QThreadPool()

        # TODO: whether the db is initialized or not IS NOT the window's responsibility to remember
        # add a value to models or something
        self.db_initialized = False  # Whether or not the database file has been loaded

        # Top-right statistics; all 0 at start.
        self.stats = bpsynctools.TableStatistics()

        # Prepopulate fields
        self.mp3_path_lineedit.setText('tmp')
        self.data_path_lineedit.setText('data')
        self.backup_path_lineedit.setText('backups')

        # Buttons
        self.xml_browse_button.clicked.connect(self.xml_open_prompt)
        self.bpstat_browse_button.clicked.connect(self.bpstat_open_prompt)
        self.database_browse_button.clicked.connect(self.database_open_prompt)
        self.load_all_button.clicked.connect(self.update_with_all)

        self.mp3_browse_button.clicked.connect(self.mp3_save_prompt)
        self.data_browse_button.clicked.connect(self.data_save_prompt)
        self.backup_browse_button.clicked.connect(self.backup_save_prompt)

        self.show_ignored_songs_button.clicked.connect(self.open_ignored_songs_dialog)

        self.start_button.clicked.connect(self.start_processing)

        # Table functionality
        # Context menu
        self.songs_changed_table.customContextMenuRequested.connect(
            lambda pos: self.songs_changed_table.show_context_menu(pos, self.lib))
        self.songs_changed_table.context_menu_enabled = True
        self.new_songs_table.customContextMenuRequested.connect(
            lambda pos: self.new_songs_table.show_context_menu(pos, self.lib))
        self.new_songs_table.context_menu_enabled = True

        # Song library change updates (edits to self.lib)
        self.songs_changed_table.songChanged.connect(self.update_song_in_songs_changed_table)
        self.new_songs_table.songChanged.connect(self.update_song_in_new_songs_table)

        self.songs_changed_lineedit.textChanged.connect(lambda text: self.songs_changed_table.proxy.set_filter_text(text))
        self.new_songs_lineedit.textChanged.connect(lambda text: self.new_songs_table.proxy.set_filter_text(text))        

        # Synced songs table
        # In order: column headers, starting data, checkbox columns, columns to filter on with lineedit
        headers_delta = ["Track ID", "Reprocess?", "Title", "Artist", "Album", "Base plays", "XML plays", "BP plays", "Delta", "New playcount", "Persistent ID"]
        data_delta = [[2, 1, "Call My Name Feat. Yukacco", "mameyudoufu", "「FÜGENE2」", 25, 38, 42, "+30", 55, "DEAE900B9933338C"]]
        box_columns_delta = [1] # Processing column = 1
        filter_on_delta = [1, 3, 4, 10]

        column_sizes_delta = [50, 120, 200, 120, 120, 80, 80, 80, 80, 100, 200]

        self.songs_changed_table.setup(headers_delta, box_columns_delta, filter_on_delta)
        self.songs_changed_table.set_data(data_delta)
        self.songs_changed_table.set_column_widths(column_sizes_delta)

        # New songs table
        headers = ["Track ID", "Process?", "Track?", "Title", "Artist", "Album", "Plays", "Trimmed?", "Volume%", "Filepath"]
        data = [[1, 1, 1, "YU.ME.NO !", "ユメガタリ(ミツキヨ , shnva)", " ユメの喫茶店", 24, "No", "100%", "D:/Music/a.mp3"]]
        box_columns = [1, 2] # Processing column = 1, tracking column = 2
        filter_on = [3, 4, 5]

        column_sizes = [50, 100, 100, 200, 120, 120, 50, 100, 50, 200]

        self.new_songs_table.setup(headers, box_columns, filter_on)
        self.new_songs_table.set_data(data)
        self.new_songs_table.set_column_widths(column_sizes)

        # Enable updates from checkbox
        # Note that this breaks if the underlying table model is changed (which shouldn't change)
        self.new_songs_table.table_model.dataChanged.connect(lambda idx: self.update_stats_from_index(idx, self.new_songs_table))
        self.songs_changed_table.table_model.dataChanged.connect(lambda idx: self.update_stats_from_index(idx, self.songs_changed_table))
    
    def open_ignored_songs_dialog(self):
        # whose responsibility is it to keep track of this?
        if not self.db_initialized:
            bpsynctools.show_error_window("Database not available!", 
                              "Have you loaded in a .db file yet?",
                              "Database not available!")
            return

        with models.Session() as session:
            ignored_songs = session.query(models.IgnoredSong).all()

        if not ignored_songs:
            bpsynctools.show_error_window("No ignored songs found!",
                              "There were no ignored songs in the database file. Ignored songs only appear if you explicitly choose not to track a song in your library.",
                              "No ignored songs found!")
            return

        window = IgnoredSongsDialog(self, ignored_songs)
        window.show()

    def xml_open_prompt(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open XML", self.program_path,
                "XML (*.xml);;All Files (*)")
        if file_name:
            self.xml_path_lineedit.setText(file_name)

    def bpstat_open_prompt(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open .bpstat", self.program_path,
                "Blackplayer statistics file (*.bpstat);;All Files (*)")
        if file_name:
            self.bpstat_path_lineedit.setText(file_name)

    def database_open_prompt(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open .bpstat", self.program_path,
                "bpsync database file (*.db);;All Files (*)")
        if file_name:
            self.database_path_lineedit.setText(file_name)

    def mp3_save_prompt(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self,
                "Select processed mp3 directory", self.program_path)
        if directory:
            self.mp3_path_lineedit.setText(directory)

    def data_save_prompt(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self,
                "Select data directory", self.program_path)
        if directory:
            self.data_path_lineedit.setText(directory)

    def backup_save_prompt(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self,
                "Select backup directory", self.program_path)
        if directory:
            self.backup_path_lineedit.setText(directory)

    def update_with_all(self):
        # get contents of lineedits
        xml_path = self.xml_path_lineedit.text()
        bpstat_path = self.bpstat_path_lineedit.text()
        database_path = self.database_path_lineedit.text()

        if not xml_path or not bpstat_path or not database_path:
            bpsynctools.show_error_window("Please make sure you've entered all paths!",
                              "You can do this by manually entering the path or selecting each path by clicking Browse.",
                              "Paths not defined")
            return

        # call helper function for getting data from files
        # this function raises error windows on its end
        file_data = bpsynctools.get_std_data(xml_path, bpstat_path, database_path)
        if file_data:
            self.lib, self.bpsongs, self.db_songs = file_data
        else:
            # return early
            return

        # call helper function
        existing_data, new_data = bpsynctools.standard_sync_arrays_from_data(self.lib, self.bpsongs)

        self.songs_changed_table.set_data(existing_data)
        self.new_songs_table.set_data(new_data)

        # Mark database as ready
        self.db_initialized = True

        # Generate initial statistics (overwrites current object)
        # These have to be generated on a per-table basis
        songs_changed_stats = bpsynctools.get_statistics(self.songs_changed_table.table_model.array_data, self.lib, None, 1)
        songs_new_stats = bpsynctools.get_statistics(self.new_songs_table.table_model.array_data, self.lib, 2, 1)
        self.stats = songs_changed_stats + songs_new_stats
        
        # Update stat labels
        self.update_statistics_labels()

    def update_song_in_songs_changed_table(self, song):
        """
        Called when a Song object in self.lib is modified by any means.

        It is this window's responsibility to know how to handle the change
        of a song object in the underlying library.
        """
        # Search for equivalent row in the underlying data
        # Linear is good enough
        data = self.songs_changed_table.table_model.array_data
        target_index = -1
        for index, row in enumerate(data):
            if row[0] == song.track_id:
                target_index = index
                break

        if target_index == -1:
            logger.error(f"Tried looking up {song.track_id} in the model, but it wasn't there?")
            return

        # Generate a "fake" first_sync_array from the song
        temp_lib = {song.track_id: song}
        new_data = bpsynctools.first_sync_array_from_libpysongs(temp_lib)

        # Update row in data
        data[target_index] = new_data[0]

        # Tell the model to update
        # inefficient call?
        self.songs_changed_table.set_data(data)

    def update_song_in_new_songs_table(self, song):
        """
        Called when a Song object in self.lib is modified by any means.

        It is this window's responsibility to know how to handle the change
        of a song object in the underlying library.
        """
        # Search for equivalent row in the underlying data
        # Linear is good enough
        data = self.new_songs_table.table_model.array_data
        target_index = -1
        for index, row in enumerate(data):
            if row[0] == song.track_id:
                target_index = index
                break

        if target_index == -1:
            logger.error(f"Tried looking up {song.track_id} in the model, but it wasn't there?")
            return

        # Generate a "fake" first_sync_array from the song
        temp_lib = {song.track_id: song}
        _, new_data = bpsynctools.standard_sync_array_from_data(temp_lib, self.bpsongs)

        # Update row in data
        data[target_index] = new_data[0]

        # Tell the model to update
        # inefficient call?
        self.new_songs_table.set_data(data)

    def update_stats_from_index(self, index, table):
        """
        Update the top-right statistics from a checkbox tick/untick.
        """
        # Check if library has been loaded; else, ignore
        if not self.lib:
            return

        # Check if the index's column is in one of the checkbox columns; else, ignore
        if index.column() not in table.table_model.checkbox_columns:
            return
        
        # Get track ID in the same row as the index in column 0
        # Signature: createIndex(row, column, ptr)
        # ptr is quite interesting: https://doc.qt.io/qtforpython/PySide6/QtCore/QAbstractItemModel.html#PySide6.QtCore.PySide6.QtCore.QAbstractItemModel.createIndex
        track_id_index = table.table_model.createIndex(index.row(), 0, table)
        track_id = table.table_model.data(track_id_index, QtCore.Qt.DisplayRole)

        # Look it up in the library
        try:
            song = self.lib.songs[track_id]
        except KeyError:
            # If it doesn't exist (somehow), exit early
            logger.error(f"Couldn't find {track_id} when updating statistics?")
            return

        # Either increment or decrement counters as needed
        # It's the case that processing is always in column index 1,
        # and tracking is always in column index 2. This is hardcoded
        # because I don't expect this to change anytime soon.

        # Get new state of checkbox and update stats accordingly
        new_state = table.table_model.data(index, QtCore.Qt.DisplayRole)
        if index.column() == 1:
            if new_state == True:
                self.stats.num_processing += 1
                self.stats.size_processing += song.size                
            else:
                self.stats.num_processing -= 1
                self.stats.size_processing -= song.size
        elif index.column() == 2:
            if new_state == True:
                self.stats.num_tracking += 1      
            else:
                self.stats.num_tracking -= 1
        else:
            logger.error(f"Tried looking up column {index.column()} for statistics updates?")

        # Update statistics labels
        self.update_statistics_labels()
    
    def update_statistics_labels(self):
        """
        Update labels from self.stats. 
        
        Call after the XML has been loaded or a checkbox state has changed.
        """
        # Check if lib.songs loaded; else, refuse.
        if not self.lib:
            logger.error(f"Tried to update statistics when the table wasn't ready yet?")
            return
        
        # len() is constant time in CPython.
        num_tracks = len(self.lib.songs)
        num_songs_in_db = len(self.db_songs)

        # Update all labels.
        self.tracks_found_label.setText(f"{num_tracks} tracks found")
        self.tracks_totalsize_label.setText(f"{bpsynctools.humanbytes(self.stats.total_size)} total size")
        self.tracks_indatabase_label.setText(f"{num_songs_in_db} songs currently being tracked")
        self.tracks_synccount_label.setText(f"{self.stats.num_tracking} songs to track")
        self.tracks_copysize_label.setText(f"{bpsynctools.humanbytes(self.stats.size_processing)} to process")
        self.tracks_copycount_label.setText(f"{self.stats.num_processing} tracks to process")

    def start_processing(self):
        # Get all backup paths, store into array
        xml_path = self.xml_path_lineedit.text()
        bpstat_path = self.bpstat_path_lineedit.text()
        database_path = self.database_path_lineedit.text()
        backup_paths = [xml_path, bpstat_path, database_path]

        # Check if all necessary fields are (probably) filled out
        mp3_target_directory = self.mp3_path_lineedit.text()
        data_directory = self.data_path_lineedit.text()
        backup_directory = self.backup_path_lineedit.text()

        if not(mp3_target_directory and data_directory and backup_directory and self.lib):
            bpsynctools.show_error_window("Missing required fields!",
                              "Please make sure you've loaded an XML and set everything under Options.",
                              "Required fields missing")
            return

        # Calculate bpstat prefix
        bpstat_prefix = self.bpsongs[0].get_bpstat_prefix()

        # Get track IDs of selected items for processing/tracking by iterating over table widget's model data
        new_data = self.new_songs_table.table_model.array_data
        selected_ids_processing = []
        selected_ids_tracking = []
        for row in new_data:
            if row[1]:  # Check for mp3 processing
                selected_ids_processing.append(row[0])
            if row[2]:  # Check for db tracking
                selected_ids_tracking.append(row[0])

        # Create progress bar for element processing (the longest operation)
        progress_window = bpsyncwidgets.ProgressWindow(len(selected_ids_processing))
        progress_window.show()

        # Start processing thread
        song_worker = bpsyncwidgets.StandardWorker(self.lib, selected_ids_processing, selected_ids_tracking,
                                                    mp3_target_directory, data_directory, bpstat_prefix, backup_directory, backup_paths,
                                                    self.songs_changed_table.table_model.array_data)
        song_worker.signal_connection.songStartedProcessing.connect(lambda progress_val, song_string: progress_window.updateFields(progress_val, song_string))

        # Cancel thread availability
        progress_window.logger_connection.canceled.connect(lambda: song_worker.stop_thread())

        self.thread_manager.start(song_worker)

class IgnoredSongsDialog(QtWidgets.QDialog, Ui_IgnoredSongsDialog):
    def __init__(self, parent, ignored_songs):
        """
        Set up everything related to the IgnoredSongsDialog.

        :param parent: The parent window of this widget.
        :param ignored_songs: The result of performing a query for all
            IgnoredSong objects in the database.
        """
        super().__init__(parent)

        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setupUi(self)
        
        self.ignored_songs = ignored_songs

        self.setup_ignored_songs_table()

    def setup_ignored_songs_table(self):
        # create dict for bpstat songs, by persistent id
        # take this information from the libpytunes Library object in the parent class
        libsongs = {}
        for song in self.parent().lib.songs.values():
            libsongs[song.persistent_id] = song

        # The current songs present in the new songs table. Prevents songs from being added twice through this dialog
        # into the new songs table.
        current_data = self.parent().new_songs_table.table_model.array_data
        existing_track_ids = [row[0] for row in current_data]

        # Generate data
        data = []
        
        for ignored_song in self.ignored_songs:
            # get associated libpytunes Song object from its ID
            try:
                song = libsongs[ignored_song.persistent_id]
            except KeyError:
                logger.info(f"Failed to look up {ignored_song.persistent_id} when building the IgnoredSongsDialog table, was it deleted?")
                continue

            # Check if it is already in the new songs table (which is, unfortunately, a linear search)
            if song.track_id not in existing_track_ids:
                # get all the needed data, mark its tracking box as off by default
                data.append([song.track_id, 0, song.name, song.artist, song.album, song.play_count, song.location])

        # Static table information
        headers = ["Track ID", "Track?", "Title", "Artist", "Album", "Plays", "Filepath"]
        box_columns = [1]
        filter_on = [2, 3, 4]

        column_sizes = [50, 80, 200, 120, 120, 50, 200]

        self.ignored_song_table.setup(headers, data, box_columns, filter_on)
        self.ignored_song_table.set_column_widths(column_sizes)

    def accept(self):
        """
        On dialog accept (OK button is clicked).
        """
        # Get the persistent IDs of the new songs to add
        unignored_songs = {}  # A 2D array.

        table_data = self.ignored_song_table.table_model.array_data
        for row in table_data:
            if row[1]:  # If "Track?" box checked
                # Note that the parent's library should be an unmodified libpytunes Library
                # object, which has its keys as the track ID (and not persistent ID)
                unignored_songs[row[0]] = self.parent().lib.songs[row[0]]

        # Generate the 2D array containing the data needed
        new_data = bpsynctools.first_sync_array_from_libpysongs(unignored_songs)

        # Get the parent's table's underlying model data for the new songs table
        current_data = self.parent().new_songs_table.table_model.array_data

        # Append to this underlying model data
        # note: [[1, 2], [3, 4]] + [[5, 6], [7, 8]] = [[1, 2], [3, 4], [5, 6], [7, 8]]
        current_data += new_data

        # Update the table with this new data
        self.parent().new_songs_table.set_data(current_data)
        
        # Call super
        super().accept()

class ExportImportWindow(QtWidgets.QWidget, Ui_ExportImportWindow):
    def __init__(self):
        """
        Set up the ExportImportWindow.
        """
        super().__init__()

        self.lib = None
        self.program_path = QtCore.QDir.currentPath()

        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setupUi(self)
        
        # Input filepath
        self.xml_browse_button.clicked.connect(self.xml_open_prompt)
        self.xml_load_button.clicked.connect(self.update_with_xml)

        # Accept/reject buttons
        self.saveButton.clicked.connect(self.start_processing)
        self.cancelButton.clicked.connect(lambda: self.close())

    def xml_open_prompt(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open XML", self.program_path,
                "XML (*.xml);;All Files (*)")
        if file_name:
            self.xml_path_lineedit.setText(file_name)

    def update_with_xml(self):
        # get contents of lineedit
        xml_path = self.xml_path_lineedit.text()
        if not xml_path:
            bpsynctools.show_error_window("Please enter an XML path!",
                              "You can do this by manually entering the path or selecting it by clicking Browse.",
                              "No XML path defined")
            return
        # generate library from it
        try:
            self.lib = Library(xml_path)
        except xml.parsers.expat.ExpatError as e:
            bpsynctools.show_error_window("Invalid XML file!",
                              f"Couldn't parse XML file (if it is one) - {e}",
                              "Invalid XML file")
            return
        except FileNotFoundError:
            bpsynctools.show_error_window("File not found!",
                              "The entered path doesn't appear to exist.",
                              "Invalid XML filepath")
            return

        # update statistics counter
        self.songsLoadedLabel.setText(f"{len(self.lib.songs)} songs loaded")

        # enable buttonBox
        self.saveButton.setEnabled(True)

    def set_output_path(self):
        path = QtWidgets.QFileDialog.getSaveFileName(self,
                "Save ExportImport file as...", self.program_path,
                "Text file (*.txt);;All Files (*)")
        if path:
            self.save_path_lineedit.setText(path)

    def start_processing(self):
        """
        On dialog accept ("Save" button is clicked).

        After asserting that the necessary inputs exist, this function
        searches the widget for all the available checkboxes. The widget
        has been designed such that the checkboxes have similar names
        to their corresponding labels, which have the exact text required
        for the add_to_exportimport function.
        """
        # Assert library exists
        if not self.lib:
            bpsynctools.show_error_window("No library loaded!",
                                          "The underlying library doesn't have anything - did you load an XML?",
                                          "No library loaded")
            # This really shouldn't be possible anyways
            logger.error("Got accept() even though the buttonBox is disabled?")
            return

        # Have user specify the save path
        # If they cancel and no path is returned, return early
        output_path, _ = QtWidgets.QFileDialog.getSaveFileName(self,
                "Save ExportImport file as...", self.program_path,
                "Text file (*.txt);;All Files (*)")
        if not output_path:
            # Same as just cancelling the save operation
            return

        # Gather all ticked checkboxes
        checkboxes = self.findChildren(QtWidgets.QCheckBox)
        checked_checkbox_names = []
        for checkbox in checkboxes:
            if checkbox.isChecked():
                checked_checkbox_names.append(checkbox.objectName())
                
        # Get the names of all associated labels by replacing "CheckBox" with "Label"
        label_names = [obj_name.replace("CheckBox", "Label") for obj_name in checked_checkbox_names]

        # For each label, get its actual containing text
        tags = []
        for label_name in label_names:
            label = getattr(self, label_name) # (should) return QLabel object
            tags.append(label.text())

        # Pass into add_to_exportimport, raise error otherwise 
        try:
            bpsynctools.add_to_exportimport(self.lib, tags, output_path)

            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.NoIcon)
            msg.setText("Processing complete. Check the results for accuracy.")
            msg.setWindowTitle("ExportImport file complete")
            msg.exec()
        except Exception as e:
            bpsynctools.show_error_window("Something went wrong while generating the ExportImport file!",
                    str(e),
                    "Processing error")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainMenuWindow()
    window.show()

    # Start the event loop.
    app.exec()


'''
if __name__ == "__main__":
    lib = Library('iTunes_Music_Library.xml')
    
    bpstat_name = datetime.now().strftime("%Y-%m-%d %H-%M-%S (new).bpstat")
    bpstat_path = os.path.join(DATA_FOLDER, bpstat_name)

    os.makedirs(DATA_FOLDER, exist_ok=True)
    os.makedirs(SONGS_FOLDER, exist_ok=True)
    # bpstat generation and processing can happen at the same time
    for _, song in lib.songs.items():
        #bpsynctools.copy_and_process_song(song)
        bpsynctools.add_to_bpstat(song, TARGET_FOLDER, bpstat_path)

    # Create database with new songs
    song_arr = [song for _, song in lib.songs.items()]
    models.create_db()
    models.add_libpy_songs(song_arr)

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
'''