from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from PySide6 import QtCore, QtWidgets


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
            self.checkbox_columns[index] = False

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
        
        
# Only for local execution
class TestWidget(QWidget):
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

        # Initialize SongView, add to window's layout
        tv1 = SongView()
        tv1.setup(headers, data, box_columns, filter_on)
        tv1.set_column_widths(column_sizes)
        self.layout().addWidget(tv1)

        # Add form layout
        flayout = QFormLayout()
        self.layout().addLayout(flayout)

        # Add filter LineEdit to layout
        self.le = QLineEdit(self)
        flayout.addRow("Search", self.le)
        # On LineEdit change, reset the proxy's filter (which also implicitly runs FilterAcceptsRow())
        self.le.textChanged.connect(lambda text: tv1.proxy.set_filter_text(text))


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = TestWidget()
    w.show()
    sys.exit(app.exec())
