# -*- coding: utf-8 -*-
import logging

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, QModelIndex

import settings.settings as s
from tools import notify_with_checkbox
from downloaders.base import Downloader
from db.manager import DbManager
from dialogs import EditVideoDialog, VideoDownloadDialog
from ui.main_window_ui import Ui_MainWindow

__all__ = ('MainAppWindow',)


class MainAppWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    Форма основного окна приложения
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self._logger = logging.getLogger(self.__class__.__name__)
        self.db = DbManager()
        self.save_dir = None

        # Настройка окна
        self.setWindowTitle(s.MAIN_WINDOW_TITLE)
        self.setWindowIcon(QtGui.QIcon(s.APP_ICON_PATH))
        self.setFixedSize(self.width(), self.height())

        # Создание модели для таблицы videos_table
        self.table_model = QtGui.QStandardItemModel(0, 3, parent=self)

        for row_index, video in enumerate(self.db.get_all_table_videos()):
            row_items = [
                QtGui.QStandardItem(video['resource']),
                QtGui.QStandardItem(video['title']),
                QtGui.QStandardItem(video['format_name']),
            ]
            self.table_model.appendRow(row_items)
            index = self.table_model.index(row_index, 0)
            self.table_model.setData(index, video['id'], role=Qt.UserRole)

        # Настройка таблицы videos_table
        self.videos_table.setModel(self.table_model)
        self.table_model.setHorizontalHeaderLabels(['Источник', 'Заголовок', 'Формат'])

        self.videos_table.setColumnWidth(0, 110)
        self.videos_table.setColumnWidth(1, 500)
        self.videos_table.setColumnWidth(2, self.videos_table.width() - 610)

        self.videos_table.verticalHeader().hide()
        self.videos_table.horizontalHeader().setFixedHeight(34)
        self.videos_table.horizontalHeader().setHighlightSections(False)

        self.videos_table.horizontalScrollBar().hide()
        self.videos_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.videos_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.videos_table.setFocusPolicy(Qt.NoFocus)

        self.videos_table.doubleClicked.connect(self.videos_table_double_clicked)
        self.videos_table.selectionModel().selectionChanged.connect(self.table_row_selected)
        self.videos_table.model().rowsInserted.connect(self.table_row_inserted)

        self.start_button.clicked.connect(self.start_button_clicked)
        self.add_video_button.clicked.connect(self.add_video_button_clicked)
        self.delete_video_button.clicked.connect(self.delete_video_button_clicked)
        self.edit_video_button.clicked.connect(self.edit_video_button_clicked)
        self.select_dir_button.clicked.connect(self.select_dir_button_clicked)

    def table_row_selected(self, *_):
        if self.videos_table.selectionModel().selectedRows():
            self.delete_video_button.setEnabled(True)
            self.edit_video_button.setEnabled(True)
        else:
            self.delete_video_button.setEnabled(False)
            self.edit_video_button.setEnabled(False)

    def table_row_inserted(self, *_):
        self.videos_table.selectionModel().clearSelection()
        self.delete_video_button.setEnabled(False)
        self.edit_video_button.setEnabled(False)

    def videos_table_double_clicked(self, index: QModelIndex):
        self.edit_table_video(index.row())

    def edit_video_button_clicked(self):
        self.edit_table_video(self.videos_table.selectedIndexes()[0].row())

    def delete_video_button_clicked(self):
        row = self.videos_table.selectedIndexes()[0].row()
        id = self.table_model.data(self.table_model.index(row, 0),
                                   Qt.UserRole)
        print('delete: id', id)
        self.db.delete_table_video_by_id(id)
        self.table_model.removeRow(row)

    def edit_table_video(self, row_index: int):
        print('edit video:', row_index)

        video_id = self.table_model.data(self.table_model.index(row_index, 0),
                                         Qt.UserRole)
        video_info = self.db.get_table_video_by_id(video_id)

        dialog = EditVideoDialog(title='Редактировать параметры',
                                 url=video_info['url'],
                                 resource_name=video_info['resource'],
                                 selected_format_name=video_info['format_name'],
                                 parent=self)
        if dialog.exec():
            info = dialog.get_inputs()
        else:
            self._logger.debug('Edit dialog rejected')
            return

        dl: Downloader = info['dl']

        if not self.db.has_table_video(url=dl.url, format_name=info['format_name']):

            self.db.update_table_video(url=dl.url,
                                       resource_name=info['resource_name'],
                                       title=dl.title,
                                       format_name=info['format_name'],
                                       format_string=dl.get_formats_dict()[info['format_name']],
                                       thumbnail_filename=info['tn_filename'],
                                       id=video_id)
            self.table_model.item(row_index, 0).setText(info['resource_name'])
            self.table_model.item(row_index, 1).setText(dl.title)
            self.table_model.item(row_index, 2).setText(info['format_name'])

    def add_video_button_clicked(self):
        self._logger.debug('add_video_button is clicked')

        dialog = EditVideoDialog('Добавить видеоролик')

        if dialog.exec():
            info = dialog.get_inputs()
        else:
            self._logger.debug('dialog is rejected')
            return

        dl: Downloader = info['dl']

        if not self.db.has_table_video(url=dl.url, format_name=info['format_name']):

            video_id = self.db.add_table_video(url=dl.url,
                                               resource_name=info['resource_name'],
                                               title=dl.title,
                                               format_name=info['format_name'],
                                               format_string=dl.get_formats_dict()[info['format_name']],
                                               thumbnail_filename=info['tn_filename'])

            self.table_model.appendRow([
                QtGui.QStandardItem(info['resource_name']),
                QtGui.QStandardItem(dl.title),
                QtGui.QStandardItem(info['format_name'])
            ])

            # В "скрытых" данных первой ячейки каждой строки таблицы будет храниться
            # id видеоролика в базе данных.
            added_index = self.table_model.index(self.table_model.rowCount() - 1, 0)
            self.table_model.setData(added_index, video_id, Qt.UserRole)

        else:
            self.report_error('Такой видеоролик уже добавлен.')

    def select_dir_button_clicked(self):
        self.save_dir = str(QtWidgets.QFileDialog.getExistingDirectory(self, 'Выберите папку'))
        self.save_dir_label.setText(self.save_dir)

    def start_button_clicked(self):
        self._logger.debug('start_button is clicked')

        if not self.save_dir:  # проверка на наличие папки для сохранения
            self.report_error('Не выбрана папка для сохранения. Выберите папку и попробуйте снова.')
            return

        videos_dicts = self.db.get_all_table_videos()

        if not videos_dicts:  # проверка на наличие видеороликов для скачивания
            self.report_error('Нет видеороликов для скачивания. Добавьте хотя-бы один видеоролик '
                              'и попробуйте снова.')
            return

        if int(self.db.get_setting('show_is_video_download')):
            accepted, cb_checked = notify_with_checkbox(self, 'Начать скачивание',
                                                        'Вы действительно хотите начать загрузку?')
            if cb_checked:  # Проверка - чтобы не нагружать базу данных
                self.db.set_setting('show_is_video_download', '0')
            if not accepted:
                return

        dialog = VideoDownloadDialog(videos_dicts, self.save_dir)

        dialog.exec()
        # remaining_videos = dialog.get_remaining_videos()
        self.table_model.removeRows(0, self.table_model.rowCount())
        self.db.delete_all_table_videos()

    def report_error(self, msg: str):
        """
        Сообщает об ошибке пользователю с помощью ``QMessageBox.critical()``

        Args:
            msg: Текст ошибки.
        """
        QtWidgets.QMessageBox.critical(self, 'Ошибка', msg,
                                       defaultButton=QtWidgets.QMessageBox.Ok)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.db.close()
        event.accept()
