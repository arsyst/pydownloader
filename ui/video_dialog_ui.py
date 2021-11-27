# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sources/video_dialog_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_VideoDialog(object):
    def setupUi(self, VideoDialog):
        VideoDialog.setObjectName("VideoDialog")
        VideoDialog.setEnabled(True)
        VideoDialog.resize(646, 494)
        VideoDialog.setStyleSheet("* {background: rgb(248, 248, 249);}\n"
"\n"
"QLabel {\n"
"    color: #121212;\n"
"    font-size: 16px;\n"
"}\n"
"\n"
"QComboBox,\n"
"QPushButton,\n"
"QTableView,\n"
"QLineEdit {\n"
"    border-color: #d9dadb;\n"
"    border-style: solid;\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: #121212;\n"
"}\n"
"\n"
"QPushButton,\n"
"QTableView,\n"
"QLineEdit,\n"
"QComboBox:editable {\n"
"    background: #fff;\n"
"}\n"
"\n"
"QComboBox,\n"
"QLineEdit {\n"
"    padding-left: 8px;\n"
"}\n"
"\n"
"QComboBox:!editable {\n"
"    background: #e8e8e9;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 18px;\n"
"    border-top-right-radius: 5px;\n"
"    border-bottom-right-radius: 5px;\n"
"    padding-right: 6px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(images/down_arrow.svg);\n"
"}\n"
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
        self.cancel_button = QtWidgets.QPushButton(VideoDialog)
        self.cancel_button.setGeometry(QtCore.QRect(370, 443, 111, 30))
        self.cancel_button.setObjectName("cancel_button")
        self.save_button = QtWidgets.QPushButton(VideoDialog)
        self.save_button.setEnabled(False)
        self.save_button.setGeometry(QtCore.QRect(500, 443, 111, 30))
        self.save_button.setObjectName("save_button")
        self.url_edit = QtWidgets.QLineEdit(VideoDialog)
        self.url_edit.setGeometry(QtCore.QRect(30, 119, 581, 33))
        self.url_edit.setObjectName("url_edit")
        self.url_label = QtWidgets.QLabel(VideoDialog)
        self.url_label.setGeometry(QtCore.QRect(30, 94, 181, 19))
        self.url_label.setObjectName("url_label")
        self.formats_label = QtWidgets.QLabel(VideoDialog)
        self.formats_label.setGeometry(QtCore.QRect(30, 229, 171, 19))
        self.formats_label.setObjectName("formats_label")
        self.formats_box = QtWidgets.QComboBox(VideoDialog)
        self.formats_box.setGeometry(QtCore.QRect(30, 255, 581, 33))
        self.formats_box.setEditable(False)
        self.formats_box.setObjectName("formats_box")
        self.check_button = QtWidgets.QPushButton(VideoDialog)
        self.check_button.setGeometry(QtCore.QRect(30, 164, 111, 30))
        self.check_button.setObjectName("check_button")
        self.check_status_label = QtWidgets.QLabel(VideoDialog)
        self.check_status_label.setGeometry(QtCore.QRect(152, 169, 451, 20))
        self.check_status_label.setStyleSheet("color:rgb(12, 12, 12)")
        self.check_status_label.setObjectName("check_status_label")
        self.thumbnail_label = QtWidgets.QLabel(VideoDialog)
        self.thumbnail_label.setGeometry(QtCore.QRect(30, 309, 231, 121))
        self.thumbnail_label.setText("")
        self.thumbnail_label.setScaledContents(False)
        self.thumbnail_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.thumbnail_label.setObjectName("thumbnail_label")
        self.video_title_label = QtWidgets.QLabel(VideoDialog)
        self.video_title_label.setGeometry(QtCore.QRect(280, 309, 331, 121))
        self.video_title_label.setStyleSheet("font-size: 18px;\n"
"font-family: Roboto, Arial, sans-serif;")
        self.video_title_label.setText("")
        self.video_title_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.video_title_label.setWordWrap(True)
        self.video_title_label.setObjectName("video_title_label")
        self.resource_box = QtWidgets.QComboBox(VideoDialog)
        self.resource_box.setGeometry(QtCore.QRect(30, 46, 581, 33))
        self.resource_box.setStyleSheet("")
        self.resource_box.setEditable(True)
        self.resource_box.setObjectName("resource_box")
        self.resource_box_label = QtWidgets.QLabel(VideoDialog)
        self.resource_box_label.setGeometry(QtCore.QRect(30, 20, 191, 19))
        self.resource_box_label.setObjectName("resource_box_label")

        self.retranslateUi(VideoDialog)
        QtCore.QMetaObject.connectSlotsByName(VideoDialog)

    def retranslateUi(self, VideoDialog):
        _translate = QtCore.QCoreApplication.translate
        VideoDialog.setWindowTitle(_translate("VideoDialog", "Dialog"))
        self.cancel_button.setText(_translate("VideoDialog", "Отменить"))
        self.save_button.setText(_translate("VideoDialog", "Сохранить"))
        self.url_label.setText(_translate("VideoDialog", "Ссылка на видеоролик:"))
        self.formats_label.setText(_translate("VideoDialog", "Качество видеоролика:"))
        self.check_button.setText(_translate("VideoDialog", "Проверить"))
        self.check_status_label.setText(_translate("VideoDialog", "Нажмите \"проверить\", чтобы продолжить"))
        self.resource_box_label.setText(_translate("VideoDialog", "Источник:"))