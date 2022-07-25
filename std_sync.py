# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'std_sync.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

from bpsyncwidgets import SongView

class Ui_StandardSyncWindow(object):
    def setupUi(self, StandardSyncWindow):
        if not StandardSyncWindow.objectName():
            StandardSyncWindow.setObjectName(u"StandardSyncWindow")
        StandardSyncWindow.resize(840, 754)
        self.verticalLayout_5 = QVBoxLayout(StandardSyncWindow)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_2 = QLabel(StandardSyncWindow)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setWordWrap(True)

        self.verticalLayout_5.addWidget(self.label_2)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label = QLabel(StandardSyncWindow)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(85, 0))

        self.horizontalLayout_5.addWidget(self.label)

        self.xml_path_lineedit = QLineEdit(StandardSyncWindow)
        self.xml_path_lineedit.setObjectName(u"xml_path_lineedit")

        self.horizontalLayout_5.addWidget(self.xml_path_lineedit)

        self.xml_browse_button = QPushButton(StandardSyncWindow)
        self.xml_browse_button.setObjectName(u"xml_browse_button")

        self.horizontalLayout_5.addWidget(self.xml_browse_button)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_3 = QLabel(StandardSyncWindow)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(85, 0))

        self.horizontalLayout_7.addWidget(self.label_3)

        self.bpstat_path_lineedit = QLineEdit(StandardSyncWindow)
        self.bpstat_path_lineedit.setObjectName(u"bpstat_path_lineedit")

        self.horizontalLayout_7.addWidget(self.bpstat_path_lineedit)

        self.bpstat_browse_button = QPushButton(StandardSyncWindow)
        self.bpstat_browse_button.setObjectName(u"bpstat_browse_button")

        self.horizontalLayout_7.addWidget(self.bpstat_browse_button)


        self.verticalLayout_3.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_4 = QLabel(StandardSyncWindow)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_8.addWidget(self.label_4)

        self.database_path_lineedit = QLineEdit(StandardSyncWindow)
        self.database_path_lineedit.setObjectName(u"database_path_lineedit")

        self.horizontalLayout_8.addWidget(self.database_path_lineedit)

        self.database_browse_button = QPushButton(StandardSyncWindow)
        self.database_browse_button.setObjectName(u"database_browse_button")

        self.horizontalLayout_8.addWidget(self.database_browse_button)


        self.verticalLayout_3.addLayout(self.horizontalLayout_8)


        self.horizontalLayout_6.addLayout(self.verticalLayout_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.load_all_button = QPushButton(StandardSyncWindow)
        self.load_all_button.setObjectName(u"load_all_button")

        self.verticalLayout_4.addWidget(self.load_all_button)

        self.calc_hashes_checkbox = QCheckBox(StandardSyncWindow)
        self.calc_hashes_checkbox.setObjectName(u"calc_hashes_checkbox")

        self.verticalLayout_4.addWidget(self.calc_hashes_checkbox)


        self.horizontalLayout_6.addLayout(self.verticalLayout_4)

        self.groupBox_2 = QGroupBox(StandardSyncWindow)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.tracks_indatabase_label = QLabel(self.groupBox_2)
        self.tracks_indatabase_label.setObjectName(u"tracks_indatabase_label")

        self.gridLayout.addWidget(self.tracks_indatabase_label, 1, 0, 1, 1)

        self.tracks_copysize_label = QLabel(self.groupBox_2)
        self.tracks_copysize_label.setObjectName(u"tracks_copysize_label")

        self.gridLayout.addWidget(self.tracks_copysize_label, 2, 0, 1, 1)

        self.tracks_copycount_label = QLabel(self.groupBox_2)
        self.tracks_copycount_label.setObjectName(u"tracks_copycount_label")

        self.gridLayout.addWidget(self.tracks_copycount_label, 2, 1, 1, 1)

        self.tracks_found_label = QLabel(self.groupBox_2)
        self.tracks_found_label.setObjectName(u"tracks_found_label")

        self.gridLayout.addWidget(self.tracks_found_label, 0, 0, 1, 1)

        self.tracks_synccount_label = QLabel(self.groupBox_2)
        self.tracks_synccount_label.setObjectName(u"tracks_synccount_label")

        self.gridLayout.addWidget(self.tracks_synccount_label, 1, 1, 1, 1)

        self.tracks_totalsize_label = QLabel(self.groupBox_2)
        self.tracks_totalsize_label.setObjectName(u"tracks_totalsize_label")

        self.gridLayout.addWidget(self.tracks_totalsize_label, 0, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)


        self.horizontalLayout_6.addWidget(self.groupBox_2)


        self.verticalLayout_5.addLayout(self.horizontalLayout_6)

        self.label_8 = QLabel(StandardSyncWindow)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_5.addWidget(self.label_8)

        self.songs_changed_table = SongView(StandardSyncWindow)
        self.songs_changed_table.setObjectName(u"songs_changed_table")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.songs_changed_table.sizePolicy().hasHeightForWidth())
        self.songs_changed_table.setSizePolicy(sizePolicy)
        self.songs_changed_table.setContextMenuPolicy(Qt.CustomContextMenu)

        self.verticalLayout_5.addWidget(self.songs_changed_table)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_18 = QLabel(StandardSyncWindow)
        self.label_18.setObjectName(u"label_18")

        self.horizontalLayout_4.addWidget(self.label_18)

        self.songs_changed_lineedit = QLineEdit(StandardSyncWindow)
        self.songs_changed_lineedit.setObjectName(u"songs_changed_lineedit")

        self.horizontalLayout_4.addWidget(self.songs_changed_lineedit)


        self.verticalLayout_5.addLayout(self.horizontalLayout_4)

        self.label_11 = QLabel(StandardSyncWindow)
        self.label_11.setObjectName(u"label_11")

        self.verticalLayout_5.addWidget(self.label_11)

        self.new_songs_table = SongView(StandardSyncWindow)
        self.new_songs_table.setObjectName(u"new_songs_table")
        sizePolicy.setHeightForWidth(self.new_songs_table.sizePolicy().hasHeightForWidth())
        self.new_songs_table.setSizePolicy(sizePolicy)
        self.new_songs_table.setContextMenuPolicy(Qt.CustomContextMenu)

        self.verticalLayout_5.addWidget(self.new_songs_table)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_19 = QLabel(StandardSyncWindow)
        self.label_19.setObjectName(u"label_19")

        self.horizontalLayout_9.addWidget(self.label_19)

        self.new_songs_lineedit = QLineEdit(StandardSyncWindow)
        self.new_songs_lineedit.setObjectName(u"new_songs_lineedit")

        self.horizontalLayout_9.addWidget(self.new_songs_lineedit)


        self.verticalLayout_5.addLayout(self.horizontalLayout_9)

        self.groupBox = QGroupBox(StandardSyncWindow)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.show_ignored_songs_button = QPushButton(self.groupBox)
        self.show_ignored_songs_button.setObjectName(u"show_ignored_songs_button")

        self.verticalLayout_2.addWidget(self.show_ignored_songs_button)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_12 = QLabel(self.groupBox)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_3.addWidget(self.label_12)

        self.data_path_lineedit = QLineEdit(self.groupBox)
        self.data_path_lineedit.setObjectName(u"data_path_lineedit")

        self.horizontalLayout_3.addWidget(self.data_path_lineedit)

        self.data_browse_button = QPushButton(self.groupBox)
        self.data_browse_button.setObjectName(u"data_browse_button")

        self.horizontalLayout_3.addWidget(self.data_browse_button)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.label_20 = QLabel(self.groupBox)
        self.label_20.setObjectName(u"label_20")

        self.verticalLayout_2.addWidget(self.label_20)

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

        self.backup_path_lineedit = QLineEdit(self.groupBox)
        self.backup_path_lineedit.setObjectName(u"backup_path_lineedit")

        self.horizontalLayout_2.addWidget(self.backup_path_lineedit)

        self.backup_browse_button = QPushButton(self.groupBox)
        self.backup_browse_button.setObjectName(u"backup_browse_button")

        self.horizontalLayout_2.addWidget(self.backup_browse_button)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.label_17 = QLabel(self.groupBox)
        self.label_17.setObjectName(u"label_17")

        self.verticalLayout_2.addWidget(self.label_17)


        self.verticalLayout_5.addWidget(self.groupBox)

        self.start_button = QPushButton(StandardSyncWindow)
        self.start_button.setObjectName(u"start_button")
        self.start_button.setEnabled(True)

        self.verticalLayout_5.addWidget(self.start_button)


        self.retranslateUi(StandardSyncWindow)

        QMetaObject.connectSlotsByName(StandardSyncWindow)
    # setupUi

    def retranslateUi(self, StandardSyncWindow):
        StandardSyncWindow.setWindowTitle(QCoreApplication.translate("StandardSyncWindow", u"Standard Sync", None))
        self.label_2.setText(QCoreApplication.translate("StandardSyncWindow", u"This tool compares any changes in an existing song database and writes an updated XML and .bpstat. If applicable, it also prompts you to copy and prepare any new songs that were not tracked in the XML previously or require a reprocess (e.g. a start/stop time change).", None))
        self.label.setText(QCoreApplication.translate("StandardSyncWindow", u"XML filepath", None))
        self.xml_browse_button.setText(QCoreApplication.translate("StandardSyncWindow", u"Browse", None))
        self.label_3.setText(QCoreApplication.translate("StandardSyncWindow", u".bpstat filepath", None))
        self.bpstat_browse_button.setText(QCoreApplication.translate("StandardSyncWindow", u"Browse", None))
        self.label_4.setText(QCoreApplication.translate("StandardSyncWindow", u"Database filepath", None))
        self.database_browse_button.setText(QCoreApplication.translate("StandardSyncWindow", u"Browse", None))
        self.load_all_button.setText(QCoreApplication.translate("StandardSyncWindow", u"Load", None))
