# -*- coding: utf-8 -*-

from logging import getLogger
from typing import Optional

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, QTimer

import settings.settings as s
from ui.video_dialog_ui import Ui_VideoDialog
from ui.video_download_dialog_ui import Ui_VideoDownloadDialog
from downloaders.tools import *
from downloaders.base import Downloader
from tools import get_thumbnail_path, human_size, show_notification
from threads import *
from exceptions import *

__all__ = ('EditVideoDialog', 'VideoDownloadDialog')


def errors_reporting(func):
    """
    Декоратор, обрабатывающий исключения в методах класса ``EditVideoDialog``.
    """
    def wrapper(*args, **kwargs):
        self = args[0]
        try:
            returned = func(*args, **kwargs)
        except InternetConnectionError:
            self.report_error('Не удалось подключиться к ресурсу. '
                              'Проверьте подключение к интернету и попробуйте снова.')
        except IncorrectLinkError:
            self.report_error('Не удалось получить доступ к видеоролику. '
                              'Проверьте правильность ссылки и попробуйте снова.')
        except OtherError as err:
            self._logger.error(f'Unknown error catched: {err.__class__}: {str(err)}')
            self.report_error('Произошла неизвестная ошибка. '
                              'Попробуйте снова через несколько минут.\n'
                              f'Код ошибки: {err.err.__class__.__name__}')
        else:
            return returned
    return wrapper


