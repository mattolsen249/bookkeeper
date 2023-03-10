"""
Описан класс, представляющий расходную операцию
"""
from dataclasses import dataclass
from datetime import date
from typing import Tuple


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
    amount: int
    comment: str

    def __init__(self,
                 args: Tuple[str] | None = (date.min, 'Все', 0, ''),
                 pk: int = 0) -> None:
        self.pk = pk
        if args is not None:
            [year, month, day] = args[0].split('-')
            self.expense_date = date(int(year), int(month), int(day))
            self.category_name = args[1]
            self.amount = int(args[2])
            self.comment = args[3]
