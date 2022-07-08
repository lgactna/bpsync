# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'song_info.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractSpinBox, QApplication, QCheckBox,
    QDateTimeEdit, QDialog, QDialogButtonBox, QFormLayout,
    QFrame, QHBoxLayout, QLabel, QLayout,
    QLineEdit, QPushButton, QSizePolicy, QSpinBox,
    QVBoxLayout, QWidget)

class Ui_SongInfoDialog(object):
    def setupUi(self, SongInfoDialog):
        if not SongInfoDialog.objectName():
            SongInfoDialog.setObjectName(u"SongInfoDialog")
        SongInfoDialog.resize(669, 466)
        SongInfoDialog.setStyleSheet(u"QLineEdit, QSpinBox{\n"
"	background:transparent;\n"
"	border:transparent;\n"
"}\n"
"\n"
"QLineEdit:focus, QSpinBox:focus{\n"
"	background:white;\n"
"	border: 1px solid gray;\n"
"}")
        self.verticalLayout_4 = QVBoxLayout(SongInfoDialog)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_19 = QLabel(SongInfoDialog)
        self.label_19.setObjectName(u"label_19")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy)
        self.label_19.setMinimumSize(QSize(0, 30))
        self.label_19.setMaximumSize(QSize(16777215, 30))
        self.label_19.setStyleSheet(u"QTextEdit{\n"
"background:transparent\n"
"}")
        self.label_19.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.label_19)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.songImageLabel = QLabel(SongInfoDialog)
        self.songImageLabel.setObjectName(u"songImageLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.songImageLabel.sizePolicy().hasHeightForWidth())
        self.songImageLabel.setSizePolicy(sizePolicy1)
        self.songImageLabel.setMinimumSize(QSize(160, 160))
        self.songImageLabel.setMaximumSize(QSize(160, 160))

        self.verticalLayout_3.addWidget(self.songImageLabel)

        self.pushButton = QPushButton(SongInfoDialog)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setEnabled(False)

        self.verticalLayout_3.addWidget(self.pushButton)


        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setFormAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.titleLabel = QLabel(SongInfoDialog)
        self.titleLabel.setObjectName(u"titleLabel")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.titleLabel)

        self.titleLineEdit = QLineEdit(SongInfoDialog)
        self.titleLineEdit.setObjectName(u"titleLineEdit")
        self.titleLineEdit.setStyleSheet(u"")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.titleLineEdit)

        self.artistLabel = QLabel(SongInfoDialog)
        self.artistLabel.setObjectName(u"artistLabel")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.artistLabel)

        self.artistLineEdit = QLineEdit(SongInfoDialog)
        self.artistLineEdit.setObjectName(u"artistLineEdit")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.artistLineEdit)

        self.albumLabel = QLabel(SongInfoDialog)
        self.albumLabel.setObjectName(u"albumLabel")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.albumLabel)

        self.albumLineEdit = QLineEdit(SongInfoDialog)
        self.albumLineEdit.setObjectName(u"albumLineEdit")

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.albumLineEdit)

        self.yearLabel = QLabel(SongInfoDialog)
        self.yearLabel.setObjectName(u"yearLabel")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.yearLabel)

        self.yearSpinBox = QSpinBox(SongInfoDialog)
        self.yearSpinBox.setObjectName(u"yearSpinBox")
        self.yearSpinBox.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.yearSpinBox)

        self.genreLabel = QLabel(SongInfoDialog)
        self.genreLabel.setObjectName(u"genreLabel")

        self.formLayout_2.setWidget(4, QFormLayout.LabelRole, self.genreLabel)

        self.genreLineEdit = QLineEdit(SongInfoDialog)
        self.genreLineEdit.setObjectName(u"genreLineEdit")

        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.genreLineEdit)


        self.horizontalLayout.addLayout(self.formLayout_2)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.formLayout_3 = QFormLayout()
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.formLayout_3.setFormAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.trackIDLabel = QLabel(SongInfoDialog)
        self.trackIDLabel.setObjectName(u"trackIDLabel")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.trackIDLabel)

        self.trackIDLineEdit = QLineEdit(SongInfoDialog)
        self.trackIDLineEdit.setObjectName(u"trackIDLineEdit")
        self.trackIDLineEdit.setReadOnly(True)

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.trackIDLineEdit)

        self.persistentIDLabel = QLabel(SongInfoDialog)
        self.persistentIDLabel.setObjectName(u"persistentIDLabel")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.persistentIDLabel)

        self.persistentIDLineEdit = QLineEdit(SongInfoDialog)
        self.persistentIDLineEdit.setObjectName(u"persistentIDLineEdit")
        self.persistentIDLineEdit.setReadOnly(True)

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.persistentIDLineEdit)

        self.locationLabel = QLabel(SongInfoDialog)
        self.locationLabel.setObjectName(u"locationLabel")

        self.formLayout_3.setWidget(2, QFormLayout.LabelRole, self.locationLabel)

        self.locationLineEdit = QLineEdit(SongInfoDialog)
        self.locationLineEdit.setObjectName(u"locationLineEdit")
        self.locationLineEdit.setReadOnly(True)

        self.formLayout_3.setWidget(2, QFormLayout.FieldRole, self.locationLineEdit)


        self.verticalLayout_2.addLayout(self.formLayout_3)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SetMinAndMaxSize)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout_4 = QFormLayout()
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.formLayout_4.setVerticalSpacing(9)
        self.label_13 = QLabel(SongInfoDialog)
        self.label_13.setObjectName(u"label_13")

        self.formLayout_4.setWidget(0, QFormLayout.LabelRole, self.label_13)

        self.sizeLabel = QLabel(SongInfoDialog)
        self.sizeLabel.setObjectName(u"sizeLabel")
        self.sizeLabel.setMinimumSize(QSize(87, 0))
        self.sizeLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout_4.setWidget(0, QFormLayout.FieldRole, self.sizeLabel)

        self.label_16 = QLabel(SongInfoDialog)
        self.label_16.setObjectName(u"label_16")

        self.formLayout_4.setWidget(1, QFormLayout.LabelRole, self.label_16)

        self.totalLengthLabel = QLabel(SongInfoDialog)
        self.totalLengthLabel.setObjectName(u"totalLengthLabel")
        self.totalLengthLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout_4.setWidget(1, QFormLayout.FieldRole, self.totalLengthLabel)

        self.label_14 = QLabel(SongInfoDialog)
        self.label_14.setObjectName(u"label_14")

        self.formLayout_4.setWidget(2, QFormLayout.LabelRole, self.label_14)

        self.trackTypeLabel = QLabel(SongInfoDialog)
        self.trackTypeLabel.setObjectName(u"trackTypeLabel")
        self.trackTypeLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout_4.setWidget(2, QFormLayout.FieldRole, self.trackTypeLabel)

        self.label_3 = QLabel(SongInfoDialog)
        self.label_3.setObjectName(u"label_3")

        self.formLayout_4.setWidget(3, QFormLayout.LabelRole, self.label_3)

        self.bpmLabel = QLabel(SongInfoDialog)
        self.bpmLabel.setObjectName(u"bpmLabel")
        self.bpmLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout_4.setWidget(3, QFormLayout.FieldRole, self.bpmLabel)

        self.label_5 = QLabel(SongInfoDialog)
        self.label_5.setObjectName(u"label_5")

        self.formLayout_4.setWidget(4, QFormLayout.LabelRole, self.label_5)

        self.dateModifiedLabel = QLabel(SongInfoDialog)
        self.dateModifiedLabel.setObjectName(u"dateModifiedLabel")
        self.dateModifiedLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout_4.setWidget(4, QFormLayout.FieldRole, self.dateModifiedLabel)

        self.label_6 = QLabel(SongInfoDialog)
        self.label_6.setObjectName(u"label_6")

        self.formLayout_4.setWidget(5, QFormLayout.LabelRole, self.label_6)

        self.dateAddedLabel = QLabel(SongInfoDialog)
        self.dateAddedLabel.setObjectName(u"dateAddedLabel")
        self.dateAddedLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout_4.setWidget(5, QFormLayout.FieldRole, self.dateAddedLabel)

        self.label_7 = QLabel(SongInfoDialog)
        self.label_7.setObjectName(u"label_7")

        self.formLayout_4.setWidget(6, QFormLayout.LabelRole, self.label_7)

        self.bitrateLabel = QLabel(SongInfoDialog)
        self.bitrateLabel.setObjectName(u"bitrateLabel")
        self.bitrateLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout_4.setWidget(6, QFormLayout.FieldRole, self.bitrateLabel)

        self.sampleRateLabel = QLabel(SongInfoDialog)
        self.sampleRateLabel.setObjectName(u"sampleRateLabel")
        self.sampleRateLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout_4.setWidget(7, QFormLayout.FieldRole, self.sampleRateLabel)

        self.label_8 = QLabel(SongInfoDialog)
        self.label_8.setObjectName(u"label_8")

        self.formLayout_4.setWidget(7, QFormLayout.LabelRole, self.label_8)


        self.verticalLayout.addLayout(self.formLayout_4)


        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.line = QFrame(SongInfoDialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_2.addWidget(self.line)

        self.formLayout_5 = QFormLayout()
        self.formLayout_5.setObjectName(u"formLayout_5")
        self.startTimeLabel = QLabel(SongInfoDialog)
        self.startTimeLabel.setObjectName(u"startTimeLabel")

        self.formLayout_5.setWidget(0, QFormLayout.LabelRole, self.startTimeLabel)

        self.startTimeSpinBox = QSpinBox(SongInfoDialog)
        self.startTimeSpinBox.setObjectName(u"startTimeSpinBox")
        self.startTimeSpinBox.setMinimumSize(QSize(120, 0))
        self.startTimeSpinBox.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.formLayout_5.setWidget(0, QFormLayout.FieldRole, self.startTimeSpinBox)

        self.stopTimeLabel = QLabel(SongInfoDialog)
        self.stopTimeLabel.setObjectName(u"stopTimeLabel")

        self.formLayout_5.setWidget(1, QFormLayout.LabelRole, self.stopTimeLabel)

        self.stopTimeSpinBox = QSpinBox(SongInfoDialog)
        self.stopTimeSpinBox.setObjectName(u"stopTimeSpinBox")
        self.stopTimeSpinBox.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.formLayout_5.setWidget(1, QFormLayout.FieldRole, self.stopTimeSpinBox)

        self.discNumberLabel = QLabel(SongInfoDialog)
        self.discNumberLabel.setObjectName(u"discNumberLabel")

        self.formLayout_5.setWidget(2, QFormLayout.LabelRole, self.discNumberLabel)

        self.discNumberSpinBox = QSpinBox(SongInfoDialog)
        self.discNumberSpinBox.setObjectName(u"discNumberSpinBox")
        self.discNumberSpinBox.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.formLayout_5.setWidget(2, QFormLayout.FieldRole, self.discNumberSpinBox)

        self.discCountLabel = QLabel(SongInfoDialog)
        self.discCountLabel.setObjectName(u"discCountLabel")

        self.formLayout_5.setWidget(3, QFormLayout.LabelRole, self.discCountLabel)

        self.discCountSpinBox = QSpinBox(SongInfoDialog)
        self.discCountSpinBox.setObjectName(u"discCountSpinBox")
        self.discCountSpinBox.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.formLayout_5.setWidget(3, QFormLayout.FieldRole, self.discCountSpinBox)

        self.trackNumberLabel = QLabel(SongInfoDialog)
        self.trackNumberLabel.setObjectName(u"trackNumberLabel")

        self.formLayout_5.setWidget(4, QFormLayout.LabelRole, self.trackNumberLabel)

        self.trackNumberSpinBox = QSpinBox(SongInfoDialog)
        self.trackNumberSpinBox.setObjectName(u"trackNumberSpinBox")
        self.trackNumberSpinBox.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.formLayout_5.setWidget(4, QFormLayout.FieldRole, self.trackNumberSpinBox)

        self.trackCountLabel = QLabel(SongInfoDialog)
        self.trackCountLabel.setObjectName(u"trackCountLabel")

        self.formLayout_5.setWidget(5, QFormLayout.LabelRole, self.trackCountLabel)

        self.trackCountSpinBox = QSpinBox(SongInfoDialog)
        self.trackCountSpinBox.setObjectName(u"trackCountSpinBox")
        self.trackCountSpinBox.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.formLayout_5.setWidget(5, QFormLayout.FieldRole, self.trackCountSpinBox)

        self.ratingComputedLabel = QLabel(SongInfoDialog)
        self.ratingComputedLabel.setObjectName(u"ratingComputedLabel")

        self.formLayout_5.setWidget(6, QFormLayout.LabelRole, self.ratingComputedLabel)

        self.ratingComputedCheckBox = QCheckBox(SongInfoDialog)
        self.ratingComputedCheckBox.setObjectName(u"ratingComputedCheckBox")

        self.formLayout_5.setWidget(6, QFormLayout.FieldRole, self.ratingComputedCheckBox)

        self.compilationLabel = QLabel(SongInfoDialog)
        self.compilationLabel.setObjectName(u"compilationLabel")

        self.formLayout_5.setWidget(7, QFormLayout.LabelRole, self.compilationLabel)

        self.compilationCheckBox = QCheckBox(SongInfoDialog)
        self.compilationCheckBox.setObjectName(u"compilationCheckBox")

        self.formLayout_5.setWidget(7, QFormLayout.FieldRole, self.compilationCheckBox)


        self.horizontalLayout_2.addLayout(self.formLayout_5)

        self.line_2 = QFrame(SongInfoDialog)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_2.addWidget(self.line_2)

        self.formLayout_6 = QFormLayout()
        self.formLayout_6.setObjectName(u"formLayout_6")
        self.volumeAdjustmentLabel = QLabel(SongInfoDialog)
        self.volumeAdjustmentLabel.setObjectName(u"volumeAdjustmentLabel")
        font = QFont()
        font.setUnderline(True)
        self.volumeAdjustmentLabel.setFont(font)

        self.formLayout_6.setWidget(0, QFormLayout.LabelRole, self.volumeAdjustmentLabel)

        self.volumeAdjustmentSpinBox = QSpinBox(SongInfoDialog)
        self.volumeAdjustmentSpinBox.setObjectName(u"volumeAdjustmentSpinBox")
        self.volumeAdjustmentSpinBox.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.volumeAdjustmentSpinBox.setMinimum(-1024)
        self.volumeAdjustmentSpinBox.setMaximum(1024)

        self.formLayout_6.setWidget(0, QFormLayout.FieldRole, self.volumeAdjustmentSpinBox)

        self.playCountLabel = QLabel(SongInfoDialog)
        self.playCountLabel.setObjectName(u"playCountLabel")

        self.formLayout_6.setWidget(1, QFormLayout.LabelRole, self.playCountLabel)

        self.playCountSpinBox = QSpinBox(SongInfoDialog)
        self.playCountSpinBox.setObjectName(u"playCountSpinBox")
        self.playCountSpinBox.setReadOnly(True)
        self.playCountSpinBox.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.formLayout_6.setWidget(1, QFormLayout.FieldRole, self.playCountSpinBox)

        self.lastPlayedLabel = QLabel(SongInfoDialog)
        self.lastPlayedLabel.setObjectName(u"lastPlayedLabel")

        self.formLayout_6.setWidget(2, QFormLayout.LabelRole, self.lastPlayedLabel)

        self.lastPlayedDateTimeEdit = QDateTimeEdit(SongInfoDialog)
        self.lastPlayedDateTimeEdit.setObjectName(u"lastPlayedDateTimeEdit")
        self.lastPlayedDateTimeEdit.setCalendarPopup(True)

        self.formLayout_6.setWidget(2, QFormLayout.FieldRole, self.lastPlayedDateTimeEdit)

        self.skipCountLabel = QLabel(SongInfoDialog)
        self.skipCountLabel.setObjectName(u"skipCountLabel")

        self.formLayout_6.setWidget(3, QFormLayout.LabelRole, self.skipCountLabel)

        self.skipCountSpinBox = QSpinBox(SongInfoDialog)
        self.skipCountSpinBox.setObjectName(u"skipCountSpinBox")
        self.skipCountSpinBox.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.formLayout_6.setWidget(3, QFormLayout.FieldRole, self.skipCountSpinBox)

        self.lastSkippedLabel = QLabel(SongInfoDialog)
        self.lastSkippedLabel.setObjectName(u"lastSkippedLabel")

        self.formLayout_6.setWidget(4, QFormLayout.LabelRole, self.lastSkippedLabel)

        self.albumRatingLabel = QLabel(SongInfoDialog)
        self.albumRatingLabel.setObjectName(u"albumRatingLabel")

        self.formLayout_6.setWidget(5, QFormLayout.LabelRole, self.albumRatingLabel)

        self.albumRatingSpinBox = QSpinBox(SongInfoDialog)
        self.albumRatingSpinBox.setObjectName(u"albumRatingSpinBox")
        self.albumRatingSpinBox.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.formLayout_6.setWidget(5, QFormLayout.FieldRole, self.albumRatingSpinBox)

        self.lovedLabel = QLabel(SongInfoDialog)
        self.lovedLabel.setObjectName(u"lovedLabel")

        self.formLayout_6.setWidget(6, QFormLayout.LabelRole, self.lovedLabel)

        self.lovedCheckBox = QCheckBox(SongInfoDialog)
        self.lovedCheckBox.setObjectName(u"lovedCheckBox")

        self.formLayout_6.setWidget(6, QFormLayout.FieldRole, self.lovedCheckBox)

        self.dislikedLabel = QLabel(SongInfoDialog)
        self.dislikedLabel.setObjectName(u"dislikedLabel")

        self.formLayout_6.setWidget(7, QFormLayout.LabelRole, self.dislikedLabel)

        self.dislikedCheckBox = QCheckBox(SongInfoDialog)
        self.dislikedCheckBox.setObjectName(u"dislikedCheckBox")

        self.formLayout_6.setWidget(7, QFormLayout.FieldRole, self.dislikedCheckBox)

        self.lastSkippedDateTimeEdit = QDateTimeEdit(SongInfoDialog)
        self.lastSkippedDateTimeEdit.setObjectName(u"lastSkippedDateTimeEdit")
        self.lastSkippedDateTimeEdit.setProperty("showGroupSeparator", False)
        self.lastSkippedDateTimeEdit.setCalendarPopup(True)

        self.formLayout_6.setWidget(4, QFormLayout.FieldRole, self.lastSkippedDateTimeEdit)


        self.horizontalLayout_2.addLayout(self.formLayout_6)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.buttonBox = QDialogButtonBox(SongInfoDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout_4.addWidget(self.buttonBox)


        self.retranslateUi(SongInfoDialog)
        self.buttonBox.accepted.connect(SongInfoDialog.accept)
        self.buttonBox.rejected.connect(SongInfoDialog.reject)

        QMetaObject.connectSlotsByName(SongInfoDialog)
    # setupUi

    def retranslateUi(self, SongInfoDialog):
        SongInfoDialog.setWindowTitle(QCoreApplication.translate("SongInfoDialog", u"Song information: {song.name} - {song.artist}", None))
        self.label_19.setText(QCoreApplication.translate("SongInfoDialog", u"You can change certain fields here directly by clicking OK after making changes. Note that some changes may not persist in a produced MP3 or in iTunes. ", None))
        self.songImageLabel.setText("")
        self.pushButton.setText(QCoreApplication.translate("SongInfoDialog", u"Change image", None))
        self.titleLabel.setText(QCoreApplication.translate("SongInfoDialog", u"Title", None))
#if QT_CONFIG(whatsthis)
        self.titleLineEdit.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.artistLabel.setText(QCoreApplication.translate("SongInfoDialog", u"Artist", None))
        self.albumLabel.setText(QCoreApplication.translate("SongInfoDialog", u"Album", None))
        self.yearLabel.setText(QCoreApplication.translate("SongInfoDialog", u"Year", None))
        self.genreLabel.setText(QCoreApplication.translate("SongInfoDialog", u"Genre", None))
        self.trackIDLabel.setText(QCoreApplication.translate("SongInfoDialog", u"Track ID", None))
        self.trackIDLineEdit.setText("")
        self.persistentIDLabel.setText(QCoreApplication.translate("SongInfoDialog", u"Persistent ID", None))
        self.locationLabel.setText(QCoreApplication.translate("SongInfoDialog", u"Location", None))
        self.label_13.setText(QCoreApplication.translate("SongInfoDialog", u"Size", None))
        self.sizeLabel.setText(QCoreApplication.translate("SongInfoDialog", u"TextLabel", None))
        self.label_16.setText(QCoreApplication.translate("SongInfoDialog", u"Total length", None))
        self.totalLengthLabel.setText(QCoreApplication.translate("SongInfoDialog", u"TextLabel", None))
        self.label_14.setText(QCoreApplication.translate("SongInfoDialog", u"Track type", None))
        self.trackTypeLabel.setText(QCoreApplication.translate("SongInfoDialog", u"TextLabel", None))
        self.label_3.setText(QCoreApplication.translate("SongInfoDialog", u"BPM", None))
        self.bpmLabel.setText(QCoreApplication.translate("SongInfoDialog", u"TextLabel", None))
        self.label_5.setText(QCoreApplication.translate("SongInfoDialog", u"Date modified", None))
        self.dateModifiedLabel.setText(QCoreApplication.translate("SongInfoDialog", u"TextLabel", None))
        self.label_6.setText(QCoreApplication.translate("SongInfoDialog", u"Date added", None))
        self.dateAddedLabel.setText(QCoreApplication.translate("SongInfoDialog", u"TextLabel", None))
        self.label_7.setText(QCoreApplication.translate("SongInfoDialog", u"Bitrate", None))
        self.bitrateLabel.setText(QCoreApplication.translate("SongInfoDialog", u"TextLabel", None))
        self.sampleRateLabel.setText(QCoreApplication.translate("SongInfoDialog", u"TextLabel", None))
        self.label_8.setText(QCoreApplication.translate("SongInfoDialog", u"Sample rate", None))
        self.startTimeLabel.setText(QCoreApplication.translate("SongInfoDialog", u"Start time", None))
        self.stopTimeLabel.setText(QCoreApplication.translate("SongInfoDialog", u"Stop time", None))
        self.discNumberLabel.setText(QCoreApplication.translate("SongInfoDialog", u"Disc number", None))
        self.discCountLabel.setText(QCoreApplication.translate("SongInfoDialog", u"Disc count", None))
        self.trackNumberLabel.setText(QCoreApplication.translate("SongInfoDialog", u"Track number", None))
        self.trackCountLabel.setText(QCoreApplication.translate("SongInfoDialog", u"Track count", None))
        self.ratingComputedLabel.setText(QCoreApplication.translate("SongInfoDialog", u"Rating computed", None))
        self.compilationLabel.setText(QCoreApplication.translate("SongInfoDialog", u"Compilation", None))
#if QT_CONFIG(tooltip)
        self.volumeAdjustmentLabel.setToolTip(QCoreApplication.translate("SongInfoDialog", u"iTunes normally stores this value from -255 to 255. You can set it from -255 to 1024 here, which is equivalent to a 400% volume increase.", None))
#endif // QT_CONFIG(tooltip)
        self.volumeAdjustmentLabel.setText(QCoreApplication.translate("SongInfoDialog", u"Volume adjustment", None))
#if QT_CONFIG(tooltip)
        self.volumeAdjustmentSpinBox.setToolTip(QCoreApplication.translate("SongInfoDialog", u"iTunes normally stores this value from -255 to 255. You can set it from -255 to 1024 here, which is equivalent to a 400% volume increase.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.playCountLabel.setToolTip(QCoreApplication.translate("SongInfoDialog", u"This value is not editable.", None))
#endif // QT_CONFIG(tooltip)
        self.playCountLabel.setText(QCoreApplication.translate("SongInfoDialog", u"Play count", None))
#if QT_CONFIG(tooltip)
        self.playCountSpinBox.setToolTip(QCoreApplication.translate("SongInfoDialog", u"This value is not editable.", None))
#endif // QT_CONFIG(tooltip)
        self.lastPlayedLabel.setText(QCoreApplication.translate("SongInfoDialog", u"Last played", None))
        self.skipCountLabel.setText(QCoreApplication.translate("SongInfoDialog", u"Skip count", None))
        self.lastSkippedLabel.setText(QCoreApplication.translate("SongInfoDialog", u"Last skipped", None))
        self.albumRatingLabel.setText(QCoreApplication.translate("SongInfoDialog", u"Album rating", None))
        self.lovedLabel.setText(QCoreApplication.translate("SongInfoDialog", u"Loved", None))
        self.dislikedLabel.setText(QCoreApplication.translate("SongInfoDialog", u"Disliked", None))
    # retranslateUi

