"""
Definitions for all custom Qt objects used in this project.
"""
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from PySide6 import QtCore, QtWidgets

import os
from datetime import datetime
import time
import logging

from pydub import AudioSegment
from pydub.utils import mediainfo
import eyed3

import bpsynctools
import bpparse
import models

from progress import Ui_ProcessingProgress

# region SongView
class CheckBoxDelegate(QtWidgets.QItemDelegate):
    """
    A delegate that places a checkbox in the cells of the column to which it's applied.

    From https://stackoverflow.com/questions/17748546/pyqt-column-of-checkboxes-in-a-qtableview
    """

    def __init__(self, parent):
        QtWidgets.QItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        """
        Important, otherwise an editor is created if the user clicks in this cell.
        """
        return None

    def paint(self, painter, option, index):
        """
        Paint a checkbox without the label.
        """
        self.drawBackground(painter, option, index)  # Draws the background for row-based selection
        self.drawCheck(painter, option, option.rect,
                       QtCore.Qt.Unchecked if int(index.data()) == 0 else QtCore.Qt.Checked)

    def editorEvent(self, event, model, option, index):
        """
        Change the data in the model and the state of the checkbox
        if the user presses the left mousebutton and this cell is editable. Otherwise do nothing.
        """
        if not int(index.flags() & QtCore.Qt.ItemIsEditable) > 0:
            return False
        if event.type() == QtCore.QEvent.Type.MouseButtonRelease and event.button() == Qt.MouseButton.LeftButton:
            # Change the checkbox-state
            self.setModelData(None, model, index)
            return True
        return False

    def setModelData(self, editor, model, index):
        """
        Invert checkbox on click.

        Affects proxy:
        https://forum.qt.io/topic/121874/how-to-access-source-model-methods-from-proxy-model,
        https://doc.qt.io/qt-5/qabstractproxymodel.html#mapToSource
        """
        # `index` returns the index relative to the proxy, which must be remapped to the source
        source_index = self.parent().proxy.mapToSource(index)
        check_state = self.parent().table_model.data(source_index, Qt.DisplayRole)
        check_state = 0 if check_state else 1  # Invert 1 -> 0 or 0 -> 1

        self.parent().table_model.setData(source_index, check_state, Qt.EditRole)


class CheckBoxHeader(QtWidgets.QHeaderView):
    # https://stackoverflow.com/questions/2970312/pyqt4-qtcore-pyqtsignal-object-has-no-attribute-connect
    # custom signals must be class variables, not attribute variables
    # Slot: logicalIndex, new_check_state (as int)
    checkBoxClicked = QtCore.Signal(int, int)

    # adapted from https://stackoverflow.com/questions/21557913/checkbox-in-a-header-cell-in-qtableview
    def __init__(self, orientation, checkbox_columns, parent):
        """
        Initialize table header with support for checkbox column headers.

        :param orientation: Orientation of the header (vertical, horizontal)
        :param checkbox_columns: List with column indexes to apply checkboxes to as the key. Default value of checkbox is True.
        :param parent: Parent widget.
        """
        QtWidgets.QHeaderView.__init__(self, orientation, parent)
        # super(CheckBoxHeader, self).__init__(orientation)
        # TODO: improve clarity of this variable/design
        self.checkbox_columns = {}
        for index in checkbox_columns:
            self.checkbox_columns[index] = True

        # Fixes sorting/clicking on the header items not working
        # https://stackoverflow.com/questions/18777554/why-wont-my-custom-qheaderview-allow-sorting
        self.setSectionsClickable(True)

        # TODO: setup function to define checkbox column headers
        # TODO: function in model to toggle all VISIBLE rows
        # TODO: function from proxy to return visible rows that can 

    def paintSection(self, painter, rect, logicalIndex):
        # Draw the original section headers
        painter.save()
        super().paintSection(painter, rect, logicalIndex)
        painter.restore()

        # Draw the checkbox
        # see https://doc.qt.io/qt-5/qheaderview.html#sectionViewportPosition
        
        if logicalIndex in self.checkbox_columns:
            x_start_pos = self.sectionViewportPosition(logicalIndex)

            option = QStyleOptionButton()
            option.rect = QRect(x_start_pos + 1, 3, 20, 20)
            option.state = QStyle.State_Enabled | QStyle.State_Active

            if self.checkbox_columns[logicalIndex]:
                option.state |= QStyle.State_On
            else:
                option.state |= QStyle.State_Off

            self.style().drawPrimitive(QStyle.PE_IndicatorCheckBox, option, painter)

    def mousePressEvent(self, event):
        # Below is not necessary due to super() call, kept for reference
        # Likely need to implement manual sorting, as well as manual tracking of checkbox positions
        # i.e. use sortByColumn: https://doc.qt.io/qt-5/qtableview.html#sortByColumn
        # https://stackoverflow.com/questions/26775577/hidden-sort-indicator-on-column-in-qtreeview

        # Figure out if any of the column checkboxes were clicked, act if necessary
        for column_index in self.checkbox_columns:
            x_start_pos = self.sectionViewportPosition(column_index)
            rect = QRect(x_start_pos + 1, 3, 20, 20)

            click_point = event.position().toPoint()

            # contains() only supports integer QPoints, not floating-point QPointF
            if rect.contains(click_point):
                self.setIsChecked(column_index, not self.checkbox_columns[column_index]) # TODO: 1 is placeholder number
                self.checkBoxClicked.emit(column_index, self.checkbox_columns[column_index])  # Tell parent about new state in column
                return
    
        # If click event wasn't in a column checkbox:
        # Do the rest of the normal behavior of a mousePressEvent(), like sorting
        super().mousePressEvent(event)

    def redrawCheckBoxes(self):
        self.viewport().update()

    def setIsChecked(self, column_index, val):
        if self.checkbox_columns[column_index] != val:
            self.checkbox_columns[column_index] = val
            self.redrawCheckBoxes()


