# -*- coding: utf-8 -*-

import sqlite3
from logging import getLogger, Logger
from typing import Optional

import settings.settings as s

__all__ = ('DbManager',)


def dict_factory(cursor, row) -> dict:
    """Генератор строк-словарей для sqlite3"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class DbManager:
    """
    Класс для управления SQLite базой данных приложения.

    Список параметров настроек:

    * 'show_is_video_download' - Если '1' - показывать сообщение
      "Вы действительно хотите загрузить...", иначе - не показывать (По умолчанию - '1').

    Attributes:
        connection: Объект подключения к базе данных приложения.
                    Представлен классом Connection модуля sqlite3.
        cursor: Объект курсора для соединения DbManager.connection
        _logger: Объект канала логирования. Представлен классом Logger модуля logging.

    Args:
        db_path: Путь до файла базы данных приложения.
    """

    connection: sqlite3.Connection
    _logger: Logger

    def __init__(self,
                 db_path: str = s.DB_PATH):
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()
        self._logger = getLogger(self.__class__.__name__)

    def add_table_video(self,
                        url: str,
                        resource_name: str,
                        title: Optional[str] = None,
                        format_name: Optional[str] = None,
                        format_string: Optional[str] = None,
                        thumbnail_filename: Optional[str] = None) -> int:
        """
        Записывает в базу данных видеоролик, добавленный в таблицу видеороликов
        для скачивания.

        Args:
            url: URL адрес на страницу видеоролика.
            resource_name: Название источника видеоролика.
            title: Заголовок видеоролика
            format_name: Название формата скачивания.
            format_string: Строка формата скачивания.
            thumbnail_filename: Имя файла изображения превью видеоролика.

        Returns:
            ID видеоролика в базе данных
        """
        query = """
        INSERT INTO table_video (url, resource, title, thumbnail_filename,
                                 format_name, format_string)
        VALUES (:url, :resource, :title, :thumbnail_filename,
                :format_name, :format_string)"""

        self.cursor.execute(query, {
            'url': url,
            'resource': resource_name,
            'title': title,
            'thumbnail_filename': thumbnail_filename,
            'format_name': format_name,
            'format_string': format_string,
        })
        self.connection.commit()

        self._logger.debug('Table video added')

        return self.cursor.lastrowid

    def get_all_table_videos(self) -> list[dict]:
        """
        Возвращает данные видеороликов, занесенных в таблицу видеороликов
        для загрузки. Возвращаемые словари имеют следующие ключи:
        ``id``, ``url``, ``resource``, ``title``, ``thumbnail_filename``,
        ``format_name``, ``format_string``

        Returns:
            Список словарей с данными видеоролика.
        """
        query = """SELECT * FROM table_video"""
        result = self.cursor.execute(query).fetchall()

        return result

    def get_table_video_by_id(self, id: int) -> dict:
        """
        Возвращает данные видеоролика, занесенного в таблицу видеороликов
        по его id. Возвращаемый словарь имеет следующие ключи:
        ``id``, ``url``, ``resource``, ``title``, ``thumbnail_filename``,
        ``format_name``, ``format_string``

        Args:
            id: id видеоролика в базе данных.

        Returns:
            Словарь данных видеоролика.
        """
        query = """
        SELECT * FROM table_video
        WHERE id = ?"""
        result = self.cursor.execute(query, (id,)).fetchone()

        return result

    def has_table_video(self,
                        url: str,
                        format_name: str) -> bool:
        """
        Проверяет, есть ли видеоролик в таблице видеороликов для скачивания
        по URL адресу и формату видеоролика.

        Args:
            url: URL адрес проверяемого видеоролика.
            format_name: Название формата проверяемого видеоролика.

        Returns:
            Если видеоролик присутствует в таблице - True, иначе - False.
        """
        query = """
        SELECT * FROM table_video
        WHERE url = ? AND format_name = ?"""

        result = self.cursor.execute(query, (url, format_name)).fetchall()
        return bool(result)

    def delete_table_video_by_id(self, id: int) -> None:
        """
        Удаляет видеоролик, занесенного в таблицу видеороликов
        по его id. Возвращаемый словарь имеет следующие ключи:
        ``id``, ``url``, ``resource``, ``title``, ``thumbnail_filename``,
        ``format_name``, ``format_string``

        Args:
            id: id видеоролика в базе данных.

        Returns:
            Словарь данных видеоролика.
        """
        query = """
        DELETE FROM table_video
        WHERE id = ?"""
        self.cursor.execute(query, (id,))
        self.connection.commit()

    def delete_all_table_videos(self) -> None:
        """
        Удаляет все видеоролики, занесенные в таблицу видеороликов для скачивания.
        """
        query = """
        DELETE FROM table_video"""
        self.cursor.execute(query)
        self.connection.commit()

    def update_table_video(self,
                           id: int,
                           url: str,
                           resource_name: str,
                           title: Optional[str] = None,
                           format_name: Optional[str] = None,
                           format_string: Optional[str] = None,
                           thumbnail_filename: Optional[str] = None) -> None:
        """
        Обновить данные о видеоролике, занесенном в таблицу
        для скачивания по его id.

        Args:
            id: id обновляемого видеоролика.
            url: URL адрес на страницу видеоролика.
            resource_name: Название источника видеоролика.
            title: Заголовок видеоролика
            format_name: Название формата скачивания.
            format_string: Строка формата скачивания.
            thumbnail_filename: Имя файла изображения превью видеоролика.
        """
        query = """
        UPDATE table_video
        SET url = :url, resource = :resource, title = :title,
            thumbnail_filename = :thumbnail_filename,
            format_name = :format_name, format_string = :format_string
        WHERE id = :id
        """
        self.cursor.execute(query, {
            'id': id,
            'url': url,
            'resource': resource_name,
            'title': title,
            'thumbnail_filename': thumbnail_filename,
            'format_name': format_name,
            'format_string': format_string,
        })
        self.connection.commit()

    def set_setting(self, setting_key: str, value: str) -> None:
        """
        Устанавливает параметр настроек по названию (ключу) параметра.
        Список параметров смотрите в документации к классу ``DbManager``.

        Args:
            setting_key: Название (ключ) параметра.
            value: Значение параметра.
        """
        query = """
        UPDATE settings SET value = ?
        WHERE key = ?
        """
        self.cursor.execute(query, (value, setting_key))
        self.connection.commit()

    def get_setting(self, setting_key: str) -> str:
        """
        Возвращает значение параметра настроек по названию (ключу).
        Список параметров смотрите в докуметации к классу ``DbMansger``.

        Args:
            setting_key: Название (ключ) параметра настроек.

        Returns:
            Значение параметра настроек.
        """
        query = """
        SELECT settings.value FROM settings
        WHERE settings.key = ?
        """
        result = self.cursor.execute(query, (setting_key,)).fetchone()
        return result['value']

    def close(self) -> None:
        """
        Закрывает соединение с базой данных.
        """
        self.connection.close()
