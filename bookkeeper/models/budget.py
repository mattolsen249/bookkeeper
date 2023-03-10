"""
Описан класс, представляющий бюджетные ограничения
"""

from dataclasses import dataclass
from datetime import date
from typing import Tuple


@dataclass(slots=True)
class Budget:
    """
    Бюджет.
    limit - ограничение бюджета
    datetime_init - начало периода подсчета бюджета
    datetime_fin - конец периода подсчета бюджета
    category_name - название категории расходов
    """
    pk: int
    name: str
    amount_limit: float
    date1: date
    date2: date
    category_name: str

    def __init__(self,
                 attrs: Tuple[str] = (0, 'budget', date.min, date.max, 'Все'),
                 pk: int = 0) -> None:
        self.pk = pk
        self.amount_limit = float(attrs[0])
        self.name = attrs[1]
        [year, month, day] = attrs[2].split('-')
        self.date1 = date(int(year), int(month), int(day))
        [year, month, day] = attrs[3].split('-')
        self.date2 = date(int(year), int(month), int(day))
        self.category_name = attrs[4]
