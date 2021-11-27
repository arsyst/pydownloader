# -*- coding: utf-8 -*-

from logging import Logger
from pprint import pprint
from typing import Union, Callable, Optional

import requests
from youtube_dl import YoutubeDL

from settings import *
from tools import *

__all__ = ('SimpleDL',)


class SimpleDL:
    """
    Класс для упрощенной работы с youtube_dl.
    Подробнее о youtube_dl: https://github.com/ytdl-org/youtube-dl

    Attributes:
        url: URL адрес видеоролика.
        logger: Объект канала логирования. Представлен классом Logger модуля logging.
        _ydl_logger: Класс логирования для youtube_dl.

    Args:
        url: URL адрес видеоролика
        logger: Объект канала логирования. Представлен классом Logger модуля logging.
    """

    url: str
    logger: Logger

    def __init__(self,
                 url: str,
                 logger: Logger):
        self.url = url
        self.logger = logger

        class YdlLogger:
            def debug(self, msg='NONE'):
                logger.debug(f'DL({url}): ydl debug: {msg}')

            def warning(self, msg='NONE'):
                logger.debug(f'DL({url}): ydl warn: {msg}')

            def error(self, msg='NONE'):
                logger.error(f'DL({url}): ydl err: {msg}')

        self._ydl_logger = YdlLogger

    def download(self,
                 on_progress: Union[Callable, list[Callable]],
                 path: Optional[str] = None,
                 file_name: str = '%(title)s.%(ext)s',
                 download_format: Union[int, str] = 'bestaudio+bestvideo/best') -> None:
        """
        Начинает загрузку видеоролика.

        При получении фрагмета видеоролика вызывается функция или список функций,
        передаваемый в качестве аргумента ``on_progress`` с аргументами,
        описанными здесь: https://github.com/ytdl-org/youtube-dl/blob/master/youtube_dl/YoutubeDL.py#L235

        О возможных форматах, передаваемых в качастве аргумента ``download_format``
        написано здесь: https://github.com/ytdl-org/youtube-dl#format-selection

        Args:
            on_progress: Функция или список функций,
                         вызываемых при получении фрагмента видеоролика.
            path: Путь к папке загрузки файла
            file_name: Имя выходного файла
            download_format: Строка формата загружаемого видеоролика
        """
        self.logger.info(f'DL({self.url}): starting video downloading')

        if path is not None:
            path = '\\'.join(path.split('\\') + [file_name])

        opts = {
            'format': download_format,
            'outtmpl': path,
            'progress_hooks': on_progress if isinstance(on_progress, list) else [on_progress],
            'logger': self._ydl_logger
        }

        with YoutubeDL(opts) as dl:
            dl.download([self.url])

        self.logger.info(f'DL({self.url}): video downloaded')

    def get_formats(self) -> Optional[dict[str, str]]:
        """
        Получает возможные форматы скачивания видеоролика.

        Возвращает словарь вида ``{строка_формата: строка_свойств_формата}``

        Returns:
            Словарь форматов скачивания видеоролика или None, если выбор формата недоступен.
        """
        self.logger.debug(f'DL({self.url}): get_formats starting')

        with YoutubeDL({'logger': self._ydl_logger}) as dl:
            data = dl.extract_info(self.url,
                                   download=False)

        if data['extractor'] in FORMAT_SELECTION_ALLOWED_EXTRACTORS:
            formats = data.get('formats', [data])

            filtered_video_formats = filter_video_formats(
                get_audio_video_formats(formats)
            ) + filter_video_formats(
                get_only_video_formats(formats)
            )

            pprint(filtered_video_formats)

            audio_formats = get_only_audio_formats(formats)

            formats_to_return = {FORMAT_PROPTIES_FPS_TEMPLATE.format(**f):
                                     f"bestaudio+{f['format_id']}" if is_only_video_format(f) else f['format_id']
                                 for f in filtered_video_formats
                                 if not (not audio_formats and is_only_video_format(f))}

            formats_to_return = {val: key for key, val in formats_to_return.items()}
            return formats_to_return

        else:
            return None

    def download_thumbnail(self,
                           path: str = THUMBNAILS_DIR_PATH) -> str:
        """
        Скачивает превью видеоролика в папку, указанную в аргументе ``path``.

        Args:
            path: Папка для скачивания превью видеоролика

        Returns:
            Имя файла скачанного превью
        """
        self.logger.info(f'DL({self.url}): starting download thumbnail')

        with YoutubeDL({'logger': self._ydl_logger}) as dl:
            data = dl.extract_info(self.url,
                                   download=False)
        thumbnail_url = data['thumbnail']
        thumbnail_ext = get_thumbnail_extension(thumbnail_url)
        thumbnail_file_name = f"{data['id']}.{thumbnail_ext}"

        with open(f'{path}/{thumbnail_file_name}', 'wb') as handle:
            response = requests.get(thumbnail_url, stream=True)
            if not response.ok:
                self.logger.error(f'DL({self.url}): resp not ok: {response}')
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)
        self.logger.info(f'DL({self.url}): thumbnail downloaded')

        return thumbnail_file_name
