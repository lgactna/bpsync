# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'first_time.ui'
##
## Created by: Qt User Interface Compiler version 6.2.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_FirstTimeWindow(object):
    def setupUi(self, FirstTimeWindow):
        if not FirstTimeWindow.objectName():
            FirstTimeWindow.setObjectName(u"FirstTimeWindow")
        FirstTimeWindow.resize(840, 670)
        self.verticalLayout_3 = QVBoxLayout(FirstTimeWindow)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_2 = QLabel(FirstTimeWindow)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.label_2)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label = QLabel(FirstTimeWindow)
        self.label.setObjectName(u"label")

        self.horizontalLayout_5.addWidget(self.label)

        self.xml_path_lineedit = QLineEdit(FirstTimeWindow)
        self.xml_path_lineedit.setObjectName(u"xml_path_lineedit")

        self.horizontalLayout_5.addWidget(self.xml_path_lineedit)

        self.xml_browse_button = QPushButton(FirstTimeWindow)
        self.xml_browse_button.setObjectName(u"xml_browse_button")

        self.horizontalLayout_5.addWidget(self.xml_browse_button)

        self.xml_load_button = QPushButton(FirstTimeWindow)
        self.xml_load_button.setObjectName(u"xml_load_button")

        self.horizontalLayout_5.addWidget(self.xml_load_button)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.tracks_copycount_label = QLabel(FirstTimeWindow)
        self.tracks_copycount_label.setObjectName(u"tracks_copycount_label")

        self.gridLayout.addWidget(self.tracks_copycount_label, 0, 1, 1, 1)

        self.tracks_synccount_label = QLabel(FirstTimeWindow)
        self.tracks_synccount_label.setObjectName(u"tracks_synccount_label")

        self.gridLayout.addWidget(self.tracks_synccount_label, 1, 1, 1, 1)

        self.tracks_totalsize_label = QLabel(FirstTimeWindow)
        self.tracks_totalsize_label.setObjectName(u"tracks_totalsize_label")

        self.gridLayout.addWidget(self.tracks_totalsize_label, 1, 0, 1, 1)

        self.tracks_found_label = QLabel(FirstTimeWindow)
        self.tracks_found_label.setObjectName(u"tracks_found_label")

        self.gridLayout.addWidget(self.tracks_found_label, 0, 0, 1, 1)

        self.tracks_copysize_label = QLabel(FirstTimeWindow)
        self.tracks_copysize_label.setObjectName(u"tracks_copysize_label")

        self.gridLayout.addWidget(self.tracks_copysize_label, 2, 0, 1, 1)

        self.tracks_error_label = QLabel(FirstTimeWindow)
        self.tracks_error_label.setObjectName(u"tracks_error_label")
        self.tracks_error_label.setStyleSheet(u"color:red")

        self.gridLayout.addWidget(self.tracks_error_label, 2, 1, 1, 1)


        self.horizontalLayout_5.addLayout(self.gridLayout)


        self.horizontalLayout_6.addLayout(self.horizontalLayout_5)


        self.verticalLayout_3.addLayout(self.horizontalLayout_6)

        self.label_8 = QLabel(FirstTimeWindow)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_3.addWidget(self.label_8)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_18 = QLabel(FirstTimeWindow)
        self.label_18.setObjectName(u"label_18")

        self.horizontalLayout_4.addWidget(self.label_18)

        self.table_filter_lineedit = QLineEdit(FirstTimeWindow)
        self.table_filter_lineedit.setObjectName(u"table_filter_lineedit")

        self.horizontalLayout_4.addWidget(self.table_filter_lineedit)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.songs_table = QTableWidget(FirstTimeWindow)
        if (self.songs_table.columnCount() < 9):
            self.songs_table.setColumnCount(9)
        __qtablewidgetitem = QTableWidgetItem()
        self.songs_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.songs_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.songs_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.songs_table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.songs_table.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.songs_table.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.songs_table.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.songs_table.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.songs_table.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        if (self.songs_table.rowCount() < 1):
            self.songs_table.setRowCount(1)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.songs_table.setVerticalHeaderItem(0, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.songs_table.setItem(0, 0, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.songs_table.setItem(0, 1, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.songs_table.setItem(0, 2, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.songs_table.setItem(0, 3, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.songs_table.setItem(0, 4, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.songs_table.setItem(0, 5, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.songs_table.setItem(0, 6, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.songs_table.setItem(0, 7, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.songs_table.setItem(0, 8, __qtablewidgetitem18)
        self.songs_table.setObjectName(u"songs_table")
        self.songs_table.setEnabled(False)
        self.songs_table.horizontalHeader().setMinimumSectionSize(40)
        self.songs_table.horizontalHeader().setDefaultSectionSize(100)
        self.songs_table.horizontalHeader().setProperty("showSortIndicator", True)
        self.songs_table.horizontalHeader().setStretchLastSection(True)
        self.songs_table.verticalHeader().setMinimumSectionSize(20)
        self.songs_table.verticalHeader().setDefaultSectionSize(20)
        self.songs_table.verticalHeader().setProperty("showSortIndicator", False)
        self.songs_table.verticalHeader().setStretchLastSection(False)

        self.verticalLayout_3.addWidget(self.songs_table)

        self.groupBox = QGroupBox(FirstTimeWindow)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_9 = QLabel(self.groupBox)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout.addWidget(self.label_9)

        self.mp3_path_lineedit = QLineEdit(self.groupBox)
        self.mp3_path_lineedit.setObjectName(u"mp3_path_lineedit")

        self.horizontalLayout.addWidget(self.mp3_path_lineedit)

        self.mp3_browse_button = QPushButton(self.groupBox)
        self.mp3_browse_button.setObjectName(u"mp3_browse_button")

        self.horizontalLayout.addWidget(self.mp3_browse_button)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.label_16 = QLabel(self.groupBox)
        self.label_16.setObjectName(u"label_16")

        self.verticalLayout_2.addWidget(self.label_16)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_10 = QLabel(self.groupBox)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_2.addWidget(self.label_10)

        self.db_path_lineedit = QLineEdit(self.groupBox)
        self.db_path_lineedit.setObjectName(u"db_path_lineedit")

        self.horizontalLayout_2.addWidget(self.db_path_lineedit)

        self.db_browse_button = QPushButton(self.groupBox)
        self.db_browse_button.setObjectName(u"db_browse_button")

        self.horizontalLayout_2.addWidget(self.db_browse_button)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.label_17 = QLabel(self.groupBox)
        self.label_17.setObjectName(u"label_17")

        self.verticalLayout_2.addWidget(self.label_17)

        self.groupBox_2 = QGroupBox(self.groupBox)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_12 = QLabel(self.groupBox_2)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_12)

        self.label_13 = QLabel(self.groupBox_2)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_13)

        self.label_14 = QLabel(self.groupBox_2)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_14)

        self.label_15 = QLabel(self.groupBox_2)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_15)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_11 = QLabel(self.groupBox_2)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_3.addWidget(self.label_11)

        self.bpstat_path_lineedit = QLineEdit(self.groupBox_2)
        self.bpstat_path_lineedit.setObjectName(u"bpstat_path_lineedit")

        self.horizontalLayout_3.addWidget(self.bpstat_path_lineedit)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.verticalLayout_2.addWidget(self.groupBox_2)


        self.verticalLayout_3.addWidget(self.groupBox)

        self.start_button = QPushButton(FirstTimeWindow)
        self.start_button.setObjectName(u"start_button")
        self.start_button.setEnabled(False)

        self.verticalLayout_3.addWidget(self.start_button)


        self.retranslateUi(FirstTimeWindow)

        QMetaObject.connectSlotsByName(FirstTimeWindow)
    # setupUi

    def retranslateUi(self, FirstTimeWindow):
        FirstTimeWindow.setWindowTitle(QCoreApplication.translate("FirstTimeWindow", u"First-time Sync Setup", None))
        self.label_2.setText(QCoreApplication.translate("FirstTimeWindow", u"This tool copies and renames the songs you select from the XML and creates a .bpstat for importing statistics. It also creates a local database file used for tracking playcount changes between BlackPlayer and the XML.", None))
        self.label.setText(QCoreApplication.translate("FirstTimeWindow", u"XML filepath", None))
        self.xml_browse_button.setText(QCoreApplication.translate("FirstTimeWindow", u"Browse", None))
        self.xml_load_button.setText(QCoreApplication.translate("FirstTimeWindow", u"Load", None))
        self.tracks_copycount_label.setText(QCoreApplication.translate("FirstTimeWindow", u"0 tracks selected for copying", None))
        self.tracks_synccount_label.setText(QCoreApplication.translate("FirstTimeWindow", u"0 tracks selected for syncing", None))
        self.tracks_totalsize_label.setText(QCoreApplication.translate("FirstTimeWindow", u"0 MB total size", None))
        self.tracks_found_label.setText(QCoreApplication.translate("FirstTimeWindow", u"0 tracks found", None))
        self.tracks_copysize_label.setText(QCoreApplication.translate("FirstTimeWindow", u"0 MB to be copied", None))
        self.tracks_error_label.setText(QCoreApplication.translate("FirstTimeWindow", u"Please load an XML!", None))
        self.label_8.setText(QCoreApplication.translate("FirstTimeWindow", u"Songs to copy and prepare for sync", None))
        self.label_18.setText(QCoreApplication.translate("FirstTimeWindow", u"Search", None))
        ___qtablewidgetitem = self.songs_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("FirstTimeWindow", u"Track ID", None));
        ___qtablewidgetitem1 = self.songs_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("FirstTimeWindow", u"Copy?", None));
        ___qtablewidgetitem2 = self.songs_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("FirstTimeWindow", u"Track?", None));
        ___qtablewidgetitem3 = self.songs_table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("FirstTimeWindow", u"Title", None));
        ___qtablewidgetitem4 = self.songs_table.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("FirstTimeWindow", u"Artist", None));
        ___qtablewidgetitem5 = self.songs_table.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("FirstTimeWindow", u"Album", None));
        ___qtablewidgetitem6 = self.songs_table.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("FirstTimeWindow", u"Playcount", None));
        ___qtablewidgetitem7 = self.songs_table.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("FirstTimeWindow", u"Filepath", None));
        ___qtablewidgetitem8 = self.songs_table.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("FirstTimeWindow", u"Trimmed?", None));
        ___qtablewidgetitem9 = self.songs_table.verticalHeaderItem(0)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("FirstTimeWindow", u"Row1", None));

        __sortingEnabled = self.songs_table.isSortingEnabled()
        self.songs_table.setSortingEnabled(False)
        ___qtablewidgetitem10 = self.songs_table.item(0, 0)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("FirstTimeWindow", u"25", None));
        ___qtablewidgetitem11 = self.songs_table.item(0, 1)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("FirstTimeWindow", u"N", None));
        ___qtablewidgetitem12 = self.songs_table.item(0, 2)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("FirstTimeWindow", u"N", None));
        ___qtablewidgetitem13 = self.songs_table.item(0, 3)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("FirstTimeWindow", u"September", None));
        ___qtablewidgetitem14 = self.songs_table.item(0, 4)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("FirstTimeWindow", u"Earth, Wind & Fire", None));
        ___qtablewidgetitem15 = self.songs_table.item(0, 5)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("FirstTimeWindow", u"September", None));
        ___qtablewidgetitem16 = self.songs_table.item(0, 6)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("FirstTimeWindow", u"15", None));
        ___qtablewidgetitem17 = self.songs_table.item(0, 7)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("FirstTimeWindow", u"D:\\Music\\september.mp3", None));
        ___qtablewidgetitem18 = self.songs_table.item(0, 8)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("FirstTimeWindow", u"Yes (0:00.012 - 3:36.150)", None));
        self.songs_table.setSortingEnabled(__sortingEnabled)

        self.groupBox.setTitle(QCoreApplication.translate("FirstTimeWindow", u"Options", None))
        self.label_9.setText(QCoreApplication.translate("FirstTimeWindow", u"mp3 folder destination", None))
        self.mp3_browse_button.setText(QCoreApplication.translate("FirstTimeWindow", u"Browse", None))
        self.label_16.setText(QCoreApplication.translate("FirstTimeWindow", u"Any mp3s you have selected to be copied and renamed above will be sent to this folder.", None))
        self.label_10.setText(QCoreApplication.translate("FirstTimeWindow", u"Local DB filepath", None))
        self.db_browse_button.setText(QCoreApplication.translate("FirstTimeWindow", u"Browse", None))
        self.label_17.setText(QCoreApplication.translate("FirstTimeWindow", u"The location of the local database used to track changes to playcount between the XML and .bpstat.", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("FirstTimeWindow", u".bpstat generation", None))
        self.label_12.setText(QCoreApplication.translate("FirstTimeWindow", u"This program works by assuming all songs will be written to one flat folder, with no subdirectories and (essentially) randomized unique filenames for each mp3. To generate the associated .bpstat, you must know the full Android filepath of the folder your music will be stored in in advance.", None))
        self.label_13.setText(QCoreApplication.translate("FirstTimeWindow", u"Common root folders for music storage are:", None))
        self.label_14.setText(QCoreApplication.translate("FirstTimeWindow", u"- /storage/emulated/0/ for internal shared storage", None))
        self.label_15.setText(QCoreApplication.translate("FirstTimeWindow", u"- /storage/sdcard1/ for SD cards", None))
        self.label_11.setText(QCoreApplication.translate("FirstTimeWindow", u"Prepended filepath", None))
        self.bpstat_path_lineedit.setPlaceholderText(QCoreApplication.translate("FirstTimeWindow", u"/storage/emulated/0/Music", None))
        self.start_button.setText(QCoreApplication.translate("FirstTimeWindow", u"Start processing", None))
    # retranslateUi

