# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ignored_songs.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QHBoxLayout, QLabel, QLineEdit, QSizePolicy,
    QVBoxLayout, QWidget)

from bpsyncwidgets import SongView

class Ui_IgnoredSongsDialog(object):
    def setupUi(self, IgnoredSongsDialog):
        if not IgnoredSongsDialog.objectName():
            IgnoredSongsDialog.setObjectName(u"IgnoredSongsDialog")
        IgnoredSongsDialog.resize(551, 304)
        self.verticalLayout = QVBoxLayout(IgnoredSongsDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(IgnoredSongsDialog)
        self.label.setObjectName(u"label")
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)

        self.ignored_song_table = SongView(IgnoredSongsDialog)
        self.ignored_song_table.setObjectName(u"ignored_song_table")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ignored_song_table.sizePolicy().hasHeightForWidth())
        self.ignored_song_table.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.ignored_song_table)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(IgnoredSongsDialog)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.ignored_songs_lineedit = QLineEdit(IgnoredSongsDialog)
        self.ignored_songs_lineedit.setObjectName(u"ignored_songs_lineedit")

        self.horizontalLayout_2.addWidget(self.ignored_songs_lineedit)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.buttonBox = QDialogButtonBox(IgnoredSongsDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(IgnoredSongsDialog)
        self.buttonBox.accepted.connect(IgnoredSongsDialog.accept)
        self.buttonBox.rejected.connect(IgnoredSongsDialog.reject)

        QMetaObject.connectSlotsByName(IgnoredSongsDialog)
    # setupUi

    def retranslateUi(self, IgnoredSongsDialog):
        IgnoredSongsDialog.setWindowTitle(QCoreApplication.translate("IgnoredSongsDialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("IgnoredSongsDialog", u"If you've previously had the option to track songs and did not track them, they won't show up in future syncs to keep the new songs list from being cluttered. You can readd them to the \"new songs\" list by checking them here and clicking OK.", None))
        self.label_2.setText(QCoreApplication.translate("IgnoredSongsDialog", u"Search", None))
    # retranslateUi

