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
#       - Calculating accessible files by filepath, flagging (but not removing) inaccessible songs
#       - Calculating files that need to be trimmed
#       - Strip ID3 of semicolons
#       - Create db
#       - Calculate deltas

from first_time import Ui_FirstTimeWindow
from PySide6 import QtWidgets, QtCore, QtGui
import sys

class FirstTimeWindow(QtWidgets.QWidget,Ui_FirstTimeWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowModality(QtCore.Qt.ApplicationModal) 
        self.setupUi(self)

        self.program_path = QtCore.QDir.currentPath()

        # Prepopulate fields
        self.mp3_path_lineedit.setText('/tmp')
        self.data_path_lineedit.setText('/data')

        # Signals and slots
        self.xml_browse_button.clicked.connect(self.xml_open_prompt)
        self.xml_load_button.clicked.connect(self.update_with_xml)
        self.mp3_browse_button.clicked.connect(self.mp3_save_prompt)
        self.data_browse_button.clicked.connect(self.data_save_prompt)

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
        xml_path = xml_path_lineedit.text()
        # generate library from it
        lib = Library(xml_path)
        # update table from it
        '''
        fields:
        - track ID
        - copy?
        - track for syncing?
        - title
        - artist
        - album
        - playcount
        - filepath
        - trimmed? y/n (x:xx.xxx - x:xx.xxx)
        '''

        #sample code
        self.sample_output_table.setColumnCount(0)
        self.sample_output_table.setRowCount(0)
        for header_index in range(0, len(data[0])):
            self.sample_output_table.insertColumn(header_index)
            self.sample_output_table.setHorizontalHeaderItem(header_index, QtWidgets.QTableWidgetItem(data[0][header_index]))
        for row_number in range(0, len(data[1])):
            self.sample_output_table.insertRow(row_number)
            for column_number in range(0, len(data[0])):
                self.sample_output_table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(data[1][row_number][column_number]))

app = QtWidgets.QApplication(sys.argv)

# Create a Qt widget, which will be our window.
window = FirstTimeWindow()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

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