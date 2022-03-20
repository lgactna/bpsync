# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'progress.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPlainTextEdit,
    QProgressBar, QSizePolicy, QVBoxLayout, QWidget)

class Ui_ProcessingProgress(object):
    def setupUi(self, ProcessingProgress):
        if not ProcessingProgress.objectName():
            ProcessingProgress.setObjectName(u"ProcessingProgress")
        ProcessingProgress.resize(400, 300)
        self.verticalLayout = QVBoxLayout(ProcessingProgress)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.progress_bar = QProgressBar(ProcessingProgress)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setInvertedAppearance(False)

        self.verticalLayout.addWidget(self.progress_bar)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.song_label = QLabel(ProcessingProgress)
        self.song_label.setObjectName(u"song_label")
        self.song_label.setWordWrap(True)

        self.horizontalLayout.addWidget(self.song_label)

        self.progress_label = QLabel(ProcessingProgress)
        self.progress_label.setObjectName(u"progress_label")
        self.progress_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.progress_label)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.log_box = QPlainTextEdit(ProcessingProgress)
        self.log_box.setObjectName(u"log_box")
        self.log_box.setReadOnly(True)

        self.verticalLayout.addWidget(self.log_box)


        self.retranslateUi(ProcessingProgress)

        QMetaObject.connectSlotsByName(ProcessingProgress)
    # setupUi

    def retranslateUi(self, ProcessingProgress):
        ProcessingProgress.setWindowTitle(QCoreApplication.translate("ProcessingProgress", u"Processing songs", None))
        self.song_label.setText(QCoreApplication.translate("ProcessingProgress", u"Seiryu - BLUE DRAGON", None))
        self.progress_label.setText(QCoreApplication.translate("ProcessingProgress", u"(0/727)", None))
    # retranslateUi

