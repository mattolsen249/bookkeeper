"""
Модель категории расходов
"""
from dataclasses import  dataclass
from collections import defaultdict
from typing import Iterator, Tuple, List

from ..repository.abstract_repository import AbstractRepository


@dataclass(slots=True)
class Category:
    """
    Категория расходов, хранит название в атрибуте name,
    ссылку (id) на себя в атрибуте pk и ссылку на
    родителя (категория, подкатегорией которой является данная)
    в атрибуте parent. У категорий верхнего уровня parent = None
    """
    pk: int
    name: str
    parent: str

    def __init__(self,
                 args: Tuple[str | None] = ('Все', None),
                 pk: int = 0) -> None:
        self.pk = pk
        if args is not None:
            self.name = args[0]
            self.parent = args[1]

    def get_parent(self,
                   repo: AbstractRepository['Category']) -> 'Category | None':
        """
        Получить родительскую категорию в виде объекта Category
        Если метод вызван у категории верхнего уровня, возвращает None

        Parameters
        ----------
        repo - репозиторий для получения объектов

        Returns
        -------
        Объект класса Category или None
        """
        parent = repo.get_all((f'name=\'{self.parent}\'',))
        if len(parent) == 0:
            return None
        else:
            return parent[0]

    def get_all_parents(self,
                        repo: AbstractRepository['Category']
                        ) -> List['Category']:
        """
        Получить все категории верхнего уровня в иерархии.

        Parameters
        ----------
        repo - репозиторий для получения объектов

        Yields
        -------
        Объекты Category от родителя и выше до категории верхнего уровня
        """
        parent = self.get_parent(repo)
        if parent is None:
            return []
        else:
            return [parent, *parent.get_all_parents(repo)]

    def get_children(self,
                     repo: AbstractRepository['Category']
                     ) -> List['Category']:
        return repo.get_all((f'parent=\'{self.name}\'',))

    def get_all_children(self,
                         repo: AbstractRepository['Category']
                         ) -> List['Category']:
        """
        Получить все подкатегории из иерархии, т.е. непосредственные
        подкатегории данной, все их подкатегории и т.д.

        Parameters
        ----------
        repo - репозиторий для получения объектов

        Yields
        -------
        Объекты Category, являющиеся подкатегориями разного уровня ниже данной.
        """
        all_children = []
        children = self.get_children(repo)
        for child in children:
            all_children.append(child)
            all_children += [*child.get_all_children(repo)]
        return all_children