#if QT_CONFIG(tooltip)
        self.calc_hashes_checkbox.setToolTip(QCoreApplication.translate("StandardSyncWindow", u"This will take some time and the screen will probably hang - only enable this if songs that should be marked as reprocessable aren't.", None))
#endif // QT_CONFIG(tooltip)
        self.calc_hashes_checkbox.setText(QCoreApplication.translate("StandardSyncWindow", u"Calculate file hashes", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("StandardSyncWindow", u"Statistics", None))
        self.tracks_indatabase_label.setText(QCoreApplication.translate("StandardSyncWindow", u"0 songs currently being tracked", None))
        self.tracks_copysize_label.setText(QCoreApplication.translate("StandardSyncWindow", u"0 MB to process", None))
        self.tracks_copycount_label.setText(QCoreApplication.translate("StandardSyncWindow", u"0 tracks to process", None))
        self.tracks_found_label.setText(QCoreApplication.translate("StandardSyncWindow", u"0 tracks found", None))
        self.tracks_synccount_label.setText(QCoreApplication.translate("StandardSyncWindow", u"0 songs to track", None))
        self.tracks_totalsize_label.setText(QCoreApplication.translate("StandardSyncWindow", u"0 MB total size", None))
        self.label_8.setText(QCoreApplication.translate("StandardSyncWindow", u"Songs changed", None))
        self.label_18.setText(QCoreApplication.translate("StandardSyncWindow", u"Search", None))
        self.label_11.setText(QCoreApplication.translate("StandardSyncWindow", u"New/modified songs", None))
        self.label_19.setText(QCoreApplication.translate("StandardSyncWindow", u"Search", None))
        self.groupBox.setTitle(QCoreApplication.translate("StandardSyncWindow", u"Options", None))
        self.show_ignored_songs_button.setText(QCoreApplication.translate("StandardSyncWindow", u"Show previously ignored songs", None))
        self.label_12.setText(QCoreApplication.translate("StandardSyncWindow", u"Data directory", None))
        self.data_browse_button.setText(QCoreApplication.translate("StandardSyncWindow", u"Browse", None))
        self.label_20.setText(QCoreApplication.translate("StandardSyncWindow", u"The newly generated .bpstat and XML will be sent here.", None))
        self.label_9.setText(QCoreApplication.translate("StandardSyncWindow", u"mp3 folder directory", None))
        self.mp3_browse_button.setText(QCoreApplication.translate("StandardSyncWindow", u"Browse", None))
        self.label_16.setText(QCoreApplication.translate("StandardSyncWindow", u"Any mp3s you have selected to be copied and renamed above will be sent to this folder.", None))
        self.label_10.setText(QCoreApplication.translate("StandardSyncWindow", u"Backup directory", None))
        self.backup_browse_button.setText(QCoreApplication.translate("StandardSyncWindow", u"Browse", None))
        self.label_17.setText(QCoreApplication.translate("StandardSyncWindow", u"Copies of your current XML, bpstat, and song database will be sent here.", None))
        self.start_button.setText(QCoreApplication.translate("StandardSyncWindow", u"Start processing", None))
    # retranslateUi