class SortFilterProxyModel(QSortFilterProxyModel):
    """
    Proxy used to perform filtering and sorting without affecting the underlying data.

    Expects the parent (SongView) to have the filter_on array.
    """

    def __init__(self, *args, **kwargs):
        QSortFilterProxyModel.__init__(self, *args, **kwargs)
        # Enabling DynamicSortFilter means that editing a checkbox instantly resorts, which is jarring to the user
        self.setDynamicSortFilter(False)

    def filterAcceptsRow(self, source_row, source_parent):
        """
        Filters rows based on filterRegularExpression.

        Intended signal is a textChanged from a LineEdit like so:
        `self.LineEdit.textChanged.connect(lambda text: TableView.proxy.set_filter_text(text))`
        """
        # The proxy's current regular expression filter
        regex = self.filterRegularExpression()

        # Iterate over all columns selected for filtering
        filter_columns = self.parent().filter_columns
        for column_index in filter_columns:
            index = self.sourceModel().index(source_row, column_index, source_parent)
            if index.isValid():
                text = str(self.sourceModel().data(index, Qt.DisplayRole))
                if regex.match(text).hasMatch():
                    return True
        return False

    def set_filter_text(self, text):
        reg_exp = QtCore.QRegularExpression(text,QtCore.QRegularExpression.CaseInsensitiveOption)
        # This implicitly runs FilterAcceptsRow()
        self.setFilterRegularExpression(reg_exp)
        # Fixes proxy not maintaining sorting after unfiltering
        self.sort(self.sortColumn(), self.sortOrder())
        
class SongTableModel(QAbstractTableModel):
    """
    Adapted from the following: 
    https://stackoverflow.com/questions/22791760/pyqt-adding-rows-to-qtableview-using-qabstracttablemodel
    https://stackoverflow.com/questions/35305801/qt-checkboxes-in-qtableview

    Also see:
    https://stackoverflow.com/questions/15757072/user-editable-checkbox-in-qtableview
    https://stackoverflow.com/questions/1849337/how-can-i-add-a-user-editable-checkbox-in-qtableview-using-only-qstandarditemmod
    """

    def __init__(self, data, headers, checkbox_columns, parent=None):
        """
        :param data: 2D array of data
        :param headers: Array of strings.
        :param parent: Parent of model.
        """
        QAbstractTableModel.__init__(self, parent)
        self.array_data = data
        self.header_data = headers
        self.checkbox_columns = checkbox_columns

    def flags(self, index):
        """
        :param index: A QtCore.QModelIndex
        """
        if index.column() in self.checkbox_columns:
            # return QAbstractTableModel.flags(index) | Qt.ItemIsUserCheckable
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
        else:
            # return QAbstractTableModel.flags(index)
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def rowCount(self, parent):
        return len(self.array_data)

    def columnCount(self, parent):
        if len(self.array_data) > 0:
            return len(self.array_data[0])
        return 0

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        return self.array_data[index.row()][index.column()]

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header_data[col]
        return None

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            self.array_data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index, ())
            return True
        else:
            return False

    '''
    # Manually called - see https://stackoverflow.com/questions/28660287/sort-qtableview-in-pyqt5
    def sort(self, Ncol, order):
        """
        Sort table by given column number.
        """
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.array_data = sorted(self.array_data, key=operator.itemgetter(Ncol))
        if order == Qt.DescendingOrder:
            self.array_data.reverse()
        self.emit(SIGNAL("layoutChanged()"))
    '''


