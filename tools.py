from PyQt5.QtWidgets import QWidget, QMessageBox, QCheckBox
from typing import Optional

import settings.settings as s

__all__ = (
    'human_size',
    'filter_video_formats',
    'get_only_video_formats',
    'get_only_audio_formats',
    'get_audio_video_formats',
    'is_only_video_format',
    'get_thumbnail_extension',
    'get_thumbnail_path',
    'notify_with_checkbox',
    'show_notification'
)


def human_size(bytes_size: Optional[int]) -> Optional[str]:
    """
    Преобразует количество байтов в читаемый для пользователя вид (108МБ, 912КБ и т.д.)

    Args:
        bytes_size: Количество байтов для преобразования

    Returns:
        Строка, содержащая читаемое для человека значение объема информации.
    """
    if bytes_size is None:  # Необходимо для корректной работы кода при аргумете равном None
        return None

    suffix = 'Б'
    for unit in ['', 'К', 'М', 'Г', 'Т', 'П', 'Е', 'З']:
        if abs(bytes_size) < 1024.0:
            return f"{bytes_size:.1f}{unit}{suffix}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f}И{suffix}"


def get_thumbnail_path(filename: str) -> str:
    """
    Возвращает путь к файлу превью по имени файла.

    Args:
        filename: Имя файла превью.

    Returns:
        Путь к файлу превью.
    """
    return f'{s.THUMBNAILS_DIRECTORY_PATH}/{filename}'


# Вспомогательные функции для загрузчиков на основе youtube_dl

def is_only_video_format(format_: dict) -> bool:
    """
    Проверяет, является ли формат "только видео" форматом.

    Args:
        format_: Словарь проверяемого формата.

    Returns:
        True, если формат является "только видео" форматом, иначе False.
    """
    return format_['acodec'] == 'none'


def filter_video_formats(formats: list[dict]) -> list[dict]:
    """
    Фильтрует список форматов, возвращаемый
    ``youtube_dl.YoutubeDL.extract_info()``

    Args:
        formats: Список словарей форматов

    Returns:
        Отфильтрованный список видео-форматов
    """
    video_formats = filter(
        lambda x: x['vcodec'] != 'none',
        formats
    )

    # удалить все видео с неразрешенными расширениями
    video_formats = filter(
        lambda x: x['ext'] in s.ALLOWED_VIDEO_EXTENSIONS,
        video_formats
    )

    # formats => formats_dict{'format_string': {'ext': {format}}}
    formats_dict = {}
    for f in video_formats:
        f_string = s.FORMAT_PROPTIES_FPS_TEMPLATE.format(**f)
        ext = f['ext']
        if f_string in formats_dict:
            formats_dict[f_string][ext] = f
        else:
            formats_dict[f_string] = {ext: f}

    # formats_dict => filtered_formats[{format}]
    filtered_formats = []
    for _, d in formats_dict.items():
        filtered_formats.append(max(
            d.items(),
            key=lambda x: s.ALLOWED_VIDEO_EXTENSIONS.index(x[0])
        )[1])

    return filtered_formats


def get_only_audio_formats(formats: list[dict]) -> list[dict]:
    """
    Фильтрует список форматов и возвращает список "только аудио" форматов

    Args:
        formats: Список словарей форматов

    Returns:
        Список "только аудио" форматов
    """
    audio_formats = list(filter(
        lambda f: f['vcodec'] == 'none',
        formats
    ))
    return audio_formats


def get_only_video_formats(formats: list[dict]) -> list[dict]:
    """
    Фильтрует список форматов и возвращает список "только видео" форматов

    Args:
        formats: Список словарей форматов

    Returns:
        Список "только видео" форматов
    """
    video_formats = list(filter(
        is_only_video_format,
        formats
    ))
    return video_formats


def get_audio_video_formats(formats: list[dict]) -> list[dict]:
    """
    Фильтрует список форматов и возвращает список "аудио и видео" форматов

    Args:
        formats: Список словарей форматов

    Returns:
        Список "аудио и видео" форматов
    """
    audio_video_formats = list(filter(
        lambda f: f['vcodec'] != 'none' and f['acodec'] != 'none',
        formats
    ))
    return audio_video_formats


def get_thumbnail_extension(url: str) -> str:
    """
    Возвращает расширение файла изображения превью по URL адресу превью.

    Args:
        url: URL адрес превью

    Returns:
        Расширение файла изображения превью
    """
    return url.split('?')[0].split('.')[-1]


def notify_with_checkbox(window: QWidget,
                         title: str,
                         text: str) -> tuple[bool, bool]:
    """
    Показывает окно-предупреждение с возможностью отмены действия и
    флажком "Больше не спрашивать".

    Args:
        window: Объект родительского окна.
        title: Заголовок окна-предупреждения
        text: Текст окна-предупреждения

    Returns:
        notify_with_checkbox: Кортеж с двумя элементами типа bool - нажал ли пользователь кнопку
                              "Продолжить" и установлен ли флажок "Больше не спрашивать".
    """
    message_box = QMessageBox(window)
    message_box.setWindowTitle(title)
    message_box.setText(text)
    message_box.setIcon(QMessageBox.Warning)
    message_box.addButton('Отмена', QMessageBox.RejectRole)
    message_box.addButton('Продолжить', QMessageBox.AcceptRole)

    checkbox = QCheckBox('Больше не спрашивать')
    message_box.setCheckBox(checkbox)

    accepted = message_box.exec()
    checkbox_checked = message_box.checkBox().isChecked()

    return accepted, checkbox_checked


def show_notification(window: QWidget,
                      title: str,
                      text: str) -> None:
    """
    Показывает окно-уведомление с кнопкой "ОК"

    Args:
        window: Объект родительского окна.
        title: Заголовок окна.
        text: Текст уведомления.
    """
    QMessageBox.information(window, title, text,
                            defaultButton=QMessageBox.Ok)
