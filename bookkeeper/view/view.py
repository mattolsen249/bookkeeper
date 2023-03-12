import sys
from typing import Callable
from PySide6 import QtWidgets

from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.view.abstract_view import AbstractView
from bookkeeper.view.main_window import MainWindow


class View(AbstractView):
    """
    Класс View.
    Содержит атрибуты app и window, а также ряд методов,
    обеспечивающих корректное взаимодействие со списками экземпляров моделей
    и их обработку.
    """
    def __init__(self) -> None:
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = MainWindow()

    def run(self) -> None:
        """
        Показ окна и запуск приложения
        """
        self.window.show()
        sys.exit(self.app.exec())

    def set_budget_list(self, budgets: list[Budget]) -> None:
        """
        Получение списка бюджетов
        """
        self.window.set_budget_list(budgets)

    def set_category_list(self, categories: list[Category]) -> None:
        """
        Получение списка категорий
        """
        self.window.set_category_list(categories)

    def set_expense_list(self, expenses: list[Expense]) -> None:
        """
        Получение списка расходов
        """
        self.window.set_expense_list(expenses)

    def register_budget_creator(self,
                                handler: Callable[[Budget], int]) -> None:
        """
        "Регистрация" handler в качестве обработчика
        создания экземпляра модели бюджета
        """
        self.window.budget_creator = handler

    def register_budget_updater(self,
                                handler: Callable[[Budget], None]) -> None:
        """
        "Регистрация" handler в качестве обработчика
        изменения экземпляра модели бюджета.
        """
        self.window.budget_updater = handler

    def register_budget_deleter(self,
                                handler: Callable[[int], None]) -> None:
        """
        "Регистрация" handler в качестве обработчика
        удаления экземпляра модели бюджета.
        """
        self.window.budget_deleter = handler

    def register_category_creator(self,
                                  handler: Callable[[Category], int]) -> None:
        """
        "Регистрация" handler в качестве обработчика
        создания экземпляра модели категории.
        """
        self.window.category_creator = handler

    def register_category_updater(self,
                                  handler: Callable[[Category], None]) -> None:
        """
        "Регистрация" handler в качестве обработчика
        зменения экземпляра модели категории.
        """
        self.window.category_updater = handler

    def register_category_deleter(self,
                                  handler: Callable[[int], None]) -> None:
        """
        "Регистрация" handler в качестве обработчика
        удаления экземпляра модели категории.
        """
        self.window.category_deleter = handler

    def register_expense_creator(self,
                                 handler: Callable[[Expense], int]) -> None:
        """
        "Регистрация" handler в качестве обработчика
        создания экземпляра модели расхода.
        """
        self.window.expense_creator = handler

    def register_expense_updater(self,
                                 handler: Callable[[Expense], None]) -> None:
        """
        "Регистрация" handler в качестве обработчика
        изменения экземпляра модели расхода.
        """
        self.window.expense_updater = handler

    def register_expense_deleter(self,
                                 handler: Callable[[int], None]) -> None:
        """
        "Регистрация" handler в качестве обработчика
        удаления экземпляра модели расхода.
        """
        self.window.expense_deleter = handler
