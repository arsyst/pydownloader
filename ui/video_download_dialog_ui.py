# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sources/video_download_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_VideoDownloadDialog(object):
    def setupUi(self, VideoDownloadDialog):
        VideoDownloadDialog.setObjectName("VideoDownloadDialog")
        VideoDownloadDialog.resize(662, 337)
        VideoDownloadDialog.setStyleSheet("* {background: rgb(248, 248, 249);}\n"
"\n"
"QLabel {\n"
"    color: #121212;\n"
"    font-size: 16px;\n"
"}\n"
"\n"
"QPushButton,\n"
"QProgressBar {\n"
"    border-color: #d9dadb;\n"
"    border-style: solid;\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: #121212;\n"
"    background: #fff;\n"
"}\n"
"\n"
"QProgressBar {text-align: center;}\n"
"\n"
"QPushButton {\n"
"    padding: 3px 7px\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    color: #2d2d2f;\n"
"    background: #d9d9da;\n"
"    border-color: #c3c5c6;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background: #f4f4f5;\n"
"}")
        self.progress_bar = QtWidgets.QProgressBar(VideoDownloadDialog)
        self.progress_bar.setGeometry(QtCore.QRect(30, 235, 601, 25))
        self.progress_bar.setProperty("value", 0)
        self.progress_bar.setObjectName("progress_bar")
        self.pause_button = QtWidgets.QPushButton(VideoDownloadDialog)
        self.pause_button.setGeometry(QtCore.QRect(350, 280, 141, 30))
        self.pause_button.setObjectName("pause_button")
        self.stop_button = QtWidgets.QPushButton(VideoDownloadDialog)
        self.stop_button.setEnabled(True)
        self.stop_button.setGeometry(QtCore.QRect(500, 280, 131, 30))
        self.stop_button.setStyleSheet("color: #fff;\n"
"background: rgb(233, 81, 68);\n"
"border-color: rgb(179, 59, 39);")
        self.stop_button.setCheckable(False)
        self.stop_button.setObjectName("stop_button")
        self.now_downloads_label = QtWidgets.QLabel(VideoDownloadDialog)
        self.now_downloads_label.setGeometry(QtCore.QRect(30, 24, 151, 19))
        self.now_downloads_label.setObjectName("now_downloads_label")
        self.thumbnail_label = QtWidgets.QLabel(VideoDownloadDialog)
        self.thumbnail_label.setGeometry(QtCore.QRect(40, 60, 231, 121))
        self.thumbnail_label.setStyleSheet("\n"
"")
        self.thumbnail_label.setText("")
        self.thumbnail_label.setScaledContents(False)
        self.thumbnail_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.thumbnail_label.setObjectName("thumbnail_label")
        self.video_title_label = QtWidgets.QLabel(VideoDownloadDialog)
        self.video_title_label.setGeometry(QtCore.QRect(290, 60, 331, 121))
        self.video_title_label.setStyleSheet("font-size: 18px;\n"
"font-family: Roboto, Arial, sans-serif;")
        self.video_title_label.setText("")
        self.video_title_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.video_title_label.setWordWrap(True)
        self.video_title_label.setObjectName("video_title_label")
        self.decorative_label = QtWidgets.QLabel(VideoDownloadDialog)
        self.decorative_label.setGeometry(QtCore.QRect(30, 50, 601, 141))
        self.decorative_label.setStyleSheet("border-color: #d9dadb;\n"
"border-style: solid;\n"
"border-width: 1px;\n"
"border-radius: 5px;\n"
"")
        self.decorative_label.setText("")
        self.decorative_label.setObjectName("decorative_label")
        self.status_label = QtWidgets.QLabel(VideoDownloadDialog)
        self.status_label.setGeometry(QtCore.QRect(30, 208, 601, 19))
        self.status_label.setObjectName("status_label")
        self.decorative_label.raise_()
        self.progress_bar.raise_()
        self.pause_button.raise_()
        self.stop_button.raise_()
        self.now_downloads_label.raise_()
        self.thumbnail_label.raise_()
        self.video_title_label.raise_()
        self.status_label.raise_()

        self.retranslateUi(VideoDownloadDialog)
        QtCore.QMetaObject.connectSlotsByName(VideoDownloadDialog)

    def retranslateUi(self, VideoDownloadDialog):
        _translate = QtCore.QCoreApplication.translate
        VideoDownloadDialog.setWindowTitle(_translate("VideoDownloadDialog", "Dialog"))
        self.pause_button.setText(_translate("VideoDownloadDialog", "??????????????????????????"))
        self.stop_button.setText(_translate("VideoDownloadDialog", "??????????????????"))
        self.now_downloads_label.setText(_translate("VideoDownloadDialog", "???????????? ??????????????????????:"))
        self.status_label.setText(_translate("VideoDownloadDialog", "???????????????????? ?? ????????????????????..."))