class EditVideoDialog(QtWidgets.QDialog, Ui_VideoDialog):
    """
    Форма диалогового окна для ввода параметров скачиваемого видеоролика

    Args:
        title: Заголовок диалогового окна.
        url: Введенный ранее URL адрес видеоролика (указывается при редактировании).
        resource_name: Выбранный ранее источник видеоролика (указывается при редактировании).
        selected_format_name: Выбранный ранее формат видеоролика (указывается при редактировании).
    """

    def __init__(self,
                 title: str = 'Параметры скачивания',
                 url: Optional[str] = None,
                 resource_name: Optional[str] = None,
                 selected_format_name: Optional[str] = None,
                 parent=None):
        super(EditVideoDialog, self).__init__(parent=parent)
        self.setupUi(self)

        self._logger = getLogger(str(self.__class__))

        # Настройки окна
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle(title)
        self.setWindowIcon(QtGui.QIcon(s.APP_ICON_PATH))

        # Настройки QComboBox
        self.formats_box.setEditable(False)
        self.formats_box.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        self.formats_box.currentTextChanged.connect(self.format_changed)

        self.resource_box.addItems(get_downloaders_names())
        self.resource_box.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        self.resource_box.setEditText('Выберите источник')
        self.resource_box.currentTextChanged.connect(self.resource_changed)

        # Настройки QPushButton
        self.check_button.setEnabled(False)
        self.check_button.clicked.connect(self.check_button_clicked)

        self.save_button.setEnabled(False)

        self.cancel_button.clicked.connect(self.reject)
        self.save_button.clicked.connect(self.accept)

        # Если в режиме редактирования:
        if url:
            self.selected_format_name = selected_format_name

            self.resource_box.setCurrentText(resource_name)
            self.url_edit.setText(url)
            self.check_button.click()
        else:
            self.selected_format_name = None

        self._logger.debug('EditVideoDialog: inited')

    def resource_changed(self, text: str = '', *_):
        if text in get_downloaders_names():
            self.check_button.setEnabled(True)
        else:
            self.check_button.setEnabled(False)

    def format_changed(self, text: str = '', *_):
        try:
            names = self.dl.get_sorted_formats_names()
        except (AttributeError, NameError):  # если self.dl еще не определен
            names = []
        if text in names:
            self.save_button.setEnabled(True)
        else:
            self.save_button.setEnabled(False)

    @errors_reporting
    def check_button_clicked(self, *_):
        self._logger.debug('EditVideoDialog: check_button is clicked')

        self.check_status_label.setText('Проверка...')
        self.check_status_label.setStyleSheet('color: rgb(12, 12, 12);')

        self.thumbnail_label.clear()
        self.video_title_label.setText('')

        self.save_button.setEnabled(False)

        self.formats_box.setEditable(True)
        self.formats_box.clear()
        self.formats_box.setEditText('')
        self.formats_box.setEditable(False)

        video_url = self.url_edit.text()
        dl_class = get_downloader(self.resource_box.currentText())

        self.timeout_timer = QTimer(self)
        self.timeout_timer.timeout.connect(self.timeout_reached)
        self.timeout_timer.start(s.THREAD_WORKING_TIMEOUT)

        self.video_info_download_thread = VideoInfoDownloadThread(dl_class, video_url)
        self.video_info_download_thread.error_raised.connect(self.thread_error_raised)
        self.video_info_download_thread.info_downloaded.connect(self.video_info_downloaded)
        self.video_info_download_thread.start()

    def video_info_downloaded(self, dl: Downloader):
        self.dl = dl

        self.timeout_timer.stop()
        self.timeout_timer.start(s.THREAD_WORKING_TIMEOUT + 7000)

        self.tn_download_thread = ThumbnailDownloadThread(self.dl)
        self.tn_download_thread.error_raised.connect(self.thread_error_raised)
        self.tn_download_thread.thumbnail_downloaded.connect(self.thumbnail_downloaded)
        self.tn_download_thread.start()

    def thread_error_raised(self, err: str):
        self._logger.error(f'error: {err}')

        self.timeout_timer.stop()

        self.check_status_label.setText('Произошла ошибка. Попробуйте еще раз.')
        self.check_status_label.setStyleSheet('color: rgb(255, 65, 68);')

        if err == 'InternetConnectionError':
            self.report_error('Не удалось подключиться к ресурсу. '
                              'Проверьте подключение к интернету и попробуйте снова.')

        elif err == 'IncorrectLinkError':
            self.report_error('Не удалось получить доступ к видеоролику. '
                              'Проверьте правильность ссылки и попробуйте снова.')

        else:
            self.report_error('Произошла неизвестная ошибка. '
                              'Попробуйте снова через несколько минут.\n'
                              f'Код ошибки: {err}')

    @errors_reporting
    def thumbnail_downloaded(self, tn_filename: str):
        print('tn_pixmap path:', tn_filename)

        self.timeout_timer.stop()

        self.video_formats = self.dl.get_sorted_formats_names()

        if self.video_formats is None:
            self.formats_box.setEditable(True)
            self.formats_box.setEditText('Выбор формата недоступен')
            self.formats_box.setEditable(False)
            self.save_button.setEnabled(True)
        else:
            self.formats_box.clear()
            self.formats_box.setEditable(True)
            self.formats_box.addItems(self.video_formats)
            if self.selected_format_name:  # Если режим редактирования
                self.formats_box.setCurrentText(self.selected_format_name)
                self.save_button.setEnabled(True)
            else:  # Если режим добавления
                self.formats_box.setEditText('Выберите формат')
                self.save_button.setEnabled(False)

        self.thumbnail_filename = tn_filename

        if tn_filename is not None:
            tn_pixmap = QtGui.QPixmap(get_thumbnail_path(tn_filename))
            tn_pixmap = tn_pixmap.scaled(self.thumbnail_label.width(),
                                         self.thumbnail_label.height(),
                                         Qt.KeepAspectRatio)
            self.thumbnail_label.clear()
            self.thumbnail_label.setAlignment(Qt.AlignRight)
            self.thumbnail_label.setPixmap(tn_pixmap)

        else:
            self.thumbnail_label.clear()
            self.thumbnail_label.setAlignment(Qt.AlignHCenter)
            self.thumbnail_label.setText('Превью недоступно')

        title_str = f'<h4 style="font-weight: 500; margin-bottom: 0.3em;">{self.dl.title}</h4>' \
                    f'<span style="font-size: 16px; color: #666">Автор: {self.dl.author}</span>'
        self.video_title_label.setText(title_str)

        self.check_status_label.setText('Проверка прошла успешно')
        self.check_status_label.setStyleSheet('color: rgb(41, 165, 22);')

    def report_error(self, msg: str, status_label_error: bool = True):
        QtWidgets.QMessageBox.critical(self, 'Ошибка', msg,
                                       defaultButton=QtWidgets.QMessageBox.Ok)
        if status_label_error:
            self.check_status_label.setText('Произошла ошибка. Попробуйте еще раз.')
            self.check_status_label.setStyleSheet('color: rgb(255, 65, 68);')

    def timeout_reached(self, *_):
        self.report_error('Превышено время ожидания. '
                          'Попробуйте еще раз через несколько минут.')

        # Завершение процессов, время выполнения которых превышено.
        try:
            if self.video_info_download_thread.isRunning():
                self.video_info_download_thread.terminate()
        except (AttributeError, NameError):
            pass
        try:
            if self.tn_download_thread.isRunning():
                self.tn_download_thread.terminate()
        except (AttributeError, NameError):
            pass

    def get_inputs(self) -> dict:
        """
        Возвращает словарь данных, введенные пользователем в диалоговое окно
        и дополнительную информацию о видеоролике.

        Возвращаемый словарь имеет вид:

        ``{'dl': объект_загрузчика,
        'format_name': название_формата,
        'tn_filename': имя_файла_превью,
        'resource_name': название_источника}``

        Returns:
            Данные, введенные пользователем и дополнительную информацию о видеоролике
        """
        return {'dl': self.dl,
                'format_name': self.formats_box.currentText(),
                'tn_filename': self.thumbnail_filename,
                'resource_name': self.resource_box.currentText()}


