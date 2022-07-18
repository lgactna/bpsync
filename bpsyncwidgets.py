"""
Definitions for all custom Qt objects used in this project.
"""
# unfortunately i don't know where the half-qualified and fully-qualified names are anymore
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from PySide6 import QtCore, QtWidgets, QtGui

import datetime
import logging
import os           # All for a "show in Explorer" feature
import time

import eyed3
import libpytunes

import bpsynctools
import models

from progress import Ui_ProcessingProgress
from song_info import Ui_SongInfoDialog

logger = logging.getLogger(__name__)

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

        if int(index.data()) == 0:
           self.drawCheck(painter, option, option.rect, QtCore.Qt.Unchecked)
        elif int(index.data()) == 1: 
           self.drawCheck(painter, option, option.rect, QtCore.Qt.Checked)
        elif int(index.data()) == -1: 
            # If the state of the checkbox is anything other than 0 or 1. 
            # Supports per-item undrawn checkboxes.
            pass
        else:
            # Checkbox data should be [-1, 1], never anything else - this indicates
            # some data mismatching
            logger.warning("Invalid index.data() in CheckboxDelegate.paint()??")

    def editorEvent(self, event, model, option, index):
        """
        Upon a left-click release where the delegate has the ItemIsEditable
        flag enabled, call setModelData(). This means that any rows in a checkbox
        column where ItemIsEditable is not set will not be updated at all.
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
        Set the data. In this case, it just inverts the checkbox on click.

        The index given refers to the proxy, and must be mapped to the source index
        to correctly update the underlying data model:
        https://forum.qt.io/topic/121874/how-to-access-source-model-methods-from-proxy-model,
        https://doc.qt.io/qt-5/qabstractproxymodel.html#mapToSource
        """
        # `index` returns the index relative to the proxy, which must be remapped to the source
        source_index = self.parent().proxy.mapToSource(index)
        check_state = self.parent().table_model.data(source_index, Qt.DisplayRole)
        check_state = 0 if check_state else 1  # Invert 1 -> 0 or 0 -> 1

        # Required call to setData for data to correctly update in the table model
        # Do not edit the underlying array directly!!
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

        # This represents the current state of each checkbox header,
        # where the key is its column index and the value is a boolean
        self.checkbox_columns = {}
        for index in checkbox_columns:
            self.checkbox_columns[index] = True

        # Fixes sorting/clicking on the header items not working
        # https://stackoverflow.com/questions/18777554/why-wont-my-custom-qheaderview-allow-sorting
        self.setSectionsClickable(True)

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
        # Below comments are not relevant due to super() call, kept for reference
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
                self.setIsChecked(column_index, not self.checkbox_columns[column_index])
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
            if index.data() == -1:
                # This is how individual rows can bet set to not have a checkbox
                # All models must agree that "-1" is 
                return Qt.ItemIsEnabled | Qt.ItemIsSelectable
            else:
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
        """
        Set data of specific cell based on the (source) index.

        This can only be used for single-cell changes due to the use of QModelIndex. 
        If you need to edit a lot of data at once, it's probably best
        to directly edit array_data.

        This explicitly emits dataChanged, which is good for tracking single-cell
        changes to the underlying data.
        """
        # (Checkboxes must use this method to edit data, otherwise things will break!)

        # Note: index must be relative to the source model, not the proxy model!
        # Callers are responsible for mapping it ahead of time!
        if role == Qt.EditRole and int(index.flags() & QtCore.Qt.ItemIsEditable) > 0:
            old_data = self.array_data[index.row()][index.column()]
            self.array_data[index.row()][index.column()] = value

            # https://doc.qt.io/qt-6/qabstractitemmodel.html#dataChanged
            # dataChanged normally takes a top-left index, bottom-right index, and a list of flags
            # But since we're only editing one specific cell at a time, the index is the same
            # Any users of dataChanged can safely use just the first index
            
            # Only emit dataChanged if data has actually changed
            if old_data != value:
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
    # How to insert a checkbox into a header of a view:
    # See https://wiki.qt.io/Technical_FAQ#How_can_I_insert_a_checkbox_into_the_header_of_my_view.3F
    # Or https://stackoverflow.com/questions/21557913/checkbox-in-a-header-cell-in-qtableview

    # Using custom derived classes in Designer:
    # https://stackoverflow.com/questions/19622014/how-do-i-use-promote-to-in-qt-designer-in-pyqt4

    # Custom signal to indicate a song has changed. It is the window's responsibility
    # to know how to handle this.
    songChanged = QtCore.Signal(libpytunes.Song)

    def __init__(self, *args, **kwargs):
        """
        Default initialization.

        Note that most "real" initialization is done in setup(). This is done
        because an instance of SongView is created in compiled Qt Creator forms,
        so (unless we overwrite the "default" object) there's no way to pass anything
        into it. 

        To "properly" set up an instance of SongView, call setup() and set_data().
        You may also want to call set_column_widths().
        """
        # TODO: To avoid the odd design pattern above, break all non-song-related
        # functionality out into its own table class, then have SongView inherit from that.
        # This avoids this table from doing everything all at once.

        # QWidget.__init__(self, *args, **kwargs)
        super().__init__()
        
        # When a user selects an item, select the row (not just the cell).
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Whether or not to allow the context menu to appear. 
        # False by default; this is very narrow in use-case, and only works if
        # the track ID is in the first column.
        #
        # You must still set the context menu policy to CustomContextMenu if
        # it isn't already set. This can be done in Qt Creator.
        self.context_menu_enabled = False

        # Default states
        self.headers = []
        self.box_columns = []
        self.filter_columns = []

    def setup(self, headers: list[str], box_columns: list[int], filter_columns: list[int], row_height: int = 20):
        """
        Initializes the table's layout and table model.

        Ideally, this shoud only be called once per instance.
        It is possible to change the table layout with successive calls
        to setup() without needing to replace the SongView. (This does
        create new references for everything.)
        
        :param headers: An array of strings to set the headers for.
        :param boxes: Zero-indexed array of indices to replace with the CheckBoxDelegate.
        :param filter_on: Array of indices to sort on.
        :param row_height: Height of all rows.
        """
        # Arguments for table
        self.headers = headers
        self.box_columns = box_columns
        self.filter_columns = filter_columns

        # Create main (hidden) model
        data = []  # By default, have just an empty table
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
        Completely change underlying data and emit layoutChanged().

        This *will not* caise SongTableModel to emit dataChanged().

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

            # Note that setData checks for the editable flag so this won't affect 
            # the -1 "no checkbox" rows
            self.table_model.setData(source_index, new_check_state)

    def show_context_menu(self, pos, library):
        """
        Show the context menu for a song in the table. 

        Only works if:
         - Track ID is in the first column of this table.
         - A libpytunes Library object is available, passed in as `library`.

         :param pos: The position as emitted by customContextMenuRequested.
         :param library: A libpytunes library that corresponds to the current data in the table.
        """
        # Don't do anything if the context menu isn't enabled.
        if not self.context_menu_enabled:
            return
        
        # Only generate a menu if an (actual) item in the table widget is currently selected.
        # Also, only generate a menu if the library has been loaded.
        proxy_index = self.currentIndex()
        if proxy_index.row() == -1 or proxy_index.column() == -1 or library is None:
            return

        # https://stackoverflow.com/questions/36614635/pyqt-right-click-menu-for-qcombobox
        menu = QtWidgets.QMenu()

        # Note that the table widget shows the results of the proxy model, so
        # any of the QModelIndexes it returns are relative to the proxy, not the
        # underlying source data. As a result, it's necessary to map it to the source
        # data. Also, we always want the track ID in column 0; so it's necessary to
        # create an index directly by taking the "real" row from the table_model and
        # setting the column to 0.
        source_index = self.proxy.mapToSource(proxy_index)
        target_index = self.table_model.index(source_index.row(), 0)
        track_number = self.table_model.data(target_index, QtCore.Qt.DisplayRole)
        song = library.songs[track_number]

        menu.addAction("Details", lambda: self.open_song_info_dialog(song))
        menu.addAction("Show in Explorer", lambda: bpsynctools.open_file(song.location))

        # https://doc.qt.io/qt-5/qwidget.html#mapToGlobal
        # In essence, `pos` is relative to the thing requesting the context menu; therefore, you need to ask the widget
        # to map it to the entire window for it to show up in the correct spot in the window.
        menu.exec(self.mapToGlobal(pos))

    def open_song_info_dialog(self, song):
        self.dialog = SongInfoDialog(song)
        self.dialog.songChanged.connect(lambda song: self.songChanged.emit(song))

        self.dialog.show()

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
            [23, -1, -1, "image material", "tatsh", "zephyr", 52, "Yes (0:00.000 - 5:25.012)", "D:/Music/a.mp3"],
            [37, 1, 1, "the world's end", "horie yui", "zephyr", 24, "Yes (0:00.000 - 2:14.120)", "D:/Music/b.mp3"],
            [316, -1, -1, "oceanus", "cosmo@bosoup", "deemo", 13, "No", "D:/Music/c.mp3"],
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

    This resolves a multiple inheritance conflict in ProgressWindow due to emit()
    in logging.handler.
    """
    # Fixes emit() conflict due to multiple inheritance
    # https://stackoverflow.com/questions/52479442/running-a-long-python-calculation-in-a-thread-with-logging-to-a-qt-window-cras/52492689#52492689
    appendPlainText = QtCore.Signal(str)

    canceled = QtCore.Signal()
    def __init__(self):
        super().__init__()

    def emit_cancel(self):
        self.canceled.emit()

# Only for local execution
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
            logger.warning("test")
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
    def __init__(self, lib, processing_ids, tracking_ids, ignore_ids, mp3_target_directory, data_directory, bpstat_prefix):
        super(SongWorker, self).__init__()

        self.lib = lib
        self.processing_ids = processing_ids
        self.tracking_ids = tracking_ids
        self.ignore_ids = ignore_ids
        self.mp3_target_directory = mp3_target_directory
        self.data_directory = data_directory
        self.bpstat_prefix = bpstat_prefix

        self.signal_connection = SongWorkerConnection()

        self.root_name = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S (new)")
        self.bpstat_path = os.path.join(self.data_directory, f"{self.root_name}.bpstat")

        self.stop_flag = False

    @QtCore.Slot()
    def stop_thread(self):
        """
        Enables the stop flag, does what it says on the label
        """
        # Note: requestInterruption and isInterruptionRequested is likely better.
        self.stop_flag = True

    # @QtCore.Slot()
    def run(self):
        os.makedirs(self.data_directory, exist_ok=True)
        os.makedirs(self.mp3_target_directory, exist_ok=True)
        
        song_arr = []  # array holding libpytunes songs to add to the database for tracking

        max_to_track = len(self.tracking_ids)

        # bpstat generation and processing can happen at the same time

        # iterate only over ids to process, which is the longest task
        for index, track_id in enumerate(self.tracking_ids):
            # Check for thread stop
            if self.stop_flag:
                logger.info("SongWorker thread was stopped during bpstat generation")
                self.signal_connection.songStartedProcessing.emit(index, f"Processing stopped - you can close this window.")
                return

            song = self.lib.songs[track_id]

            logger.info(f"Added {song.name} ({song.persistent_id}) to database for tracking ({index + 1}/{max_to_track})")

            bpsynctools.add_to_bpstat(song, self.bpstat_prefix, self.bpstat_path)
            song_arr.append(song)

        for index, track_id in enumerate(self.processing_ids):
            # Check for thread stop
            if self.stop_flag:
                logger.info("SongWorker thread was stopped during song processing")
                self.signal_connection.songStartedProcessing.emit(index, f"Processing stopped - you can close this window.")
                return

            song = self.lib.songs[track_id]

            logger.info(f"Processing {song.name} ({song.persistent_id})")
            self.signal_connection.songStartedProcessing.emit(index + 1, f"{song.artist} - {song.name}")

            bpsynctools.copy_and_process_song(song)

        self.signal_connection.songStartedProcessing.emit(len(self.processing_ids), f"Processing complete - you can close this window.")

        # Create/write database with new songs
        models.initialize_engine(self.data_directory)
        # Only create underlying tables if the file clearly does not exist yet
        if(not os.path.isfile(os.path.join(self.data_directory, "songs.db"))):
            models.create_db()
        models.add_libpy_songs(song_arr)
        # BUG: also, i think things crash if you delete songs from itunes (since they can't be looked up in library objects anymore)
        models.add_ignored_ids(self.ignore_ids)

class StandardWorker(SongWorker):
    """
    Worker thread for standard sync

    Expects the following, all as positional args:
    For SongWorker:
     - a libpytunes Library object
     - a list of track IDs to process
     - a list of track IDs to add to the local database
     - the target directory to write newly processed/copied songs
     - the target directory to write app data (database, new XMLs, .bpstats, etc.)
     - the filepath prefix to use in the .bpstat itself
    Specifically for StandardWorker:
     - the target directory for backups
     - an array of files to backup
     - the data array used for the table
    """
    # yuck lol
    # is there a better way to arrange these parameters? does a cohesive object make sense here?
    def __init__(self, lib, processing_ids, tracking_ids, mp3_target_directory, data_directory, bpstat_prefix, backup_directory, backup_paths, songs_changed_data):
        super().__init__(lib, processing_ids, tracking_ids, mp3_target_directory, data_directory, bpstat_prefix)
        self.backup_directory = backup_directory
        self.backup_paths = backup_paths
        self.songs_changed_data = songs_changed_data

        self.exportimport_path = os.path.join(self.data_directory, f"{self.root_name} (exportimport).txt")

    def run(self):
        """
        Does the standard-sync processes:

        - Create backups of all input files
        - Iterate over all items currently in the database, update deltas
        - Update libpytunes Library, write out to data_directory/<filename>.xml
        - Start writing existing songs' lines to .bpstat
        - Call run() of SongWorker to fill remainder
        """
        # generate backups
        for backup_filepath in self.backup_paths:
            bpsynctools.create_backup(backup_filepath, self.backup_directory)

        # use the already-calculated values for everything
        # ["Track ID", "Title", "Artist", "Album", "Base plays", "XML plays", "BP plays", "Delta", "New playcount", "Persistent ID"]
        with models.Session() as session:
            # Update existing entries from the songs_changed_table
            for row in self.songs_changed_data:            
                track_id = row[0]
                xml_plays = row[5]
                bp_plays = row[6]
                persistent_id = row[9]

                # get database entry
                db_song = session.query(models.StoredSong).filter(models.StoredSong.persistent_id==persistent_id).scalar()
                delta = db_song.get_delta(xml_plays, bp_plays)
                
                # update library entry and database
                # note that the library entry already includes the extra xml plays, so we just do last_playcount+delta
                self.lib.songs[track_id].play_count = db_song.last_playcount + delta
                
                # at this point, we can use the library entry to update everything
                # since the delta is already reflected in the libpytunes song
                db_song.update_from_libpy_song(self.lib.songs[track_id])

                # write out to bpstat
                bpsynctools.add_to_bpstat(self.lib.songs[track_id], self.bpstat_prefix, self.bpstat_path)
                bpsynctools.add_to_exportimport(db_song, self.exportimport_path)

            # Remove previously ignored songs if applicable
            for track_id in self.tracking_ids:
                lib_song_id = lib.songs[track_id].persistent_id
                ignored_song = session.query(models.IgnoredSong).filter(models.IgnoredSong.persistent_id==persistent_id).scalar()
                if ignored_song:
                    ignored_song.delete()
                    logger.info(f"Found {lib_song_id} in the ignored songs database; it's now being tracked, so it was removed")

            # commit changes
            session.commit()

        # Write out updated library to xml
        xml_path = os.path.join(self.data_directory, f"{self.root_name}.xml")
        self.lib.writeToXML(xml_path)

        super().run()


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

        # Cancel button functionality
        self.cancelButton.clicked.connect(self.cancel_event)

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

        if new_progress == self.maximum:
            self.cancelButton.setDisabled(True)

    def emit(self, record):
        """For logging support"""
        # https://stackoverflow.com/questions/28655198/best-way-to-display-logs-in-pyqt
        msg = self.format(record)
        self.logger_connection.appendPlainText.emit(msg)

    def closeEvent(self, event):
        # Always emit the cancel signal before closing
        self.cancel_event()
        event.accept()
    
    def cancel_event(self):
        logger.info("Cancellation of processing requested")
        self.logger_connection.emit_cancel()
        self.cancelButton.setDisabled(True)

class SongInfoDialog(QtWidgets.QDialog, Ui_SongInfoDialog):
    # Signal emitted when dialog is accepted and the song needs to be passed up the chain
    songChanged = QtCore.Signal(libpytunes.Song)

    def __init__(self, song):
        """
        Set up the IgnoredSongsDialog.

        :param song: The libpytunes song this dialog should display information on.
        """
        super().__init__()

        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setupUi(self)

        self.setWindowTitle(f"Detailed song information: {song.artist} - {song.name}")

        self.song = song

        self.update_fields()
        self.update_album_art()

    def update_fields(self):
        """
        Have all fields reflect the actual values contained in the song.
        """

        song = self.song

        # Top half
        self.titleLineEdit.setText(song.name)
        self.artistLineEdit.setText(song.artist)
        self.albumLineEdit.setText(song.album)
        if song.year:
            self.yearSpinBox.setValue(song.year)
        else:
            self.yearSpinBox.setSpecialValueText("")
        self.genreLineEdit.setText(song.genre)

        self.trackIDLineEdit.setText(str(song.track_id))
        self.persistentIDLineEdit.setText(song.persistent_id)
        self.locationLineEdit.setText(song.location)

        # Column 1
        # Size is in bytes.
        self.sizeLabel.setText(bpsynctools.humanbytes(song.size))
        # https://stackoverflow.com/questions/775049/how-do-i-convert-seconds-to-hours-minutes-and-seconds
        self.totalLengthLabel.setText(str(datetime.timedelta(milliseconds=song.total_time)))
        self.trackTypeLabel.setText(song.track_type)
        self.bpmLabel.setText(str(song.bpm))
        self.dateModifiedLabel.setText(time.strftime("%Y-%m-%d %H:%M:%S", song.date_modified))
        self.dateAddedLabel.setText(time.strftime("%Y-%m-%d %H:%M:%S", song.date_added))
        self.bitrateLabel.setText(str(song.bit_rate))
        self.sampleRateLabel.setText(str(song.sample_rate))

        # Column 2
        if song.start_time:
            self.startTimeSpinBox.setValue(song.start_time)
        else:
            self.yearSpinBox.setSpecialValueText("(start)")
        self.startTimeSpinBox.setMinimum(0)
        self.startTimeSpinBox.setMaximum(song.total_time)
        if song.stop_time:
            self.stopTimeSpinBox.setValue(song.stop_time)
        else:
            self.yearSpinBox.setSpecialValueText("(end)")
        self.stopTimeSpinBox.setMinimum(0)
        self.stopTimeSpinBox.setMaximum(song.total_time)
        if song.disc_number:
            self.discNumberSpinBox.setValue(song.disc_number)
        else:
            self.discNumberSpinBox.setSpecialValueText("(not set)")
        if song.disc_count:
            self.discCountSpinBox.setValue(song.disc_count)
        else:
            self.discCountSpinBox.setSpecialValueText("(not set)")
        if song.track_number:
            self.trackNumberSpinBox.setValue(song.track_number)
        else:
            self.trackNumberSpinBox.setSpecialValueText("(not set)")
        if song.track_count:
            self.trackCountSpinBox.setValue(song.track_count)
        else:
            self.trackCountSpinBox.setSpecialValueText("(not set)")
        self.ratingComputedCheckBox.setChecked(song.rating_computed if song.rating_computed else False)
        self.compilationCheckBox.setChecked(song.compilation if song.compilation else False)

        # Column 3
        self.volumeAdjustmentSpinBox.setValue(song.volume_adjustment if song.volume_adjustment else 0)
        self.playCountSpinBox.setValue(song.play_count if song.play_count else 0)
        if song.lastplayed:
            last_played_qtime = QtCore.QDateTime.fromSecsSinceEpoch(time.mktime(song.lastplayed))
            self.lastPlayedDateTimeEdit.setDateTime(last_played_qtime)
        else:
            self.lastPlayedDateTimeEdit.setSpecialValueText("(never played)")
        if song.skip_count:
            self.skipCountSpinBox.setValue(song.skip_count)
        else:
            self.skipCountSpinBox.setValue(0)
        if song.skip_date:
            last_skipped_qtime = QtCore.QDateTime.fromSecsSinceEpoch(time.mktime(song.skip_date))
            self.lastSkippedDateTimeEdit.setDateTime(last_skipped_qtime)
        else:
            self.lastSkippedDateTimeEdit.setSpecialValueText("(never skipped)")
        if song.album_rating:
            self.albumRatingSpinBox.setValue(song.album_rating)
        else:
            self.albumRatingSpinBox.setSpecialValueText("(not set)")
        self.lovedCheckBox.setChecked(song.loved if song.loved else False)
        self.dislikedCheckBox.setChecked(song.disliked if song.disliked else False)
    
    def update_album_art(self):
        # Get location of song (which is guaranteed to exist, probably)
        # Load its data via eyed3
        try:
            audio_file = eyed3.load(self.song.location)
        except IOError:
            # the file couldn't be found; at this point, just keep the label as-is
            self.songImageLabel.setText("File not found")
            return

        if len(audio_file.tag.images) == 0:
            logger.warning(f"Audio file at {self.song.location} has no image baked-in.")
            self.songImageLabel.setText("No image available")
            return
        elif len(audio_file.tag.images) > 1:
            logger.info(f"Audio file at {self.song.location} appears to have more than one image embedded, showing the first one.")

        image = audio_file.tag.images[0]
        image_data = image.image_data

        q_image = QtGui.QImage()
        q_image.loadFromData(image_data)

        pixmap = QtGui.QPixmap.fromImage(q_image)
        pixmap_scaled = pixmap.scaled(self.songImageLabel.width(), self.songImageLabel.height(), QtCore.Qt.KeepAspectRatio)

        self.songImageLabel.setPixmap(pixmap_scaled)

    def accept(self):
        """
        On dialog accept (OK button is clicked).

        This requires additional logic to have the table that showed this dialog
        in the first place to reflect the new values, since the underlying
        data model isn't "connected" to the library. It is the window's responsibility
        to reflect the changes in the table's data, since only it knows how the
        model is currently structured. This is achieved by emitting a songChanged
        signal from the dialog, which is emitted again by SongView, which should be
        connected to by the parent window.
        """
        # Refuse to do anything if the title or artist is empty, which is not allowed
        if not self.titleLineEdit.text() or not self.artistLineEdit.text():
            bpsynctools.show_error_window("Title and artist cannot be empty.", "", "Save error")
            return

        # there is likely a better way to do this, especially in Qt, but I'm not quite
        # sure what that would look like (without just subclassing/overloading everything)
        self.song.name = self.titleLineEdit.text()
        self.song.artist = self.artistLineEdit.text()
        self.song.album = self.albumLineEdit.text()
        self.song.year = self.yearSpinBox.value()
        self.song.genre = self.genreLineEdit.text()

        self.song.start_time = self.startTimeSpinBox.value() if not self.startTimeSpinBox.specialValueText() else None
        self.song.stop_time = self.stopTimeSpinBox.value() if not self.stopTimeSpinBox.specialValueText() else None
        self.song.disc_number = self.discNumberSpinBox.value() if not self.discNumberSpinBox.specialValueText() else None
        self.song.disc_count = self.discCountSpinBox.value() if not self.discCountSpinBox.specialValueText() else None
        self.song.track_number = self.trackNumberSpinBox.value() if not self.trackNumberSpinBox.specialValueText() else None
        self.song.track_count = self.trackCountSpinBox.value() if not self.trackCountSpinBox.specialValueText() else None

        self.song.volume_adjustment = self.volumeAdjustmentSpinBox.value() if self.volumeAdjustmentSpinBox.value() else None
        self.song.play_count = self.playCountSpinBox.value() if self.playCountSpinBox.value() else None
        self.song.last_played = self.lastPlayedDateTimeEdit.dateTime().toPython() if not self.lastPlayedDateTimeEdit.specialValueText() else None
        self.song.skip_count = self.skipCountSpinBox.value() if self.skipCountSpinBox.value() else None
        self.song.skip_date = self.lastSkippedDateTimeEdit.dateTime().toPython() if not self.lastPlayedDateTimeEdit.specialValueText() else None
        self.song.albumRating = self.albumRatingSpinBox.value() if not self.albumRatingSpinBox.specialValueText() else None

        self.song.rating_computed = self.ratingComputedCheckBox.isChecked() if self.ratingComputedCheckBox.isChecked() else None
        self.song.compilation = self.compilationCheckBox.isChecked() if self.compilationCheckBox.isChecked() else None
        self.song.loved = self.lovedCheckBox.isChecked() if self.lovedCheckBox.isChecked() else None
        self.song.disliked = self.dislikedCheckBox.isChecked() if self.dislikedCheckBox.isChecked() else None

        self.songChanged.emit(self.song)

        # Call super
        super().accept()


# endregion

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    # Table test
    # https://stackoverflow.com/a/60528393 for correct implementation
    w = TestTable()


    # Threading test
    # thread_manager = QtCore.QThreadPool()
    # w = ProgressWindow(1000)

    # logging.getLogger().addHandler(w)
    # logging.getLogger().setLevel(logging.DEBUG)

    # worker = TestWorker()
    # worker.signal_connection.songStartedProcessing.connect(lambda progress_val, song_string: w.updateFields(progress_val, song_string))
    # thread_manager.start(worker)

    w.show()
    sys.exit(app.exec())
