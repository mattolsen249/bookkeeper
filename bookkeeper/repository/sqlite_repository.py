"""
Модуль описывает репозиторий, взаимодействующий с БД.
Каждая таблица в БД олицетворяет определенную модель.
"""

from dataclasses import dataclass
# from datetime import datetime
from inspect import get_annotations
from typing import Any
import sqlite3

from bookkeeper.repository.abstract_repository import AbstractRepository, T
from bookkeeper.models.category import Category


@dataclass
class Test:
    """
    Тестовый класс
    """
    name: str
    # created: 'datetime'
    pk: int = 0


class SQLiteRepository(AbstractRepository[T]):
    """
    Репозиторий, взаимодействующий с одной из таблиц БД.

    ...

    АТРИБУТЫ
    ----------
    db_file: str
        название файла с БД

    cls: type
        модель, с объектами котрой работает репозиторий
    """

    db_file: str
    cls: type
    table_name: str
    fields: dict

    def __init__(self, db_file: str, cls: type) -> None:
        """
        db_file - имя файла с базой данных
        cls - модель
        """
        self.db_file = db_file
        self.cls = cls
        self.table_name = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)

        annotations = list(self.cls.__annotations__.items())
        table_fields = []
        for annotation in annotations:
            types = 'INT' * int(annotation[1] is int) + \
                    'REAL' * int(annotation[1] is float) + \
                    'TEXT' * int(annotation[1] is not int and
                                 annotation[1] is not float)
            table_fields.append(f'{str(annotation[0])} {types}')
        set_table = ', '.join(table_fields)
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            try:
                cur.execute(
                    f'CREATE TABLE {self.table_name} ({set_table})')
            except sqlite3.OperationalError:
                pass
        con.close()

    def add(self, obj) -> None:
        names = ', '.join(self.fields.keys())
        placeholders = ', '.join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'INSERT INTO {self.table_name} ({names}) '
                f'VALUES ({placeholders})', values
            )
            obj.pk = cur.lastrowid
            cur.execute(
                f'UPDATE {self.table_name} SET pk = {obj.pk} '
                f'WHERE ROWID = {obj.pk}'
            )
        con.close()

    def get(self, pk: int) -> T | None:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'SELECT * FROM {self.table_name} WHERE pk = {pk}'
            )
            tuple_obj = cur.fetchone()
        con.close()
        obj = self.cls(tuple_obj[1:], pk=tuple_obj[0])
        return obj


    """
        def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'SELECT * FROM {self.table_name}'
            )
            tuple_objs = cur.fetchall()
        con.close()
        objs = []
        for tuple_obj in tuple_objs:
            objs.append(self.cls(tuple_obj[1:], pk=tuple_obj[0]))
        if where is None:
            return objs
        else:
            return [obj for obj in objs
                    if all(getattr(obj, attr) == where[attr] for attr in
                           where.keys())]
    """
    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'SELECT * FROM {self.table_name} WHERE '
            )
            tuple_objs = cur.fetchall()
        con.close()
        objs = []
        for tuple_obj in tuple_objs:
            objs.append(self.cls(tuple_obj[1:], pk=tuple_obj[0]))
        if where is None:
            return objs
        else:
            return [obj for obj in objs
                    if all(getattr(obj, attr) == where[attr] for attr in
                           where.keys())]

    def update(self, pk: int, attrs: tuple) -> None:
        names = list(self.fields.keys())
        sets = ', '.join(f'{name} = \'{attrs[names.index(name)]}\''
                         for name in names)
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'UPDATE {self.table_name} SET {sets} WHERE pk = {pk}'
            )
        con.close()

    def delete(self, pk: int) -> None:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'DELETE FROM {self.table_name} WHERE pk = {pk}'
            )
        con.close()


