from logging import Logger, getLogger
from typing import Optional, Union, Callable

import settings.settings as s

__all__ = ('Downloader',)


class Downloader:
    """
    Базовый класс для загрузчиков.

    Args:
        url: URL адрес видеоролика.

    Attributes:
        url: URL адрес видеоролика.
        _logger: Объект канала логирования. Представлен классом Logger модуля logging.
    """

    url: str
    title: str
    _logger: Logger

    def __init__(self,
                 url: str):
        self.url = url
        self._logger = getLogger(str(self.__class__))
        self._logger.debug('class inited')

    def download(self,
                 on_progress: Union[Callable, list[Callable]],
                 path: Optional[str] = None,
                 file_name: Optional[str] = s.OUTPUT_FILE_TEMPLATE,
                 download_format: Optional[Union[int, str]] = None) -> str:
        """
        Начинает загрузку видеоролика.

        В качестве аргументов фунции передаются общее количество байт - int,
        количество скачанных байт - int и статус скачивания ('downloading',
        'finished' или 'error') - str.

        Args:
            on_progress: Функция, вызываемая при получении фрагмента видеоролика.
            path: Путь к папке загрузки файла.
            file_name: Имя выходного файла.
            download_format: Идентификатор формата загружаемого видеороликаю

        Returns:
            Путь, по которому был загружен видеоролик
        """
        pass

    def get_formats_dict(self) -> Optional[dict[str, str]]:
        """
        Получает возможные форматы скачивания видеоролика.

        Возвращает словарь вида ``{название_формата: идентификатор_формата}``

        Returns:
            Словарь форматов скачивания видеоролика или None, если выбор формата недоступен.
        """
        pass

    def get_sorted_formats_names(self) -> Optional[list[str]]:
        """
        Возвращает отсортированный список названий форматов или
        ``None``, если выбор формата недоступен

        Returns:
            Список названий форматов или None.
        """
        pass

    def download_thumbnail(self,
                           path: str = s.THUMBNAILS_DIRECTORY_PATH,
                           is_high_quality: bool = False) -> Optional[str]:
        """
        Скачивает превью видеоролика в папку, указанную в аргументе ``path``.

        Args:
            path: Папка для скачивания превью видеоролика
            is_high_quality: Если True, то превью будет загружаться в высоком разрешении,
                             иначе - в низком.

        Returns:
            Имя файла скачанного превью.
        """
        pass

    def get_total_bytes(self,
                        format_name: str) -> Optional[int]:
        """
        Возвращает общий объем памяти в байтах, занимаемых файлом видеоролика указанного формата.

        Args:
            format_name: Название формата видеоролика.

        Returns:
            Общий объем памяти, занимаемых видеороликом или
            None, если общее количество объема памяти неизвестно.
        """
        pass

    @property
    def title(self) -> str:
        """
        Заголовок видеоролика, если нет - 'Заголовок отсутствует'
        """
        return 'Заголовок отсутствует'

    @property
    def author(self) -> str:
        """
        Автор видеоролика, если нет - 'Отсутствует'
        """
        return 'Отсутствует'
