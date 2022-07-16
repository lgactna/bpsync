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
from PySide6 import QtWidgets, QtCore, QtGui



class MainMenuWindow(QtWidgets.QWidget, Ui_MainMenuWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.launch_first_button.clicked.connect(self.open_first_sync)
        self.launch_std_button.clicked.connect(self.open_std_sync)
        self.launch_bpstat_button.clicked.connect(self.open_bpstat_converter)
        self.launch_m3u_button.clicked.connect(self.open_m3u_generator)

    def open_first_sync(self):
        window = FirstTimeWindow()
        window.show()

    def open_std_sync(self):
        window = StandardSyncWindow()
        window.show()

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
        headers = ["Track ID", "Copy?", "Track?", "Title", "Artist", "Album", "Plays", "Trimmed?", "Volume%", "Filepath"]
        data = [[1, 1, 1, "YU.ME.NO !", "ユメガタリ(ミツキヨ , shnva)", " ユメの喫茶店", 24, "No", "100%", "D:/Music/a.mp3"]]
        box_columns = [1, 2]
        filter_on = [3, 4, 5]

        column_sizes = [50, 80, 80, 200, 120, 120, 50, 100, 50, 200]

        ## Set up initial table contents and formatting
        self.table_widget.setup(headers, data, box_columns, filter_on)
        self.table_widget.set_column_widths(column_sizes)

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

        # TODO: Calculate top-right statistics
        # There's two parts to this: calculating the inital set of statistics, probably in a separate function,
        # and maintaing the state of the statistics. The simplest way is to connect to each underlying
        # table model's dataChanged signal, then get its row value and use that directly against
        # the table model's data() function (or construct a new index with column 0, the track ID).
        # This does require many calls when a checkbox header is clicked, but this isn't that high of an
        # overhead.
        #
        # Also, check to make sure that the newly-updated index is in the "processing" column, 
        # otherwise there's no need to update (unless we're also keeping track of the number of 
        # tracked songs).

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

        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setupUi(self)

        self.program_path = QtCore.QDir.currentPath()
        self.lib = None  # libpytunes Library object
        self.db_songs = None  # Array of StoredSong objects from querying database
        self.bpsongs = None # Array of BPSong objects.
        self.thread_manager = QtCore.QThreadPool()

        self.db_initialized = False  # Whether or not the database file has been loaded

        # Prepopulate fields
        self.mp3_path_lineedit.setText('tmp')
        self.data_path_lineedit.setText('data')
        self.backup_path_lineedit.setText('backups')

        # Signals and slots
        ## Buttons
        self.xml_browse_button.clicked.connect(self.xml_open_prompt)
        self.bpstat_browse_button.clicked.connect(self.bpstat_open_prompt)
        self.database_browse_button.clicked.connect(self.database_open_prompt)
        self.load_all_button.clicked.connect(self.update_with_all)

        self.mp3_browse_button.clicked.connect(self.mp3_save_prompt)
        self.data_browse_button.clicked.connect(self.data_save_prompt)
        self.backup_browse_button.clicked.connect(self.backup_save_prompt)

        self.show_ignored_songs_button.clicked.connect(self.open_ignored_songs_dialog)

        self.start_button.clicked.connect(self.start_processing)

        ## Table functionality
        self.songs_changed_table.customContextMenuRequested.connect(
            lambda pos: self.songs_changed_table.show_context_menu(pos, self.lib))
        self.songs_changed_table.context_menu_enabled = True
        self.new_songs_table.customContextMenuRequested.connect(
            lambda pos: self.new_songs_table.show_context_menu(pos, self.lib))
        self.new_songs_table.context_menu_enabled = True
        self.songs_changed_table.songChanged.connect(self.update_song_in_songs_changed_table)
        self.new_songs_table.songChanged.connect(self.update_song_in_new_songs_table)

        self.songs_changed_lineedit.textChanged.connect(lambda text: self.songs_changed_table.proxy.set_filter_text(text))
        self.new_songs_lineedit.textChanged.connect(lambda text: self.new_songs_table.proxy.set_filter_text(text))

        # Synced songs table
        ## In order: column headers, starting data, checkbox columns, columns to filter on with lineedit
        headers_delta = ["Track ID", "Reprocess", "Title", "Artist", "Album", "Base plays", "XML plays", "BP plays", "Delta", "New playcount", "Persistent ID"]
        data_delta = [[2, 1, "Call My Name Feat. Yukacco", "mameyudoufu", "「FÜGENE2」", 25, 38, 42, "+30", 55, "DEAE900B9933338C"]]
        box_columns_delta = [1]
        filter_on_delta = [1, 3, 4, 10]

        column_sizes_delta = [50, 100, 200, 120, 120, 80, 80, 80, 80, 100, 200]

        self.songs_changed_table.setup(headers_delta, data_delta, box_columns_delta, filter_on_delta)
        self.songs_changed_table.set_column_widths(column_sizes_delta)

        # New songs table
        headers = ["Track ID", "Copy?", "Track?", "Title", "Artist", "Album", "Plays", "Trimmed?", "Volume%", "Filepath"]
        data = [[1, 1, 1, "YU.ME.NO !", "ユメガタリ(ミツキヨ , shnva)", " ユメの喫茶店", 24, "No", "100%", "D:/Music/a.mp3"]]
        box_columns = [1, 2]
        filter_on = [3, 4, 5]

        column_sizes = [50, 80, 80, 200, 120, 120, 50, 100, 50, 200]

        self.new_songs_table.setup(headers, data, box_columns, filter_on)
        self.new_songs_table.set_column_widths(column_sizes)
    
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

        # Check if filepaths are valid - validation done here for direct access to error window
        # TODO: Custom exception class, move out of this UI function
        # try generating the libpytunes library from specified XML
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

        ## try generating bpstat library
        self.bpsongs = bpparse.get_songs(bpstat_path)
        if not self.bpsongs:
            bpsynctools.show_error_window(".bpstat malformed!",
                                "The program wasn't able to find any valid songs in this file.",
                                "Invalid .bpstat file")
            return

        ## try getting elements from db
        try:
            models.initialize_engine(database_path)
        except Exception as e:
            bpsynctools.show_error_window("Something went wrong while connecting to the database!",
                               str(e),
                               "Database error")
            return
        with models.Session() as session:
            self.db_songs = session.query(models.StoredSong).all()
        if not self.db_songs:
            bpsynctools.show_error_window("No songs in database!",
                       "A database query yielded no results.",
                       "Database error")
            return

        # call helper function
        existing_data, new_data = bpsynctools.standard_sync_arrays_from_data(self.lib, self.bpsongs)

        self.songs_changed_table.set_data(existing_data)
        self.new_songs_table.set_data(new_data)

        # Mark database as ready
        self.db_initialized = True

        # TODO: Calculate top-right statistics

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
                # TODO: does it make sense to filter out already-tracked songs from the table here, or in StandardWorker?
                # i'd say the worker thread shouldn't need to have awareness of the conditions for adding a song
                # a simple fix is to just check the already-tracked songs table and see if this id exists
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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    #window = FirstTimeWindow()
    window = MainMenuWindow()
    window.show()

    # Start the event loop.
    app.exec()


'''
if __name__ == "__main__":
    lib = Library('iTunes_Music_Library.xml')
    # TODO: dict with key:value of persistent id:Song
    
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