class VideoDownloadDialog(QtWidgets.QDialog, Ui_VideoDownloadDialog):
    """
    Форма диалогового окна загрузки видеороликов.

    Args:
        videos: Список словарей с информацией о видеороликах, возвращаемый
                ``db.manager.DbManager.get_all_table_videos()``.
        save_path: Путь до папки сохраниния видеороликов.
    """

    def __init__(self,
                 videos: list[dict],
                 save_path: str,
                 parent=None):
        super(VideoDownloadDialog, self).__init__(parent=parent)
        self.setupUi(self)

        self._logger = getLogger(str(self.__class__))

        # Настройка окна
        self.setWindowTitle('Скачивание видео')
        self.setFixedSize(self.width(), self.height())
        self.setWindowIcon(QtGui.QIcon(s.APP_ICON_PATH))

        # Настройка GUI
        self.status_label.setText('Подготовка к скачиванию...')
        self.progress_bar.setValue(0)

        self.videos = videos
        self.videos_amount = len(videos)
        self.current_video_index = 0
        self.save_path = save_path
        self.problem_videos = []
        self.status_params = {
            'ind': 0,
            'total_videos': len(videos),
            'downloaded': '0B',
            'total_bytes': '0B',
            'status': 'Подготовка к скачиванию...'
        }

        # Настройка QPushButton
        self.pause_button.hide()  # TODO: доделать приостановку скачивания
        self.stop_button.clicked.connect(self.stop_clicked)

        self.download_video()

    def download_video(self) -> None:
        """
        Начинает загрузку первого видеоролика из списка self.videos.
        """
        self.pause_button.setEnabled(False)

        if not self.videos:
            self.all_downloaded()
            return

        self.current_video_index += 1

        self.progress_bar.setValue(0)
        self.set_dl_status(ind=self.current_video_index,
                           downloaded=human_size(0),
                           total_bytes=human_size(0),
                           status='Подготовка к скачиванию...')

        dl_class = get_downloader(self.videos[0]['resource'])
        video_url = self.videos[0]['url']

        self.info_download_thread = VideoInfoDownloadThread(dl_class, video_url)
        self.info_download_thread.error_raised.connect(self.thread_error_raised)
        self.info_download_thread.info_downloaded.connect(self.video_info_downloaded)
        self.info_download_thread.start()

    def video_info_downloaded(self, dl: Downloader):
        self.current_dl = dl

        self.tn_download_thread = ThumbnailDownloadThread(self.current_dl)
        self.tn_download_thread.error_raised.connect(self.thread_error_raised)
        self.tn_download_thread.thumbnail_downloaded.connect(self.thumbnail_downloaded)
        self.tn_download_thread.start()

    def thumbnail_downloaded(self, tn_filename: str):
        if tn_filename is not None:
            tn_pixmap = QtGui.QPixmap(get_thumbnail_path(tn_filename))
            tn_pixmap = tn_pixmap.scaled(self.thumbnail_label.width(),
                                         self.thumbnail_label.height(),
                                         Qt.KeepAspectRatio)
            self.thumbnail_label.clear()
            self.thumbnail_label.setAlignment(Qt.AlignRight)
            self.thumbnail_label.setPixmap(tn_pixmap)

        else:
            self.thumbnail_label.clear()
            self.thumbnail_label.setAlignment(Qt.AlignHCenter)
            self.thumbnail_label.setText('Превью недоступно')

        title_str = f'<h4 style="font-weight: 500; margin-bottom: 0.3em;">{self.current_dl.title}</h4>' \
                    f'<span style="font-size: 16px; color: #666">Автор: {self.current_dl.author}</span>'
        self.video_title_label.setText(title_str)

        self.set_dl_status(status='Идет скачивание...',
                           total_bytes=human_size(self.current_dl.get_total_bytes(
                               self.videos[0]['format_name']
                           )))

        self.video_download_thread = VideoDownloadThread(self.current_dl, self.save_path,
                                                         self.videos[0]['format_string'])
        self.video_download_thread.download_progress.connect(self.display_download_progress)
        self.video_download_thread.error_raised.connect(self.download_video_thread_error)
        self.video_download_thread.downloaded.connect(self.video_downloaded)
        self.video_download_thread.start()

    def display_download_progress(self, total_bytes: int,
                                  downloaded_bytes: int, status: str):
        if status == 'error':
            self.download_video_thread_error(OtherError(Exception('status "error" while downloading')))

        self.progress_bar.setValue(int(downloaded_bytes / total_bytes * 100))
        self.set_dl_status(downloaded=human_size(downloaded_bytes))

    def video_downloaded(self):
        self.videos.pop(0)
        self.download_video()

    def stop_clicked(self):
        if self.video_download_thread.isRunning():
            self.video_download_thread.terminate()
        show_notification(self, 'Скачивание завершено',
                          'Скачивание завершено. ' + ('Скачивание некоторых видеороликов прервалось ошибкой.'
                                                      if self.problem_videos else ''))
        QtWidgets.QDialog.reject(self)

    def all_downloaded(self):
        self.stop_clicked()

    def thread_error_raised(self, err: str):
        self._logger.error(f'error: {err}')

        self.problem_videos.insert(0, self.videos.pop(0))

        if err == 'InternetConnectionError':
            self.report_error('Не удалось подключиться к ресурсу. '
                              'Проверьте подключение к интернету и попробуйте снова.')

        elif err == 'IncorrectLinkError':
            self.report_error('Не удалось получить доступ к видеоролику. '
                              'Попробуйте снова через несколько минут.')

        else:
            self.report_error('Произошла неизвестная ошибка. '
                              'Попробуйте снова через несколько минут.\n'
                              f'Код ошибки: {err}')

        self.download_video()

    def download_video_thread_error(self, err: Exception):
        self._logger.error(f'Error while video {self.current_video_index} downloading: {err.__repr__()}')
        self.problem_videos.insert(0, self.videos.pop(0))
        self.download_video()

    def set_dl_status(self, **kwargs) -> None:
        """
        Обновляет строку статуса скачивания.

        Args:
            **kwargs: Один или несколько параметров скачивания:
                      ind, total_videos, downloaded, total_bytes, status.
        """
        self.status_params.update(kwargs)
        if self.status_params.get('total_bytes', None) is None:
            self.status_label.setText(s.DOWNLOAD_STATUS_TEMPLATE_WITHOUT_BYTES.format(**self.status_params))
        else:
            self.status_label.setText(s.DOWNLOAD_STATUS_TEMPLATE.format(**self.status_params))

    def report_error(self, msg: str) -> None:
        """
        Сообщает об ошибке пользователю с помощью ``QMessageBox.critical()``

        Args:
            msg: Текст ошибки.
        """
        QtWidgets.QMessageBox.critical(self, 'Ошибка', msg,
                                       defaultButton=QtWidgets.QMessageBox.Ok)

    def get_remaining_videos(self) -> list[int]:
        """Возвращает id нескачанных видеороликов"""
        return list(map(lambda x: x['id'], self.problem_videos))

    def reject(self) -> None:
        self.stop_clicked()