class SongView(QTableView):
    """
    Custom QTableView with support for checkboxes and multi-column filtering. Call `setup()` to setup.

    To filter, connect a signal to the proxy's regular expression filter, e.g.:
    `self.LineEdit.textChanged.connect(lambda text: SongView.proxy.setFilterRegularExpression(text))`

    Additional defaults:
        - SelectionBehavior is QAbstractItemView.SelectRows
        - Last column is stretched to fit viewable table
    """
    # TODO: Create top-row used for unchecking and checking all, if checkboxes used
    #       See https://wiki.qt.io/Technical_FAQ#How_can_I_insert_a_checkbox_into_the_header_of_my_view.3F
    #       Or https://stackoverflow.com/questions/21557913/checkbox-in-a-header-cell-in-qtableview

    # Using custom derived classes in Designer:
    # https://stackoverflow.com/questions/19622014/how-do-i-use-promote-to-in-qt-designer-in-pyqt4

    def __init__(self, *args, **kwargs):
        # QWidget.__init__(self, *args, **kwargs)
        super().__init__()
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

    def setup(self, headers, data, box_columns, filter_columns, row_height=20):
        """
        Initializes the table.
        
        :param headers: An array of strings to set the headers for.
        :param data: A 2D array of table data. Horizontal dimensions must be equivalent to `headers`.
        :param boxes: Zero-indexed array of indices to replace with the CheckBoxDelegate.
        :param filter_on: Array of indices to sort on.
        :param row_height: Height of all rows.
        """
        # Arguments for table
        self.headers = headers
        data = data  # Only used on initialization
        self.box_columns = box_columns
        self.filter_columns = filter_columns

        # Create main (hidden) model
        self.table_model = SongTableModel(data, self.headers, self.box_columns, self)

        # Create proxy model
        self.proxy = SortFilterProxyModel(self)
        self.proxy.setSourceModel(self.table_model)

        # Use proxy model for TableView, enable sorting with proxy
        self.setModel(self.proxy)
        self.setSortingEnabled(True)

        # Use checkbox item delegate for specified columns
        delegate = CheckBoxDelegate(self)
        for column in box_columns:
            self.setItemDelegateForColumn(column, delegate)

        # Use checkbox header
        header = CheckBoxHeader(Qt.Horizontal, box_columns, self)
        self.setHorizontalHeader(header)
        # Signal from checkBoxHeader
        header.checkBoxClicked.connect(lambda column_index, checked: self.update_data_from_checkbox_header(column_index, checked))

        # Set standard row height
        # https://stackoverflow.com/questions/19304653/how-to-set-row-height-of-qtableview
        vertical_header = self.verticalHeader()
        vertical_header.setSectionResizeMode(QHeaderView.Fixed)
        vertical_header.setDefaultSectionSize(row_height)

        # Stretch last section
        self.horizontalHeader().setStretchLastSection(True)

    def set_column_widths(self, column_sizes):
        """
        Convenience function for resizing multiple columns at once.
        """
        for column_ind, column_width in enumerate(column_sizes):
            self.setColumnWidth(column_ind, column_width)

    def set_data(self, data):
        """
        Update underlying data and emit `layoutChanged()`.

        :param data: A 2D array of table data. Horizontal dimensions must be equivalent to `headers`.
        """
        self.table_model.layoutAboutToBeChanged.emit()
        self.table_model.array_data = data
        self.table_model.layoutChanged.emit()

    def update_data_from_checkbox_header(self, column_index, new_check_state):
        # Get items currently visible in proxy
        # Map from proxy to source
        # Update applicable source rows
        visible_rows = self.proxy.rowCount()

        for row_index in range(visible_rows):
            proxy_index = self.proxy.index(row_index, column_index)
            source_index = self.proxy.mapToSource(proxy_index)
            self.table_model.setData(source_index, new_check_state)
        
# endregion

# region Other top-level widgets

