"""
Модуль описывает репозиторий, взаимодействующий с БД.
Каждая таблица в БД олицетворяет определенную модель.
"""

from typing import Tuple
import sqlite3
from bookkeeper.repository.abstract_repository import AbstractRepository, T


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

    def __init__(self, db_file: str, cls: type) -> None:
        """
        db_file - имя файла с базой данных
        cls - модель
        """
        self.db_file = db_file
        self.cls = cls
        self.table_name = cls.__name__.lower()

        self.create_dbtable()

    def create_dbtable(self):
        annotations = list(self.cls.__annotations__.items())
        table_fields = []
        for annotation in annotations:
            annotation_type = 'INT' * int(annotation[1] is int) + \
                              'REAL' * int(annotation[1] is float) + \
                              'TEXT' * int(annotation[1] is not int and
                                           annotation[1] is not float)
            table_fields.append(f'{str(annotation[0])} {annotation_type}')
        set_table = ', '.join(table_fields)
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(f'CREATE TABLE IF NOT EXISTS '
                        f'{self.table_name}({set_table})')
        con.close()

    def add(self, obj) -> None:
        names = ', '.join(self.cls.__annotations__.keys())
        placeholders = ', '.join("?" * len(self.cls.__annotations__.keys()))
        values = [getattr(obj, x)
                  for x in list(self.cls.__annotations__.keys())]
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
        if tuple_obj is not None:
            obj = self.cls(pk=tuple_obj[0], args=tuple_obj[1:])
        else:
            obj = None
        return obj

    def get_all(self, args: Tuple[str] | None = None) -> list[T]:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            if args is None:
                cur.execute(
                    f'SELECT * FROM {self.table_name}'
                )
            else:
                where = ' AND '.join(args)
                cur.execute(
                    f'SELECT * FROM {self.table_name} WHERE {where}'
                )
            tuple_objs = cur.fetchall()
        con.close()
        objs = []
        for tuple_obj in tuple_objs:
            objs.append(self.cls(pk=tuple_obj[0], args=tuple_obj[1:]))
        return objs

    def update(self,
               args: Tuple[str],
               pk: int = 0) -> None:
        names = list(self.cls.__annotations__.keys())
        names.remove('pk')
        print(names)
        sets = ', '.join(f'{name} = \'{args[names.index(name)]}\''
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
