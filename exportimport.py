# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'exportimport.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFormLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_ExportImportWindow(object):
    def setupUi(self, ExportImportWindow):
        if not ExportImportWindow.objectName():
            ExportImportWindow.setObjectName(u"ExportImportWindow")
        ExportImportWindow.resize(727, 365)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ExportImportWindow.sizePolicy().hasHeightForWidth())
        ExportImportWindow.setSizePolicy(sizePolicy)
        ExportImportWindow.setMinimumSize(QSize(727, 365))
        ExportImportWindow.setMaximumSize(QSize(727, 365))
        self.verticalLayout = QVBoxLayout(ExportImportWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_2 = QLabel(ExportImportWindow)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(16777215, 20))
        self.label_2.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_2)

        self.label_3 = QLabel(ExportImportWindow)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(16777215, 20))
        self.label_3.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.label = QLabel(ExportImportWindow)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.xml_path_lineedit = QLineEdit(ExportImportWindow)
        self.xml_path_lineedit.setObjectName(u"xml_path_lineedit")

        self.horizontalLayout.addWidget(self.xml_path_lineedit)

        self.xml_browse_button = QPushButton(ExportImportWindow)
        self.xml_browse_button.setObjectName(u"xml_browse_button")

        self.horizontalLayout.addWidget(self.xml_browse_button)

        self.xml_load_button = QPushButton(ExportImportWindow)
        self.xml_load_button.setObjectName(u"xml_load_button")

        self.horizontalLayout.addWidget(self.xml_load_button)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.songsLoadedLabel = QLabel(ExportImportWindow)
        self.songsLoadedLabel.setObjectName(u"songsLoadedLabel")
        self.songsLoadedLabel.setMaximumSize(QSize(16777215, 20))
        font = QFont()
        font.setBold(True)
        self.songsLoadedLabel.setFont(font)
        self.songsLoadedLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.songsLoadedLabel)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.formLayout_11 = QFormLayout()
        self.formLayout_11.setObjectName(u"formLayout_11")
        self.locationLabel = QLabel(ExportImportWindow)
        self.locationLabel.setObjectName(u"locationLabel")

        self.formLayout_11.setWidget(0, QFormLayout.LabelRole, self.locationLabel)

        self.locationCheckBox = QCheckBox(ExportImportWindow)
        self.locationCheckBox.setObjectName(u"locationCheckBox")

        self.formLayout_11.setWidget(0, QFormLayout.FieldRole, self.locationCheckBox)

        self.dateAddedLabel = QLabel(ExportImportWindow)
        self.dateAddedLabel.setObjectName(u"dateAddedLabel")

        self.formLayout_11.setWidget(1, QFormLayout.LabelRole, self.dateAddedLabel)

        self.dateAddedCheckBox = QCheckBox(ExportImportWindow)
        self.dateAddedCheckBox.setObjectName(u"dateAddedCheckBox")

        self.formLayout_11.setWidget(1, QFormLayout.FieldRole, self.dateAddedCheckBox)

        self.nameLabel = QLabel(ExportImportWindow)
        self.nameLabel.setObjectName(u"nameLabel")

        self.formLayout_11.setWidget(2, QFormLayout.LabelRole, self.nameLabel)

        self.nameCheckBox = QCheckBox(ExportImportWindow)
        self.nameCheckBox.setObjectName(u"nameCheckBox")

        self.formLayout_11.setWidget(2, QFormLayout.FieldRole, self.nameCheckBox)

        self.sortNameLabel = QLabel(ExportImportWindow)
        self.sortNameLabel.setObjectName(u"sortNameLabel")

        self.formLayout_11.setWidget(3, QFormLayout.LabelRole, self.sortNameLabel)

        self.sortNameCheckBox = QCheckBox(ExportImportWindow)
        self.sortNameCheckBox.setObjectName(u"sortNameCheckBox")
        self.sortNameCheckBox.setEnabled(False)

        self.formLayout_11.setWidget(3, QFormLayout.FieldRole, self.sortNameCheckBox)

        self.albumLabel = QLabel(ExportImportWindow)
        self.albumLabel.setObjectName(u"albumLabel")

        self.formLayout_11.setWidget(4, QFormLayout.LabelRole, self.albumLabel)

        self.albumCheckBox = QCheckBox(ExportImportWindow)
        self.albumCheckBox.setObjectName(u"albumCheckBox")

        self.formLayout_11.setWidget(4, QFormLayout.FieldRole, self.albumCheckBox)

        self.sortAlbumLabel = QLabel(ExportImportWindow)
        self.sortAlbumLabel.setObjectName(u"sortAlbumLabel")

        self.formLayout_11.setWidget(5, QFormLayout.LabelRole, self.sortAlbumLabel)

        self.sortAlbumCheckBox = QCheckBox(ExportImportWindow)
        self.sortAlbumCheckBox.setObjectName(u"sortAlbumCheckBox")

        self.formLayout_11.setWidget(5, QFormLayout.FieldRole, self.sortAlbumCheckBox)

        self.albumArtistLabel = QLabel(ExportImportWindow)
        self.albumArtistLabel.setObjectName(u"albumArtistLabel")

        self.formLayout_11.setWidget(6, QFormLayout.LabelRole, self.albumArtistLabel)

        self.albumArtistCheckBox = QCheckBox(ExportImportWindow)
        self.albumArtistCheckBox.setObjectName(u"albumArtistCheckBox")

        self.formLayout_11.setWidget(6, QFormLayout.FieldRole, self.albumArtistCheckBox)

        self.sortAlbumArtistLabel = QLabel(ExportImportWindow)
        self.sortAlbumArtistLabel.setObjectName(u"sortAlbumArtistLabel")

        self.formLayout_11.setWidget(7, QFormLayout.LabelRole, self.sortAlbumArtistLabel)

        self.sortAlbumArtistCheckBox = QCheckBox(ExportImportWindow)
        self.sortAlbumArtistCheckBox.setObjectName(u"sortAlbumArtistCheckBox")
        self.sortAlbumArtistCheckBox.setEnabled(False)

        self.formLayout_11.setWidget(7, QFormLayout.FieldRole, self.sortAlbumArtistCheckBox)

        self.artistLabel = QLabel(ExportImportWindow)
        self.artistLabel.setObjectName(u"artistLabel")

        self.formLayout_11.setWidget(8, QFormLayout.LabelRole, self.artistLabel)

        self.artistCheckBox = QCheckBox(ExportImportWindow)
        self.artistCheckBox.setObjectName(u"artistCheckBox")

        self.formLayout_11.setWidget(8, QFormLayout.FieldRole, self.artistCheckBox)


        self.horizontalLayout_2.addLayout(self.formLayout_11)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.sortArtistLabel = QLabel(ExportImportWindow)
        self.sortArtistLabel.setObjectName(u"sortArtistLabel")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.sortArtistLabel)

        self.sortArtistCheckBox = QCheckBox(ExportImportWindow)
        self.sortArtistCheckBox.setObjectName(u"sortArtistCheckBox")
        self.sortArtistCheckBox.setEnabled(False)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.sortArtistCheckBox)

        self.composerLabel = QLabel(ExportImportWindow)
        self.composerLabel.setObjectName(u"composerLabel")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.composerLabel)

        self.composerCheckBox = QCheckBox(ExportImportWindow)
        self.composerCheckBox.setObjectName(u"composerCheckBox")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.composerCheckBox)

        self.sortComposerLabel = QLabel(ExportImportWindow)
        self.sortComposerLabel.setObjectName(u"sortComposerLabel")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.sortComposerLabel)

        self.sortComposerCheckBox = QCheckBox(ExportImportWindow)
        self.sortComposerCheckBox.setObjectName(u"sortComposerCheckBox")
        self.sortComposerCheckBox.setEnabled(False)

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.sortComposerCheckBox)

        self.groupingLabel = QLabel(ExportImportWindow)
        self.groupingLabel.setObjectName(u"groupingLabel")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.groupingLabel)

        self.groupingCheckBox = QCheckBox(ExportImportWindow)
        self.groupingCheckBox.setObjectName(u"groupingCheckBox")

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.groupingCheckBox)

        self.genreLabel = QLabel(ExportImportWindow)
        self.genreLabel.setObjectName(u"genreLabel")

        self.formLayout_2.setWidget(4, QFormLayout.LabelRole, self.genreLabel)

        self.genreCheckBox = QCheckBox(ExportImportWindow)
        self.genreCheckBox.setObjectName(u"genreCheckBox")

        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.genreCheckBox)

        self.compilationLabel = QLabel(ExportImportWindow)
        self.compilationLabel.setObjectName(u"compilationLabel")

        self.formLayout_2.setWidget(5, QFormLayout.LabelRole, self.compilationLabel)

        self.compilationCheckBox = QCheckBox(ExportImportWindow)
        self.compilationCheckBox.setObjectName(u"compilationCheckBox")

        self.formLayout_2.setWidget(5, QFormLayout.FieldRole, self.compilationCheckBox)

        self.discNumberLabel = QLabel(ExportImportWindow)
        self.discNumberLabel.setObjectName(u"discNumberLabel")

        self.formLayout_2.setWidget(6, QFormLayout.LabelRole, self.discNumberLabel)

        self.discNumberCheckBox = QCheckBox(ExportImportWindow)
        self.discNumberCheckBox.setObjectName(u"discNumberCheckBox")

        self.formLayout_2.setWidget(6, QFormLayout.FieldRole, self.discNumberCheckBox)

        self.discCountLabel = QLabel(ExportImportWindow)
        self.discCountLabel.setObjectName(u"discCountLabel")

        self.formLayout_2.setWidget(7, QFormLayout.LabelRole, self.discCountLabel)

        self.discCountCheckBox = QCheckBox(ExportImportWindow)
        self.discCountCheckBox.setObjectName(u"discCountCheckBox")

        self.formLayout_2.setWidget(7, QFormLayout.FieldRole, self.discCountCheckBox)

        self.trackNumberLabel = QLabel(ExportImportWindow)
        self.trackNumberLabel.setObjectName(u"trackNumberLabel")

        self.formLayout_2.setWidget(8, QFormLayout.LabelRole, self.trackNumberLabel)

        self.trackNumberCheckBox = QCheckBox(ExportImportWindow)
        self.trackNumberCheckBox.setObjectName(u"trackNumberCheckBox")

        self.formLayout_2.setWidget(8, QFormLayout.FieldRole, self.trackNumberCheckBox)


        self.horizontalLayout_2.addLayout(self.formLayout_2)

        self.formLayout_3 = QFormLayout()
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.trackCountLabel = QLabel(ExportImportWindow)
        self.trackCountLabel.setObjectName(u"trackCountLabel")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.trackCountLabel)

        self.trackCountCheckBox = QCheckBox(ExportImportWindow)
        self.trackCountCheckBox.setObjectName(u"trackCountCheckBox")

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.trackCountCheckBox)

        self.yearLabel = QLabel(ExportImportWindow)
        self.yearLabel.setObjectName(u"yearLabel")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.yearLabel)

        self.yearCheckBox = QCheckBox(ExportImportWindow)
        self.yearCheckBox.setObjectName(u"yearCheckBox")

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.yearCheckBox)

        self.playsLabel = QLabel(ExportImportWindow)
        self.playsLabel.setObjectName(u"playsLabel")

        self.formLayout_3.setWidget(2, QFormLayout.LabelRole, self.playsLabel)

        self.playsCheckBox = QCheckBox(ExportImportWindow)
        self.playsCheckBox.setObjectName(u"playsCheckBox")

        self.formLayout_3.setWidget(2, QFormLayout.FieldRole, self.playsCheckBox)

        self.playedLabel = QLabel(ExportImportWindow)
        self.playedLabel.setObjectName(u"playedLabel")

        self.formLayout_3.setWidget(3, QFormLayout.LabelRole, self.playedLabel)

        self.playedCheckBox = QCheckBox(ExportImportWindow)
        self.playedCheckBox.setObjectName(u"playedCheckBox")

        self.formLayout_3.setWidget(3, QFormLayout.FieldRole, self.playedCheckBox)

        self.skipsLabel = QLabel(ExportImportWindow)
        self.skipsLabel.setObjectName(u"skipsLabel")

        self.formLayout_3.setWidget(4, QFormLayout.LabelRole, self.skipsLabel)

        self.skipsCheckBox = QCheckBox(ExportImportWindow)
        self.skipsCheckBox.setObjectName(u"skipsCheckBox")

        self.formLayout_3.setWidget(4, QFormLayout.FieldRole, self.skipsCheckBox)

        self.skippedLabel = QLabel(ExportImportWindow)
        self.skippedLabel.setObjectName(u"skippedLabel")

        self.formLayout_3.setWidget(5, QFormLayout.LabelRole, self.skippedLabel)

        self.skippedCheckBox = QCheckBox(ExportImportWindow)
        self.skippedCheckBox.setObjectName(u"skippedCheckBox")

        self.formLayout_3.setWidget(5, QFormLayout.FieldRole, self.skippedCheckBox)

        self.checkedLabel = QLabel(ExportImportWindow)
        self.checkedLabel.setObjectName(u"checkedLabel")

        self.formLayout_3.setWidget(6, QFormLayout.LabelRole, self.checkedLabel)

        self.checkedCheckBox = QCheckBox(ExportImportWindow)
        self.checkedCheckBox.setObjectName(u"checkedCheckBox")
        self.checkedCheckBox.setEnabled(False)

        self.formLayout_3.setWidget(6, QFormLayout.FieldRole, self.checkedCheckBox)

        self.commentLabel = QLabel(ExportImportWindow)
        self.commentLabel.setObjectName(u"commentLabel")

        self.formLayout_3.setWidget(7, QFormLayout.LabelRole, self.commentLabel)

        self.commentCheckBox = QCheckBox(ExportImportWindow)
        self.commentCheckBox.setObjectName(u"commentCheckBox")

        self.formLayout_3.setWidget(7, QFormLayout.FieldRole, self.commentCheckBox)

        self.descriptionLabel = QLabel(ExportImportWindow)
        self.descriptionLabel.setObjectName(u"descriptionLabel")

        self.formLayout_3.setWidget(8, QFormLayout.LabelRole, self.descriptionLabel)

        self.descriptionCheckBox = QCheckBox(ExportImportWindow)
        self.descriptionCheckBox.setObjectName(u"descriptionCheckBox")
        self.descriptionCheckBox.setEnabled(False)

        self.formLayout_3.setWidget(8, QFormLayout.FieldRole, self.descriptionCheckBox)


        self.horizontalLayout_2.addLayout(self.formLayout_3)

        self.formLayout_4 = QFormLayout()
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.longDescriptionLabel = QLabel(ExportImportWindow)
        self.longDescriptionLabel.setObjectName(u"longDescriptionLabel")

        self.formLayout_4.setWidget(0, QFormLayout.LabelRole, self.longDescriptionLabel)

        self.longDescriptionCheckBox = QCheckBox(ExportImportWindow)
        self.longDescriptionCheckBox.setObjectName(u"longDescriptionCheckBox")
        self.longDescriptionCheckBox.setEnabled(False)

        self.formLayout_4.setWidget(0, QFormLayout.FieldRole, self.longDescriptionCheckBox)

        self.lyricsLabel = QLabel(ExportImportWindow)
        self.lyricsLabel.setObjectName(u"lyricsLabel")

        self.formLayout_4.setWidget(1, QFormLayout.LabelRole, self.lyricsLabel)

        self.lyricsCheckBox = QCheckBox(ExportImportWindow)
        self.lyricsCheckBox.setObjectName(u"lyricsCheckBox")
        self.lyricsCheckBox.setEnabled(False)

        self.formLayout_4.setWidget(1, QFormLayout.FieldRole, self.lyricsCheckBox)

        self.bitRateLabel = QLabel(ExportImportWindow)
        self.bitRateLabel.setObjectName(u"bitRateLabel")

        self.formLayout_4.setWidget(2, QFormLayout.LabelRole, self.bitRateLabel)

        self.bitRateCheckBox = QCheckBox(ExportImportWindow)
        self.bitRateCheckBox.setObjectName(u"bitRateCheckBox")

        self.formLayout_4.setWidget(2, QFormLayout.FieldRole, self.bitRateCheckBox)

        self.kindAsStringLabel = QLabel(ExportImportWindow)
        self.kindAsStringLabel.setObjectName(u"kindAsStringLabel")

        self.formLayout_4.setWidget(3, QFormLayout.LabelRole, self.kindAsStringLabel)

        self.kindAsStringCheckBox = QCheckBox(ExportImportWindow)
        self.kindAsStringCheckBox.setObjectName(u"kindAsStringCheckBox")

        self.formLayout_4.setWidget(3, QFormLayout.FieldRole, self.kindAsStringCheckBox)

        self.bpmLabel = QLabel(ExportImportWindow)
        self.bpmLabel.setObjectName(u"bpmLabel")

        self.formLayout_4.setWidget(4, QFormLayout.LabelRole, self.bpmLabel)

        self.bpmCheckBox = QCheckBox(ExportImportWindow)
        self.bpmCheckBox.setObjectName(u"bpmCheckBox")

        self.formLayout_4.setWidget(4, QFormLayout.FieldRole, self.bpmCheckBox)

        self.eqLabel = QLabel(ExportImportWindow)
        self.eqLabel.setObjectName(u"eqLabel")

        self.formLayout_4.setWidget(5, QFormLayout.LabelRole, self.eqLabel)

        self.eqCheckBox = QCheckBox(ExportImportWindow)
        self.eqCheckBox.setObjectName(u"eqCheckBox")

        self.formLayout_4.setWidget(5, QFormLayout.FieldRole, self.eqCheckBox)

        self.vaLabel = QLabel(ExportImportWindow)
        self.vaLabel.setObjectName(u"vaLabel")

        self.formLayout_4.setWidget(6, QFormLayout.LabelRole, self.vaLabel)

        self.vaCheckBox = QCheckBox(ExportImportWindow)
        self.vaCheckBox.setObjectName(u"vaCheckBox")

        self.formLayout_4.setWidget(6, QFormLayout.FieldRole, self.vaCheckBox)

        self.startLabel = QLabel(ExportImportWindow)
        self.startLabel.setObjectName(u"startLabel")

        self.formLayout_4.setWidget(7, QFormLayout.LabelRole, self.startLabel)

        self.startCheckBox = QCheckBox(ExportImportWindow)
        self.startCheckBox.setObjectName(u"startCheckBox")

        self.formLayout_4.setWidget(7, QFormLayout.FieldRole, self.startCheckBox)

        self.finishLabel = QLabel(ExportImportWindow)
        self.finishLabel.setObjectName(u"finishLabel")

        self.formLayout_4.setWidget(8, QFormLayout.LabelRole, self.finishLabel)

        self.finishCheckBox = QCheckBox(ExportImportWindow)
        self.finishCheckBox.setObjectName(u"finishCheckBox")

        self.formLayout_4.setWidget(8, QFormLayout.FieldRole, self.finishCheckBox)


        self.horizontalLayout_2.addLayout(self.formLayout_4)

        self.formLayout_5 = QFormLayout()
        self.formLayout_5.setObjectName(u"formLayout_5")
        self.excludeFromShuffleLabel = QLabel(ExportImportWindow)
        self.excludeFromShuffleLabel.setObjectName(u"excludeFromShuffleLabel")

        self.formLayout_5.setWidget(0, QFormLayout.LabelRole, self.excludeFromShuffleLabel)

        self.excludeFromShuffleCheckBox = QCheckBox(ExportImportWindow)
        self.excludeFromShuffleCheckBox.setObjectName(u"excludeFromShuffleCheckBox")
        self.excludeFromShuffleCheckBox.setEnabled(False)

        self.formLayout_5.setWidget(0, QFormLayout.FieldRole, self.excludeFromShuffleCheckBox)

        self.rememberBookmarkLabel = QLabel(ExportImportWindow)
        self.rememberBookmarkLabel.setObjectName(u"rememberBookmarkLabel")

        self.formLayout_5.setWidget(1, QFormLayout.LabelRole, self.rememberBookmarkLabel)

        self.rememberBookmarkCheckBox = QCheckBox(ExportImportWindow)
        self.rememberBookmarkCheckBox.setObjectName(u"rememberBookmarkCheckBox")
        self.rememberBookmarkCheckBox.setEnabled(False)

        self.formLayout_5.setWidget(1, QFormLayout.FieldRole, self.rememberBookmarkCheckBox)

        self.bookmarkTimeLabel = QLabel(ExportImportWindow)
        self.bookmarkTimeLabel.setObjectName(u"bookmarkTimeLabel")

        self.formLayout_5.setWidget(2, QFormLayout.LabelRole, self.bookmarkTimeLabel)

        self.bookmarkTimeCheckBox = QCheckBox(ExportImportWindow)
        self.bookmarkTimeCheckBox.setObjectName(u"bookmarkTimeCheckBox")
        self.bookmarkTimeCheckBox.setEnabled(False)

        self.formLayout_5.setWidget(2, QFormLayout.FieldRole, self.bookmarkTimeCheckBox)

        self.albumRatingLabel = QLabel(ExportImportWindow)
        self.albumRatingLabel.setObjectName(u"albumRatingLabel")

        self.formLayout_5.setWidget(3, QFormLayout.LabelRole, self.albumRatingLabel)

        self.albumRatingCheckBox = QCheckBox(ExportImportWindow)
        self.albumRatingCheckBox.setObjectName(u"albumRatingCheckBox")
        self.albumRatingCheckBox.setEnabled(False)

        self.formLayout_5.setWidget(3, QFormLayout.FieldRole, self.albumRatingCheckBox)

        self.ratingLabel = QLabel(ExportImportWindow)
        self.ratingLabel.setObjectName(u"ratingLabel")

        self.formLayout_5.setWidget(4, QFormLayout.LabelRole, self.ratingLabel)

        self.ratingCheckBox = QCheckBox(ExportImportWindow)
        self.ratingCheckBox.setObjectName(u"ratingCheckBox")
        self.ratingCheckBox.setEnabled(False)

        self.formLayout_5.setWidget(4, QFormLayout.FieldRole, self.ratingCheckBox)

        self.showLabel = QLabel(ExportImportWindow)
        self.showLabel.setObjectName(u"showLabel")

        self.formLayout_5.setWidget(5, QFormLayout.LabelRole, self.showLabel)

        self.showCheckBox = QCheckBox(ExportImportWindow)
        self.showCheckBox.setObjectName(u"showCheckBox")
        self.showCheckBox.setEnabled(False)

        self.formLayout_5.setWidget(5, QFormLayout.FieldRole, self.showCheckBox)

        self.sortShowLabel = QLabel(ExportImportWindow)
        self.sortShowLabel.setObjectName(u"sortShowLabel")

        self.formLayout_5.setWidget(6, QFormLayout.LabelRole, self.sortShowLabel)

        self.sortShowCheckBox = QCheckBox(ExportImportWindow)
        self.sortShowCheckBox.setObjectName(u"sortShowCheckBox")
        self.sortShowCheckBox.setEnabled(False)

        self.formLayout_5.setWidget(6, QFormLayout.FieldRole, self.sortShowCheckBox)

        self.seasonLabel = QLabel(ExportImportWindow)
        self.seasonLabel.setObjectName(u"seasonLabel")

        self.formLayout_5.setWidget(7, QFormLayout.LabelRole, self.seasonLabel)

        self.seasonCheckBox = QCheckBox(ExportImportWindow)
        self.seasonCheckBox.setObjectName(u"seasonCheckBox")
        self.seasonCheckBox.setEnabled(False)

        self.formLayout_5.setWidget(7, QFormLayout.FieldRole, self.seasonCheckBox)

        self.episodeLabel = QLabel(ExportImportWindow)
        self.episodeLabel.setObjectName(u"episodeLabel")

        self.formLayout_5.setWidget(8, QFormLayout.LabelRole, self.episodeLabel)

        self.episodeCheckBox = QCheckBox(ExportImportWindow)
        self.episodeCheckBox.setObjectName(u"episodeCheckBox")
        self.episodeCheckBox.setEnabled(False)

        self.formLayout_5.setWidget(8, QFormLayout.FieldRole, self.episodeCheckBox)

        self.artworkLabel = QLabel(ExportImportWindow)
        self.artworkLabel.setObjectName(u"artworkLabel")

        self.formLayout_5.setWidget(9, QFormLayout.LabelRole, self.artworkLabel)

        self.artworkCheckBox = QCheckBox(ExportImportWindow)
        self.artworkCheckBox.setObjectName(u"artworkCheckBox")
        self.artworkCheckBox.setEnabled(False)

        self.formLayout_5.setWidget(9, QFormLayout.FieldRole, self.artworkCheckBox)


        self.horizontalLayout_2.addLayout(self.formLayout_5)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.saveButton = QPushButton(ExportImportWindow)
        self.saveButton.setObjectName(u"saveButton")
        self.saveButton.setEnabled(False)

        self.horizontalLayout_3.addWidget(self.saveButton)

        self.cancelButton = QPushButton(ExportImportWindow)
        self.cancelButton.setObjectName(u"cancelButton")

        self.horizontalLayout_3.addWidget(self.cancelButton)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.retranslateUi(ExportImportWindow)

        QMetaObject.connectSlotsByName(ExportImportWindow)
    # setupUi

    def retranslateUi(self, ExportImportWindow):
        ExportImportWindow.setWindowTitle(QCoreApplication.translate("ExportImportWindow", u"XML to ExportImport", None))
        self.label_2.setText(QCoreApplication.translate("ExportImportWindow", u"When a selected field is not present for a song in the XML, it is not included in the resulting ExportImport file.", None))
        self.label_3.setText(QCoreApplication.translate("ExportImportWindow", u"Disabled fields are shown for reference - they are not available in the XML and can never be exported.", None))
        self.label.setText(QCoreApplication.translate("ExportImportWindow", u"XML filepath", None))
        self.xml_browse_button.setText(QCoreApplication.translate("ExportImportWindow", u"Browse", None))
        self.xml_load_button.setText(QCoreApplication.translate("ExportImportWindow", u"Load", None))
        self.songsLoadedLabel.setText(QCoreApplication.translate("ExportImportWindow", u"No XML file loaded", None))
        self.locationLabel.setText(QCoreApplication.translate("ExportImportWindow", u"Location", None))
        self.dateAddedLabel.setText(QCoreApplication.translate("ExportImportWindow", u"DateAdded", None))
        self.nameLabel.setText(QCoreApplication.translate("ExportImportWindow", u"Name", None))
        self.sortNameLabel.setText(QCoreApplication.translate("ExportImportWindow", u"SortName", None))
        self.albumLabel.setText(QCoreApplication.translate("ExportImportWindow", u"Album", None))
        self.sortAlbumLabel.setText(QCoreApplication.translate("ExportImportWindow", u"SortAlbum", None))
        self.albumArtistLabel.setText(QCoreApplication.translate("ExportImportWindow", u"AlbumArtist", None))
        self.sortAlbumArtistLabel.setText(QCoreApplication.translate("ExportImportWindow", u"SortAlbumArtist", None))
        self.artistLabel.setText(QCoreApplication.translate("ExportImportWindow", u"Artist", None))
        self.sortArtistLabel.setText(QCoreApplication.translate("ExportImportWindow", u"SortArtist", None))
        self.composerLabel.setText(QCoreApplication.translate("ExportImportWindow", u"Composer", None))
        self.sortComposerLabel.setText(QCoreApplication.translate("ExportImportWindow", u"SortComposer", None))
        self.groupingLabel.setText(QCoreApplication.translate("ExportImportWindow", u"Grouping", None))
        self.genreLabel.setText(QCoreApplication.translate("ExportImportWindow", u"Genre", None))
        self.compilationLabel.setText(QCoreApplication.translate("ExportImportWindow", u"Compilation", None))
        self.discNumberLabel.setText(QCoreApplication.translate("ExportImportWindow", u"DiscNumber", None))
        self.discCountLabel.setText(QCoreApplication.translate("ExportImportWindow", u"DiscCount", None))
        self.trackNumberLabel.setText(QCoreApplication.translate("ExportImportWindow", u"TrackNumber", None))
        self.trackCountLabel.setText(QCoreApplication.translate("ExportImportWindow", u"TrackCount", None))
        self.yearLabel.setText(QCoreApplication.translate("ExportImportWindow", u"Year", None))
        self.playsLabel.setText(QCoreApplication.translate("ExportImportWindow", u"Plays", None))
        self.playedLabel.setText(QCoreApplication.translate("ExportImportWindow", u"Played", None))
        self.skipsLabel.setText(QCoreApplication.translate("ExportImportWindow", u"Skips", None))
        self.skippedLabel.setText(QCoreApplication.translate("ExportImportWindow", u"Skipped", None))
        self.checkedLabel.setText(QCoreApplication.translate("ExportImportWindow", u"Checked", None))
        self.commentLabel.setText(QCoreApplication.translate("ExportImportWindow", u"Comment", None))
        self.descriptionLabel.setText(QCoreApplication.translate("ExportImportWindow", u"Description", None))
        self.longDescriptionLabel.setText(QCoreApplication.translate("ExportImportWindow", u"LongDescription", None))
        self.lyricsLabel.setText(QCoreApplication.translate("ExportImportWindow", u"Lyrics", None))
        self.bitRateLabel.setText(QCoreApplication.translate("ExportImportWindow", u"BitRate", None))
        self.kindAsStringLabel.setText(QCoreApplication.translate("ExportImportWindow", u"KindAsString", None))
        self.bpmLabel.setText(QCoreApplication.translate("ExportImportWindow", u"BPM", None))
        self.eqLabel.setText(QCoreApplication.translate("ExportImportWindow", u"EQ", None))
        self.vaLabel.setText(QCoreApplication.translate("ExportImportWindow", u"VA", None))
        self.startLabel.setText(QCoreApplication.translate("ExportImportWindow", u"Start", None))
        self.finishLabel.setText(QCoreApplication.translate("ExportImportWindow", u"Finish", None))
        self.excludeFromShuffleLabel.setText(QCoreApplication.translate("ExportImportWindow", u"ExcludeFromShuffle", None))
        self.rememberBookmarkLabel.setText(QCoreApplication.translate("ExportImportWindow", u"RememberBookmark", None))
        self.bookmarkTimeLabel.setText(QCoreApplication.translate("ExportImportWindow", u"BookmarkTime", None))
        self.albumRatingLabel.setText(QCoreApplication.translate("ExportImportWindow", u"AlbumRating", None))
        self.ratingLabel.setText(QCoreApplication.translate("ExportImportWindow", u"Rating", None))
        self.showLabel.setText(QCoreApplication.translate("ExportImportWindow", u"Show", None))
        self.sortShowLabel.setText(QCoreApplication.translate("ExportImportWindow", u"SortShow", None))
        self.seasonLabel.setText(QCoreApplication.translate("ExportImportWindow", u"Season", None))
        self.episodeLabel.setText(QCoreApplication.translate("ExportImportWindow", u"Episode", None))
        self.artworkLabel.setText(QCoreApplication.translate("ExportImportWindow", u"Artwork", None))
        self.saveButton.setText(QCoreApplication.translate("ExportImportWindow", u"Save", None))
        self.cancelButton.setText(QCoreApplication.translate("ExportImportWindow", u"Cancel", None))
    # retranslateUi

