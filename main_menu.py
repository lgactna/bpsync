# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_menu.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QPushButton,
    QSizePolicy, QWidget)

class Ui_MainMenuWindow(object):
    def setupUi(self, MainMenuWindow):
        if not MainMenuWindow.objectName():
            MainMenuWindow.setObjectName(u"MainMenuWindow")
        MainMenuWindow.resize(660, 245)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainMenuWindow.sizePolicy().hasHeightForWidth())
        MainMenuWindow.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(MainMenuWindow)
        self.gridLayout.setObjectName(u"gridLayout")
        self.launch_first_button = QPushButton(MainMenuWindow)
        self.launch_first_button.setObjectName(u"launch_first_button")
        self.launch_first_button.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout.addWidget(self.launch_first_button, 0, 0, 1, 1)

        self.label = QLabel(MainMenuWindow)
        self.label.setObjectName(u"label")
        self.label.setWordWrap(True)

        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)

        self.launch_std_button = QPushButton(MainMenuWindow)
        self.launch_std_button.setObjectName(u"launch_std_button")

        self.gridLayout.addWidget(self.launch_std_button, 1, 0, 1, 1)

        self.label_2 = QLabel(MainMenuWindow)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setWordWrap(True)

        self.gridLayout.addWidget(self.label_2, 1, 1, 1, 1)

        self.launch_bpstat_button = QPushButton(MainMenuWindow)
        self.launch_bpstat_button.setObjectName(u"launch_bpstat_button")
        self.launch_bpstat_button.setEnabled(False)

        self.gridLayout.addWidget(self.launch_bpstat_button, 2, 0, 1, 1)

        self.label_3 = QLabel(MainMenuWindow)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setWordWrap(True)

        self.gridLayout.addWidget(self.label_3, 2, 1, 1, 1)

        self.launch_m3u_button = QPushButton(MainMenuWindow)
        self.launch_m3u_button.setObjectName(u"launch_m3u_button")
        self.launch_m3u_button.setEnabled(False)

        self.gridLayout.addWidget(self.launch_m3u_button, 3, 0, 1, 1)

        self.label_4 = QLabel(MainMenuWindow)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setWordWrap(True)

        self.gridLayout.addWidget(self.label_4, 3, 1, 1, 1)


        self.retranslateUi(MainMenuWindow)

        QMetaObject.connectSlotsByName(MainMenuWindow)
    # setupUi

    def retranslateUi(self, MainMenuWindow):
        MainMenuWindow.setWindowTitle(QCoreApplication.translate("MainMenuWindow", u"bpsync", None))
        self.launch_first_button.setText(QCoreApplication.translate("MainMenuWindow", u"First-time sync", None))
        self.label.setText(QCoreApplication.translate("MainMenuWindow", u"Start here if you need to create the song database. Can also be used to process songs without tracking them if needed.", None))
        self.launch_std_button.setText(QCoreApplication.translate("MainMenuWindow", u"Standard sync", None))
        self.label_2.setText(QCoreApplication.translate("MainMenuWindow", u"Use this if you have a song database.", None))
        self.launch_bpstat_button.setText(QCoreApplication.translate("MainMenuWindow", u".bpstat to XML converter", None))
        self.label_3.setText(QCoreApplication.translate("MainMenuWindow", u"Convert a .bpstat file into an iTunes XML file.", None))
        self.launch_m3u_button.setText(QCoreApplication.translate("MainMenuWindow", u"Generate .m3u", None))
        self.label_4.setText(QCoreApplication.translate("MainMenuWindow", u"Generate an m3u file for playlists that's importable into BlackPlayer.", None))
    # retranslateUi

