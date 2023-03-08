"""
Описан класс, представляющий бюджетные ограничения
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Budget:
    """
    Бюджет.
    limit - ограничение бюджета
    datetime_init - начало периода подсчета бюджета
    datetime_fin - конец периода подсчета бюджета
    category_name - название категории расходов
    """
    limit: int = 0
    datetime_init: datetime = datetime.now()
    datetime_fin: datetime = datetime.now()
    category_name: str = ''
