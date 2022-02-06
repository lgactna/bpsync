import logging
import os
from datetime import datetime
import xml.parsers.expat

from libpytunes import Library
from pydub import AudioSegment
from pydub.utils import mediainfo
import eyed3

import bpparse
import models
import bpsynctools
import bpsyncwidgets

logger = logging.getLogger(__name__)

# dev constants

LIBRARY = 'iTunes_Music_Library.xml'
DATA_FOLDER = 'data'
SONGS_FOLDER = 'tmp'

TARGET_FOLDER = '/storage/sdcard1/imported-music/'

# TODO: Separate functions for each part of the process
#       - Calculating accessible files by filepath, flagging (but not removing) inaccessible songs
#       - Calculating files that need to be trimmed
#       - Strip ID3 of semicolons
#       - Create db
#       - Calculate deltas

from first_time import Ui_FirstTimeWindow
from PySide6 import QtWidgets, QtCore, QtGui
import sys

def show_error_window(text, informative_text, title):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText(text)
    msg.setInformativeText(informative_text)
    msg.setWindowTitle(title)
    msg.exec()

class Worker(QtCore.QRunnable):
    '''
    Worker thread

    :param args: Arguments to make available to the run code
    :param kwargs: Keywords arguments to make available to the run code

    '''

    def __init__(self, *args, **kwargs):
        super(Worker, self).__init__()
        self.args = args
        self.kwargs = kwargs

    @QtCore.Slot()  # QtCore.Slot
    def run(self):
        # https://www.pythonguis.com/tutorials/multithreading-pyside-applications-qthreadpool/
        lib, processing_ids, tracking_ids, mp3_target_directory, data_directory, bpstat_prefix = self.args

        bpstat_name = datetime.now().strftime("%Y-%m-%d %H-%M-%S (new).bpstat")
        bpstat_path = os.path.join(data_directory, bpstat_name)

        os.makedirs(data_directory, exist_ok=True)
        os.makedirs(mp3_target_directory, exist_ok=True)
        # bpstat generation and processing can happen at the same time
        song_arr = []

        index = 1
        max = len(lib.songs)
        for track_id, song in lib.songs.items():
            print(f"processing {song.name} ({index}/{max})")
            if track_id in processing_ids:
                bpsynctools.copy_and_process_song(song)
            if track_id in tracking_ids:
                bpsynctools.add_to_bpstat(song, bpstat_prefix, bpstat_path)
                song_arr.append(song)

        # Create database with new songs
        # TODO: Doesn't work - need to set up to be path-independent
        #models.set_engine(data_directory)
        models.create_db()
        models.add_libpy_songs(song_arr)

"""
class Worker(QtCore.QRunnable):
    '''
    Worker thread
    '''

    @QtCore.Slot()  # QtCore.Slot
    def run(self, pd, processing_ids, tracking_ids, mp3_target_directory, data_directory, bpstat_prefix):
        '''
        Your code goes in this function
        '''
        # this ought to go somewhere else?
        bpstat_name = datetime.now().strftime("%Y-%m-%d %H-%M-%S (new).bpstat")
        bpstat_path = os.path.join(data_directory, bpstat_name)

        os.makedirs(data_directory, exist_ok=True)
        os.makedirs(mp3_target_directory, exist_ok=True)
        # bpstat generation and processing can happen at the same time
        song_arr = []

        for track_id, song in self.lib.songs.items():
            if self.pd.wasCanceled():
                return

            if track_id in processing_ids:
                bpsynctools.copy_and_process_song(song)
                self.pd.setValue(self.pd.value()+1)
            if track_id in tracking_ids:
                bpsynctools.add_to_bpstat(song, bpstat_prefix, bpstat_path)
                song_arr.append(song)

        # Create database with new songs
        # TODO: Doesn't work - need to set up to be path-independent
        #models.set_engine(data_directory)
        models.create_db()
        models.add_libpy_songs(song_arr)
"""

class FirstTimeWindow(QtWidgets.QWidget,Ui_FirstTimeWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowModality(QtCore.Qt.ApplicationModal) 
        self.setupUi(self)

        self.program_path = QtCore.QDir.currentPath()
        self.lib = None  # libpytunes Library object
        self.thread_manager = QtCore.QThreadPool()

        # Prepopulate fields
        self.mp3_path_lineedit.setText('/tmp')
        self.data_path_lineedit.setText('/data')

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
        data = bpsynctools.first_sync_array_from_lib(self.lib)
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
        # https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QProgressDialog.html#PySide2.QtWidgets.PySide2.QtWidgets.QProgressDialog.setLabel
        # TODO: doesn't work with threading as expected
        # TODO: tracking only doesn't work as expected - maybe just use full library?
        
        #self.pd = QtWidgets.QProgressDialog("Processing/copying songs.", "Cancel", 0, len(selected_ids_processing))
        #self.pd.setWindowModality(QtCore.Qt.WindowModal)

        # Start processing thread
        # TODO: tidy up
        worker = Worker(self.lib, selected_ids_processing, selected_ids_tracking, mp3_target_directory, data_directory, bpstat_prefix)
        self.thread_manager.start(worker)

    '''
    def full_processing(self, processing_ids, tracking_ids, mp3_target_directory, data_directory, bpstat_prefix):
        # this ought to go somewhere else?
        bpstat_name = datetime.now().strftime("%Y-%m-%d %H-%M-%S (new).bpstat")
        bpstat_path = os.path.join(data_directory, bpstat_name)

        os.makedirs(data_directory, exist_ok=True)
        os.makedirs(mp3_target_directory, exist_ok=True)
        # bpstat generation and processing can happen at the same time
        song_arr = []

        for track_id, song in self.lib.songs.items():
            if self.pd.wasCanceled():
                return

            if track_id in processing_ids:
                bpsynctools.copy_and_process_song(song)
                self.pd.setValue(self.pd.value()+1)
            if track_id in tracking_ids:
                bpsynctools.add_to_bpstat(song, bpstat_prefix, bpstat_path)
                song_arr.append(song)

        # Create database with new songs
        # TODO: Doesn't work - need to set up to be path-independent
        #models.set_engine(data_directory)
        models.create_db()
        models.add_libpy_songs(song_arr)
    '''

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = FirstTimeWindow()
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