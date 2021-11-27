# -*- coding: utf-8 -*-

# from pprint import pprint
from typing import Optional

import settings.settings as s
from downloaders.youtube import Youtube

__all__ = ('Twitter',)


class Twitter(Youtube):
    """
    Youtube-like загрузчик видеороликов с социальной сети Twitter при помощи модуля youtube_dl.
    Подробнее о youtube_dl: https://github.com/ytdl-org/youtube-dl
    """

    def get_formats_dict(self) -> Optional[dict[str, str]]:
        formats_dict = {fs: f['format_id']
                        for fs, f in self._formats.items()}

        return formats_dict

    def _extract_formats(self) -> None:
        formats = self._video_info.get('formats', [self._video_info])
        http_formats = filter(
            lambda x: x['protocol'].startswith('http'),
            formats
        )
        self._formats = {s.FORMAT_PROPTIES_TEMPLATE.format(**f): f
                         for f in http_formats}
