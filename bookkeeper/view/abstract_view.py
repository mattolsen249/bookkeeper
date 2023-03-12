"""
Модуль описывает абстрактный view
"""

from typing import Protocol, Callable

from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense


class AbstractView(Protocol):
    """
    Класс абстракного View.
    Должен содержать атрибуты app и window, а также ряд методов,
    обеспечивающих корректное взаимодействие со списками экземпляров моделей
    и их обработку.
    """

    def run(self) -> None:
        """
        Показ окна и запуск приложения
        """

    def set_budget_list(self, budgets: list[Budget]) -> None:
        """
        Получение списка бюджетов
        """

    def set_category_list(self, categories: list[Category]) -> None:
        """
        Получение списка категорий
        """

    def set_expense_list(self, expenses: list[Expense]) -> None:
        """
        Получение списка расходов
        """

    def register_budget_creator(self,
                                handler: Callable[[Budget], int]) -> None:
        """
        "Регистрация" handler в качестве обработчика
        создания экземпляра модели бюджета
        """

    def register_budget_updater(self,
                                handler: Callable[[Budget], None]) -> None:
        """
        "Регистрация" handler в качестве обработчика
        изменения экземпляра модели бюджета.
        """

    def register_budget_deleter(self,
                                handler: Callable[[int], None]) -> None:
        """
        "Регистрация" handler в качестве обработчика
        удаления экземпляра модели бюджета.
        """

    def register_category_creator(self,
                                  handler: Callable[[Category], int]) -> None:
        """
        "Регистрация" handler в качестве обработчика
        создания экземпляра модели категории.
        """

    def register_category_updater(self,
                                  handler: Callable[[Category], None]) -> None:
        """
        "Регистрация" handler в качестве обработчика
        зменения экземпляра модели категории.
        """

    def register_category_deleter(self,
                                  handler: Callable[[int], None]) -> None:
        """
        "Регистрация" handler в качестве обработчика
        удаления экземпляра модели категории.
        """

    def register_expense_creator(self,
                                 handler: Callable[[Expense], int]) -> None:
        """
        "Регистрация" handler в качестве обработчика
        создания экземпляра модели расхода.
        """

    def register_expense_updater(self,
                                 handler: Callable[[Expense], None]) -> None:
        """
        "Регистрация" handler в качестве обработчика
        изменения экземпляра модели расхода.
        """

    def register_expense_deleter(self,
                                 handler: Callable[[int], None]) -> None:
        """
        "Регистрация" handler в качестве обработчика
        удаления экземпляра модели расхода.
        """
