# -*- coding: utf-8 -*-

from logging import Logger
from typing import Union, Callable, Optional
import os
from pprint import pprint

import requests
from youtube_dl import YoutubeDL
from youtube_dl.utils import DownloadError, YoutubeDLError

import settings.settings as s
from exceptions import *
from downloaders.base import Downloader
from tools import *

__all__ = ('Youtube',)


class Youtube(Downloader):
    """
    Загрузчик видеороликов с видеохостинга Youtube при помощи модуля youtube_dl.
    Подробнее о youtube_dl: https://github.com/ytdl-org/youtube-dl

    Attributes:
        url: URL адрес видеоролика.
        _logger: Объект канала логирования. Представлен классом Logger модуля logging.
        _video_info: Словарь с информацией о видеролике, возвращаемый
                    ``YoutubeDL.extract_info()``
        _formats: Словарь форматов вида ``{название_формата: словарь_формата}``
        _ydl_logger: Класс логирования для youtube_dl.
        _cached_sorted_formats: Кэшированное значение функции get_sorted_formats_names.

    Args:
        url: URL адрес видеоролика
    """

    url: str
    _logger: Logger
    _video_info: dict
    _formats: dict[str, dict]
    _cached_sorted_formats: Optional[list[str]]

    def __init__(self,
                 url: str):
        super(Youtube, self).__init__(url)

        self._cached_sorted_formats = None

        try:
            with YoutubeDL({}) as dl:
                self._video_info = dl.extract_info(self.url,
                                                   download=False)
                # Ошибка, если ссылка не на этот загрузчик
                if self._video_info['extractor'] != self.__class__.__name__.lower():
                    raise IncorrectLinkError()

        except DownloadError as err:
            err_message = str(err).split(': ')[1]

            if err_message.startswith('Unable to download API page'):
                raise InternetConnectionError()
            else:
                raise IncorrectLinkError()

        self._extract_formats()

        logger = self._logger

        # Класс логирования для youtube_dl, передается в словаре опций
        class YdlLogger:
            def debug(self, msg='?'):
                logger.debug(f'DL({url}): ydl debug: {msg}')

            def warning(self, msg='?'):
                logger.debug(f'DL({url}): ydl warn: {msg}')

            def error(self, msg='?'):
                logger.error(f'DL({url}): ydl err: {msg}')

        self._ydl_logger = YdlLogger

    def download(self,
                 on_progress: Callable,
                 path: Optional[str] = None,
                 file_name: str = s.OUTPUT_FILE_TEMPLATE,
                 download_format: Union[int, str] = 'bestaudio+bestvideo/best') -> None:

        self._logger.info(f'DL({self.url}): starting video downloading (format: {download_format})')

        format_name = {v: k for k, v in self.get_formats_dict().items()}[download_format]

        if path is not None:
            path = '/'.join(path.split('/') + [file_name])

        self._logger.debug(f'DL({self.url}): downloading format-path: {path}')

        format_dict = self._formats[format_name]
        format_dict.update(self._video_info)
        format_dict['extractor'] = self.__class__.__name__

        path = path.format(**format_dict)

        file_suffix = ''
        file_index = 0

        while os.path.isfile(f'{path}{file_suffix}.mp4'):  # если файл существует - добавить индекс к названию файла
            file_index += 1
            file_suffix = f'({file_index})'  # например: youtube-название_видео(индекс)

        path += file_suffix

        self._logger.info(f'Downloading file: {path}')

        def hook(d: dict):
            if d['status'] not in ('downloading', 'finished'):
                on_progress(0, 0, 'error')
                return

            if not (total_bytes := self.get_total_bytes(format_name)):
                if not (total_bytes := d.get('total_bytes')):
                    total_bytes = d.get('total_bytes_estimate')

            downloaded_bytes = d.get('downloaded_bytes', 0)

            if d['status'] == 'finished':
                hook.last_bytes = downloaded_bytes
                return
            elif hook.last_bytes > downloaded_bytes:
                hook.plus_bytes = hook.last_bytes
                hook.last_bytes = 0

            # print(f'st: {d["status"]}, downloaded: {human_size(d["downloaded_bytes"])}, total: '
            #       f'{human_size(d["total_bytes"])}, hookplus: {human_size(hook.plus_bytes)}')

            on_progress(total_bytes, downloaded_bytes + hook.plus_bytes, d['status'])

        hook.last_bytes = 0
        hook.plus_bytes = 0

        opts = {
            'format': str(download_format),
            'outtmpl': path,
            'progress_hooks': [hook],
            'logger': self._ydl_logger,
            'recode_video': 'mp4',
        }

        if download_format != self._formats.get(s.AUDIO_FORMAT_PROPERTIES_STRING,
                                                {'format_id': None})['format_id']:
            opts['merge_output_format'] = 'mp4'

        try:
            with YoutubeDL(opts) as dl:
                dl.download([self.url])
        except YoutubeDLError as err:
            raise OtherError(err)

        self._logger.info(f'DL({self.url}): video downloaded')

    def get_formats_dict(self) -> Optional[dict[str, str]]:
        audio_format = self._formats.get(s.AUDIO_FORMAT_PROPERTIES_STRING, None)

        if audio_format:
            formats_to_return = {}
            for fn, f in self._formats.items():
                if fn != s.AUDIO_FORMAT_PROPERTIES_STRING:
                    if is_only_video_format(f):
                        formats_to_return[fn] = f"{f['format_id']}+{audio_format['format_id']}"
                    else:
                        formats_to_return[fn] = f['format_id']

            formats_to_return[s.AUDIO_FORMAT_PROPERTIES_STRING] = audio_format['format_id']

        else:
            formats_to_return = {fs: f['format_id']
                                 for fs, f in self._formats.items()
                                 if not is_only_video_format(f)}

        return formats_to_return

    def get_sorted_formats_names(self) -> list[str]:
        if self._cached_sorted_formats is None:
            def sort_function(x) -> tuple:
                height = self._formats[x].get('height', 0)
                fps = self._formats[x].get('fps', 0)
                if not isinstance(height, int):
                    height = 0
                if not isinstance(fps, int):
                    fps = 0
                return height, fps

            self._cached_sorted_formats = sorted(
                self._formats.keys(),
                key=sort_function,
                reverse=True
            )

        return self._cached_sorted_formats

    def download_thumbnail(self,
                           path: str = s.THUMBNAILS_DIRECTORY_PATH,
                           is_high_quality: bool = False) -> str:
        self._logger.info(f'DL({self.url}): starting download thumbnail')

        if not is_high_quality:
            thumbnails = self._video_info['thumbnails']
            min_len = abs(s.MEDIUM_QUALITY_THUMBNAIL_INDEX) \
                if s.MEDIUM_QUALITY_THUMBNAIL_INDEX < 0 \
                else s.MEDIUM_QUALITY_THUMBNAIL_INDEX + 1

            if len(thumbnails) < min_len:
                thumbnail_url = thumbnails[-1]['url']
            else:
                thumbnail_url = thumbnails[s.MEDIUM_QUALITY_THUMBNAIL_INDEX]['url']

        else:
            thumbnail_url = self._video_info['thumbnail']

        thumbnail_ext = get_thumbnail_extension(thumbnail_url)
        thumbnail_filename = f"{self._video_info['extractor']}-{self._video_info['id']}.{thumbnail_ext}"
        thumbnail_path = f'{path}/{thumbnail_filename}'

        if not os.path.isfile(thumbnail_path):

            try:
                with open(thumbnail_path, 'wb') as handle:
                    response = requests.get(thumbnail_url, stream=True)
                    if not response.ok:
                        self._logger.error(f'DL({self.url}): resp not ok: {response}')
                    for block in response.iter_content(1024):
                        if not block:
                            break
                        handle.write(block)

            except (requests.ConnectionError, requests.HTTPError) as err:
                raise OtherError(err.__class__.__name__)

            self._logger.debug(f'DL({self.url}): thumbnail downloaded')

        return thumbnail_filename

    def get_total_bytes(self, format_name: str) -> Optional[int]:
        try:
            return self._formats[format_name]['filesize']
        except KeyError:
            return None

    def _extract_formats(self) -> None:
        """
        Получает и записывает в атрибут ``_formats`` словарь форматов
        вида ``{название_формата: словарь_формата}``.
        """
        formats = self._video_info.get('formats', [self._video_info])
        self._formats = {}

        filtered_video_formats = filter_video_formats(
            get_audio_video_formats(formats)
        ) + filter_video_formats(
            get_only_video_formats(formats)
        )

        audio_formats = get_only_audio_formats(formats)

        best_audio_format = {'filesize': 0}
        if audio_formats:
            best_audio_format = max(audio_formats,
                                    key=lambda x: x['abr'])
            self._formats[s.AUDIO_FORMAT_PROPERTIES_STRING] = best_audio_format

        pprint(filtered_video_formats)
        for f in filtered_video_formats:
            if is_only_video_format(f) and audio_formats:
                f['filesize'] += best_audio_format['filesize']
            self._formats[s.FORMAT_PROPTIES_FPS_TEMPLATE.format(**f)] = f

    @property
    def title(self) -> Optional[str]:
        return self._video_info.get('title', 'Заголовок отсутствует')

    @property
    def author(self) -> Optional[str]:
        return self._video_info.get('uploader', 'Отсутствует')
