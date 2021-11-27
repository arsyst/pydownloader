from typing import Type

from PyQt5 import QtCore

from downloaders.base import Downloader

__all__ = ('ThumbnailDownloadThread', 'VideoInfoDownloadThread', 'VideoDownloadThread')


class ThumbnailDownloadThread(QtCore.QThread):
    """
    Класс потока загрузки превью видеороликов.
    Необходим для бесперебойной работы интерфейса окна приложения.

    Args:
        dl: Объект загрузчика, представлен классом ``downloaders.base.Downloader``.
    """

    error_raised = QtCore.pyqtSignal(str)
    thumbnail_downloaded = QtCore.pyqtSignal(str)

    def __init__(self, dl: Downloader, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.dl = dl
        print('tn_dl_thread inited')

    def run(self):
        try:
            tn_path = self.dl.download_thumbnail()
            print('tn downloaded')
        except Exception as err:
            print('Unknown error:', err)
            self.error_raised.emit(err.__class__.__name__)
        else:
            self.thumbnail_downloaded.emit(tn_path)


class VideoInfoDownloadThread(QtCore.QThread):
    """
    Класс потока загрузки информации о видеоролике.
    Необходим для бесперебойной работы интерфейса окна приложения.

    Args:
        dl_class: Класс загрузчика, представлен классом.
        url: URL адрес страницы загружаемого видеоролика.
    """

    error_raised = QtCore.pyqtSignal(str)
    info_downloaded = QtCore.pyqtSignal(Downloader)

    def __init__(self,
                 dl_class: Type[Downloader],
                 url: str,
                 parent=None):
        QtCore.QThread.__init__(self, parent)
        self.dl_class = dl_class
        self.url = url
        print('tn_dl_thread inited')

    def run(self):
        try:
            dl_object = self.dl_class(self.url)
            print('thread: dl inited')
        except Exception as err:
            print('Unknown error:', err)
            self.error_raised.emit(err.__class__.__name__)
        else:
            self.info_downloaded.emit(dl_object)


class VideoDownloadThread(QtCore.QThread):
    """
    Класс потока загрузки видеоролика.
    Необходим для бесперебойной и безопасной работы интерфейса окна приложения.

    Args:
        dl: Объект класса загрузчика, представлен классом, производным от.
        save_path: Путь до папки сохраниния видеороликов.
        format_string: Идентификатор формата.
    """

    error_raised = QtCore.pyqtSignal(str)
    downloaded = QtCore.pyqtSignal()
    download_progress = QtCore.pyqtSignal(int, int, str)

    def __init__(self,
                 dl: Downloader,
                 save_path: str,
                 format_string: str,
                 parent=None):
        QtCore.QThread.__init__(self, parent)
        self.dl = dl
        self.save_path = save_path
        self.format_string = format_string
        print('video download thread inited')

    def run(self):  # t.start()
        try:
            self.dl.download(on_progress=self.download_progress.emit,
                             path=self.save_path,
                             download_format=self.format_string)
        except Exception as err:
            self.error_raised.emit()
        else:
            self.downloaded.emit()
