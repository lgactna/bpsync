from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from PySide6 import QtCore, QtWidgets

from random import randint, choice

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
        self.drawBackground(painter, option, index) # Draws the background for row-based selection
        self.drawCheck(painter, option, option.rect, QtCore.Qt.Unchecked if int(index.data()) == 0 else QtCore.Qt.Checked)

    def editorEvent(self, event, model, option, index):
        '''
        Change the data in the model and the state of the checkbox
        if the user presses the left mousebutton and this cell is editable. Otherwise do nothing.
        '''
        if not int(index.flags() & QtCore.Qt.ItemIsEditable) > 0:
            print(int(index.flags()))
            return False
        if event.type() == QtCore.QEvent.Type.MouseButtonRelease and event.button() == Qt.MouseButton.LeftButton:
            # Change the checkbox-state
            self.setModelData(None, model, index)
            return True
        return False


    def setModelData (self, editor, model, index):
        '''
        Invert checkbox on click.

        Affects proxy: 
        https://forum.qt.io/topic/121874/how-to-access-source-model-methods-from-proxy-model,
        https://doc.qt.io/qt-5/qabstractproxymodel.html#mapToSource
        '''

        source_index = self.parent().proxy.mapToSource(index)
        data = self.parent().table_model.data(source_index, Qt.DisplayRole)
        data = int(not bool(data)) # Invert 1 -> 0 or 0 -> 1

        self.parent().table_model.setData(source_index, data, Qt.EditRole)


class SortFilterProxyModel(QSortFilterProxyModel):
    """
    Proxy used to perform filtering and sorting without affecting the underlying data.

    Expects the parent (SongView) to have the filter_on array.
    """
    def __init__(self, *args, **kwargs):
        QSortFilterProxyModel.__init__(self, *args, **kwargs)
        
    def filterAcceptsRow(self, source_row, source_parent):
        """
        Filters rows based on filterRegularExpression.

        Intended signal is a textChanged from a LineEdit like so:
        `self.LineEdit.textChanged.connect(lambda text: TableView.proxy.setFilterRegularExpression(text))`
        """
        # The proxy's current regular expression filter
        regex = self.filterRegularExpression()

        #iterate over all columns of row
        filter_columns = self.parent().filter_columns
        for column_index in filter_columns:
            index = self.sourceModel().index(source_row, column_index, source_parent)
            if index.isValid():
                 text = str(self.sourceModel().data(index, Qt.DisplayRole))
                 if regex.match(text).hasMatch():
                    return True
        return False

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
            #return QAbstractTableModel.flags(index) | Qt.ItemIsUserCheckable
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
        else:
            #return QAbstractTableModel.flags(index)
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

    def setData(self, index, value, role = Qt.EditRole):     
        if role == Qt.EditRole:             
            self.array_data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index, ())             
            return True         
        else:             
            return False

    def sort(self, Ncol, order):
        """
        Sort table by given column number.
        """
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.array_data = sorted(self.array_data, key=operator.itemgetter(Ncol))       
        if order == Qt.DescendingOrder:
            self.array_data.reverse()
        self.emit(SIGNAL("layoutChanged()"))

class SongView(QTableView):
    """
    Custom QTableView with support for checkboxes and multi-column filtering.

    :param headers: An array of strings to set the headers for.
    :param data: A 2D array of table data. Horizontal dimensions must be equivalent to `headers`
    :param boxes: Zero-indexed array of indices to replace with the CheckBoxDelegate.
    :param filter_on: Array of indices to sort on.

    The entire row, representing one song, is selected by default.
    """
    # TODO: Create top-row used for unchecking and checking all, if checkboxes used
    #       See https://wiki.qt.io/Technical_FAQ#How_can_I_insert_a_checkbox_into_the_header_of_my_view.3F
    # TODO: Test data replacement
    # TODO: Set column widths

    # In Qt Designer: https://stackoverflow.com/questions/19622014/how-do-i-use-promote-to-in-qt-designer-in-pyqt4

    def __init__(self, *args, **kwargs):
        # QWidget.__init__(self, *args, **kwargs)
        super().__init__()
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
    
    def setup(self, headers, data, box_columns, filter_columns):
        # Arguments for table
        self.headers = headers
        self.data = data
        self.box_columns = box_columns
        self.filter_columns = filter_columns

        # Create main (hidden) model
        self.table_model = SongTableModel(self.data, self.headers, self.box_columns, self)
        
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

# Only for local execution
class TestWidget(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.setLayout(QVBoxLayout())

        # Testing parameters
        headers = ["Track ID", "Copy?", "Track?", "Title", "Artist", "Album", "Plays", "Trimmed?", "Filepath"]
        data = [
                [None, 1, 1, None, None, None, None, None, None],
                [23, 1, 1, "image material", "tatsh", "zephyr", 52, "Yes (0:00.000 - 5:25.012)", "D:/Music/a.mp3"],
                [37, 1, 1, "the world's end", "horie yui", "zephyr", 24, "Yes (0:00.000 - 2:14.120)", "D:/Music/b.mp3"],
                [316, 1, 1, "oceanus", "cosmo@bosoup", "deemo", 13, "No", "D:/Music/c.mp3"],
                [521, 0, 0, "wow", "eien-p", "r", 0, "No", "D:/Music/d.mp3"]
               ]
        box_columns = [1, 2]
        filter_on = [3, 4, 5]

        # Initialize SongView, add to window's layout
        tv1 = SongView()
        tv1.setup(headers, data, box_columns, filter_on)
        self.layout().addWidget(tv1)

        # Add form layout
        flayout = QFormLayout()
        self.layout().addLayout(flayout)
        
        # Add filter LineEdit to layout
        self.le = QLineEdit(self)
        flayout.addRow("Search", self.le)
        # On LineEdit change, reset the proxy's filter (which also implicitly runs FilterAcceptsRow())
        self.le.textChanged.connect(lambda text: tv1.proxy.setFilterRegularExpression(text))

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = TestWidget()
    w.show()
    sys.exit(app.exec())
