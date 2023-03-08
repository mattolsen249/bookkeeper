"""
Описан класс, представляющий расходную операцию
"""

from dataclasses import dataclass, field
from datetime import date


@dataclass(slots=True)
class Expense:
    """
    Расходная операция.
    amount - сумма
    category - id категории расходов
    expense_date - дата расхода
    added_date - дата добавления в бд
    comment - комментарий
    pk - id записи в базе данных
    """
    pk: int
    expense_date: date
    category_name: str
    amount: float
    comment: str

    def __init__(self, attrs: tuple, pk: int = 0) -> None:
        self.pk = pk
        [year, month, day] = attrs[0].split('-')
        self.expense_date = date(int(year), int(month), int(day))
        self.category_name = attrs[1]
        self.amount = float(attrs[2])
        self.comment = attrs[3]

