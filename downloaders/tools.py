from settings.downloaders import DOWNLOADERS
from downloaders.base import Downloader

from typing import Type

__all__ = ('get_downloaders_names',
           'get_downloader')


def get_downloaders_names() -> list[str]:
    """
    Возвращает список имен интернет-платформ для загрузки видеороликов.

    Returns:
        Список имен интернет-платформ.
    """
    return sorted(DOWNLOADERS.keys())


def get_downloader(name: str) -> Type[Downloader]:
    """
    Возвращает загрузчик, имя которого передается в качестве
    аргумента ``name``.

    Args:
        name: Имя необходимого загрузчика.

    Returns:
        Класс необходимого загрузчика.
    """
    return DOWNLOADERS[name]
