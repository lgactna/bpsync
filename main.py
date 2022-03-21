import logging
import xml.parsers.expat
import sys

from libpytunes import Library

import bpsynctools
import bpsyncwidgets
import bpparse
import models

logger = logging.getLogger(__name__)

# dev constants - not used in program
LIBRARY = 'iTunes_Music_Library.xml'
DATA_FOLDER = 'data'
SONGS_FOLDER = 'tmp'

TARGET_FOLDER = '/storage/sdcard1/imported-music/'

from first_time import Ui_FirstTimeWindow
from std_sync import Ui_StandardSyncWindow
from progress import Ui_ProcessingProgress
from PySide6 import QtWidgets, QtCore, QtGui

def show_error_window(text, informative_text, title):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText(text)
    msg.setInformativeText(informative_text)
    msg.setWindowTitle(title)
    msg.exec()

class FirstTimeWindow(QtWidgets.QWidget, Ui_FirstTimeWindow):
    # TODO: right-click context menu with more information + volume edit
    # TODO: extended info screen
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
        ## Buttons
        self.xml_browse_button.clicked.connect(self.xml_open_prompt)
        self.xml_load_button.clicked.connect(self.update_with_xml)
        self.mp3_browse_button.clicked.connect(self.mp3_save_prompt)
        self.data_browse_button.clicked.connect(self.data_save_prompt)
        self.start_button.clicked.connect(self.start_processing)
        ## Table functionality
        self.table_filter_lineedit.textChanged.connect(lambda text: self.table_widget.proxy.set_filter_text(text))

        # Table
        ## In order: column headers, starting data, checkbox columns, columns to filter on with lineedit
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
            show_error_window("Please enter an XML path!", 
                              "You can do this by manually entering the path or selecting it by clicking Browse.", 
                              "No XML path defined")
            return
        # generate library from it
        try:
            self.lib = Library(xml_path)
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
        # update table from it
        data = bpsynctools.first_sync_array_from_libpysongs(self.lib.songs)
        self.table_widget.set_data(data)

        # TODO: Calculate top-right statistics

    def start_processing(self):
        # Check if all necessary fields are (probably) filled out
        mp3_target_directory = self.mp3_path_lineedit.text()
        data_directory = self.data_path_lineedit.text()
        bpstat_prefix = self.bpstat_path_lineedit.text()

        if not(mp3_target_directory and data_directory and bpstat_prefix and self.lib):
            show_error_window("Missing required fields!", 
                              "Please make sure you've loaded an XML and set everything under Options.", 
                              "Required fields missing")
            return
        
        # Oh boy
        # Get track IDs of selected items by iterating over table widget's model data
        data = self.table_widget.table_model.array_data
        selected_ids_processing = []
        selected_ids_tracking = []
        for row in data:
            if row[1]:  # Check for mp3 processing
                selected_ids_processing.append(row[0])
            if row[2]:  # Check for db tracking
                selected_ids_tracking.append(row[0])

        # Create progress bar for element processing (the longest operation)
        progress_window = bpsyncwidgets.ProgressWindow(len(selected_ids_processing))

        # Start processing thread
        # BUG: This does not kill the thread even if the windows are closed
        song_worker = bpsyncwidgets.SongWorker(self.lib, selected_ids_processing, selected_ids_tracking, mp3_target_directory, data_directory, bpstat_prefix)
        song_worker.signal_connection.songStartedProcessing.connect(lambda progress_val, song_string: progress_window.updateFields(progress_val, song_string))
        self.thread_manager.start(song_worker)

        progress_window.show()

class StandardSyncWindow(QtWidgets.QWidget, Ui_StandardSyncWindow):
    # TODO: right-click context menu with more information + volume edit
    # TODO: extended info screen
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

        self.start_button.clicked.connect(self.start_processing)

        ## Table functionality
        self.songs_changed_lineedit.textChanged.connect(lambda text: self.songs_changed_table.proxy.set_filter_text(text))
        self.new_songs_lineedit.textChanged.connect(lambda text: self.new_songs_table.proxy.set_filter_text(text))

        # Synced songs table
        ## In order: column headers, starting data, checkbox columns, columns to filter on with lineedit
        headers_delta = ["Track ID", "Title", "Artist", "Album", "Base plays", "XML plays", "BP plays", "Delta", "New playcount", "Persistent ID"]
        data_delta = [[2, "Call My Name Feat. Yukacco", "mameyudoufu", "「FÜGENE2」", 25, 38, 42, "+30", 55, "DEAE900B9933338C"]]
        box_columns_delta = []
        filter_on_delta = [1, 2, 3, 9]

        column_sizes_delta = [50, 200, 120, 120, 80, 80, 80, 80, 100, 200]

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
            show_error_window("Please make sure you've entered all paths!", 
                              "You can do this by manually entering the path or selecting each path by clicking Browse.", 
                              "Paths not defined")
            return
        
        # Check if filepaths are valid - validation done here for direct access to error window
        # TODO: Custom exception class, move out of this UI function
        ## try generating libpytuneslibrary from specified XML
        try:
            library = Library(xml_path)
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

        # call helper function
        existing_data, new_data = bpsynctools.standard_sync_arrays_from_data(library, bpsongs, db_songs)

        self.songs_changed_table.set_data(existing_data)
        self.new_songs_table.set_data(new_data)

        # TODO: Calculate top-right statistics

    def start_processing(self):
        # Check if all necessary fields are (probably) filled out
        mp3_target_directory = self.mp3_path_lineedit.text()
        data_directory = self.data_path_lineedit.text()
        bpstat_prefix = self.bpstat_path_lineedit.text()

        if not(mp3_target_directory and data_directory and bpstat_prefix and self.lib):
            show_error_window("Missing required fields!", 
                              "Please make sure you've loaded an XML and set everything under Options.", 
                              "Required fields missing")
            return
        
        # Oh boy
        # Get track IDs of selected items by iterating over table widget's model data
        data = self.table_widget.table_model.array_data
        selected_ids_processing = []
        selected_ids_tracking = []
        for row in data:
            if row[1]:  # Check for mp3 processing
                selected_ids_processing.append(row[0])
            if row[2]:  # Check for db tracking
                selected_ids_tracking.append(row[0])

        # Create progress bar for element processing (the longest operation)
        progress_window = bpsyncwidgets.ProgressWindow(len(selected_ids_processing))

        # Start processing thread
        # BUG: This does not kill the thread even if the windows are closed
        song_worker = bpsyncwidgets.SongWorker(self.lib, selected_ids_processing, selected_ids_tracking, mp3_target_directory, data_directory, bpstat_prefix)
        song_worker.signal_connection.songStartedProcessing.connect(lambda progress_val, song_string: progress_window.updateFields(progress_val, song_string))
        self.thread_manager.start(song_worker)

        progress_window.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    #window = FirstTimeWindow()
    window = StandardSyncWindow()
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