# Only for local execution
class TestTable(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.setLayout(QVBoxLayout())

        # Testing parameters
        headers = ["Track ID", "Copy?", "Track?", "Title", "Artist", "Album", "Plays", "Trimmed?", "Filepath"]
        data = [
            [23, 1, 1, "image material", "tatsh", "zephyr", 52, "Yes (0:00.000 - 5:25.012)", "D:/Music/a.mp3"],
            [37, 1, 1, "the world's end", "horie yui", "zephyr", 24, "Yes (0:00.000 - 2:14.120)", "D:/Music/b.mp3"],
            [316, 1, 1, "oceanus", "cosmo@bosoup", "deemo", 13, "No", "D:/Music/c.mp3"],
            [521, 0, 0, "wow", "eien-p", "r", 0, "No", "D:/Music/d.mp3"]
        ]
        box_columns = [1, 2]
        filter_on = [3, 4, 5]

        column_sizes = [50, 40, 40, 200, 120, 120, 50, 100, 200]

        # For deltas
        headers_delta = ["Track ID", "Title", "Artist", "Album", "Base plays", "XML plays", "BP plays", "Delta", "New playcount", "Persistent ID"]
        data_delta = [
            [23, "image material", "tatsh", "zephyr", 52, 64, 66, "+36", 88, "as546sfda654fsad465fsd"],
            [37, "the world's end", "horie yui", "zephyr", 52, 64, 66, "+40", 72, "as546sfda654fsad465fsd"],
            [316, "oceanus", "cosmo@bosoup", "deemo", 52, 64, 66, "+36", 89, "as546sfda654fsad465fsd"],
            [521,"wow", "eien-p", "r", 52, 66, 65, "+58", 34, "as546sfda654fsad465fsd"],
        ]
        box_columns_delta = []
        filter_on_delta = [1, 2, 3, 9]

        column_sizes_delta = [50, 200, 120, 120, 80, 80, 80, 80, 100, 200]

        # Initialize SongView, add to window's layout
        tv1 = SongView()
        tv1.setup(headers, data, box_columns, filter_on)
        tv1.set_column_widths(column_sizes)
        self.layout().addWidget(tv1)

        tv2 = SongView()
        tv2.setup(headers_delta, data_delta, box_columns_delta, filter_on_delta)
        tv2.set_column_widths(column_sizes_delta)
        self.layout().addWidget(tv2)

        # Add form layout
        flayout = QFormLayout()
        self.layout().addLayout(flayout)

        # Add filter LineEdit to layout
        self.le = QLineEdit(self)
        flayout.addRow("Search", self.le)
        # On LineEdit change, reset the proxy's filter (which also implicitly runs FilterAcceptsRow())
        self.le.textChanged.connect(lambda text: tv2.proxy.set_filter_text(text))


class SongWorkerConnection(QtCore.QObject):
    """
    Connection for SongWorker; provides signal for updating the progress window.
    
    On an instance of WorkerConnection in SongWorker, do `songStartedProcessing.emit(progress_int, progress_str)`.
    Intended to be used with an instance of ProgressWindow, connected in a way such as the following:

    `worker.connection.songStartedProcessing.connect(lambda a, b: w.updateFields(a, b))`
    """
    # https://stackoverflow.com/questions/53056096/pyside2-qtcore-signal-object-has-no-attribute-connect
    # QRunnables are not QObjects and therefore cannot have their own signals
    songStartedProcessing = QtCore.Signal(int, str)


class ProgressWindowConnection(QtCore.QObject):
    """
    Connection for ProgressWindow; provides signal for updating the log box.

    In ProgressWindow:
    self.logger_connection = LoggerConnection()
    self.logger_connection.appendPlainText.connect(self.log_box.appendPlainText)

    The logger must also be setup within ProgressWindow.

    This resolves a multiple inheritance conflict in ProgressWindow due to emit().
    """
    # Fixes emit() conflict due to multiple inheritance
    # https://stackoverflow.com/questions/52479442/running-a-long-python-calculation-in-a-thread-with-logging-to-a-qt-window-cras/52492689#52492689
    appendPlainText = QtCore.Signal(str)


class TestWorker(QtCore.QRunnable):
    """
    Basic worker thread for testing threading functionality with slots.

    :param args: Arguments to make available to the run code
    :param kwargs: Keywords arguments to make available to the run code
    """
    def __init__(self, *args, **kwargs):
        super(TestWorker, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.signal_connection = SongWorkerConnection()

    #@QtCore.Slot()
    def run(self):
        for i in range(1000):
            logging.warning("test")
            self.signal_connection.songStartedProcessing.emit(i, f"Test song {i}")
            #self.signal.test_signal.emit(i, f"Test song {i}")
            time.sleep(0.1)

class SongWorker(QtCore.QRunnable):
    """
    Worker thread for processing songs.

    Expects the following, all as positional args:
     - a libpytunes Library object
     - a list of track IDs to process
     - a list of track IDs to add to the local database
     - the target directory to write newly processed/copied songs
     - the target directory to write app data (database, new XMLs, .bpstats, etc.)
     - the filepath prefix to use in the .bpstat itself
    """
    def __init__(self, *args, **kwargs):
        super(SongWorker, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.signal_connection = SongWorkerConnection()

    #@QtCore.Slot()
    def run(self):
        lib, processing_ids, tracking_ids, mp3_target_directory, data_directory, bpstat_prefix = self.args

        bpstat_name = datetime.now().strftime("%Y-%m-%d %H-%M-%S (new).bpstat")
        bpstat_path = os.path.join(data_directory, bpstat_name)

        os.makedirs(data_directory, exist_ok=True)
        os.makedirs(mp3_target_directory, exist_ok=True)
        # bpstat generation and processing can happen at the same time
        song_arr = []

        max_to_track = len(tracking_ids)

        # iterate only over ids to process, which is the longest task
        for index, track_id in enumerate(tracking_ids):
            song = lib.songs[track_id]

            logging.info(f"Added {song.name} ({song.persistent_id}) to database for tracking ({index + 1}/{max_to_track})")
            
            bpsynctools.add_to_bpstat(song, bpstat_prefix, bpstat_path)
            song_arr.append(song)

        for index, track_id in enumerate(processing_ids):
            song = lib.songs[track_id]

            logging.info(f"Processing {song.name} ({song.persistent_id})")
            self.signal_connection.songStartedProcessing.emit(index + 1, f"{song.artist} - {song.name}")
            
            bpsynctools.copy_and_process_song(song)
            
        # Create database with new songs
        # TODO: Doesn't work - need to set up to be path-independent
        #models.set_engine(data_directory)
        models.create_db()
        models.add_libpy_songs(song_arr)


class ProgressWindow(logging.Handler, QtWidgets.QWidget, Ui_ProcessingProgress):
    """
    Progress window. Call updateFields() via slot from a worker thread.

    Supports setup as a logger:
    logging.getLogger().addHandler(<instance of ProgressWindow>)

    :param maximum: The maximum value of the progress bar.
    """
    # Derived with help from https://stackoverflow.com/a/60528393 and its comments
    def __init__(self, maximum): # top-level widget, no "parent"
        # Setup three parent classes + UI
        super().__init__()
        QtWidgets.QWidget.__init__(self)
        
        self.setWindowModality(QtCore.Qt.ApplicationModal) 
        self.setupUi(self)

        # Setup slot for log_box
        self.logger_connection = ProgressWindowConnection()
        self.logger_connection.appendPlainText.connect(self.log_box.appendPlainText)

        # Initialize progress bar to specified max
        self.maximum = maximum
        self.progress_bar.setMaximum(maximum)
        self.progress_bar.setValue(0) # Just in case

        self.song_label.setText("Waiting on database...")
        self.progress_label.setText(f"(0/{maximum})")

        # Set up logger
        self.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s'))
        logging.getLogger().addHandler(self)
        logging.getLogger().setLevel(logging.INFO)

    def updateFields(self, new_progress, new_string):
        """
        Update the text field and progress bar.

        :param new_progress: An int of the index currently being processed.
        :param new_string: The text to show as the current song being processed.
        """
        self.progress_label.setText(f"({new_progress}/{self.maximum})")
        self.song_label.setText(new_string)
        self.progress_bar.setValue(new_progress)
    
    def emit(self, record):
        """For logging support"""
        # https://stackoverflow.com/questions/28655198/best-way-to-display-logs-in-pyqt
        msg = self.format(record)
        self.logger_connection.appendPlainText.emit(msg)

# endregion

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    # Table test
    # https://stackoverflow.com/a/60528393 for correct implementation
    # w = TestTable()
    
    
    # Threading test
    thread_manager = QtCore.QThreadPool()
    w = ProgressWindow(1000)

    #logging.getLogger().addHandler(w)
    #logging.getLogger().setLevel(logging.DEBUG)

    worker = TestWorker()
    worker.signal_connection.songStartedProcessing.connect(lambda progress_val, song_string: w.updateFields(progress_val, song_string))
    thread_manager.start(worker)
    
    w.show()
    sys.exit(app.exec())
