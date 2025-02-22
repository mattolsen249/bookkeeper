"""
Модуль описывает структуру окна приложения
"""

from datetime import datetime, timedelta
from typing import Callable

from PySide6 import QtWidgets

from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.view.accessory_widgets import BudgetWidget
from bookkeeper.view.category_widgets import CategoryWidget, AddCategoryWidget
from bookkeeper.view.expense_widgets import ExpensesWidget, AddExpensesWidget


class MainWindow(QtWidgets.QMainWindow):
    """
    Виджет главного окна, содержащий все остальные виджеты
    """
    DAY = 1
    WEEK = 7
    MONTH = 30

    def __init__(self) -> None:
        super().__init__()
        self.category_id_name_mapping: dict[int, str] = {}
        self.category_name_id_mapping: dict[str, int] = {}
        self.categories: list[Category] = []
        self.budgets: list[Budget] = []
        self.expenses: list[Expense] = []
        self.category_creator: Callable[[Category], int] = lambda x: -1
        self.category_updater: Callable[[Category], None] = lambda x: None
        self.category_deleter: Callable[[int], None] = lambda x: None
        self.budget_creator: Callable[[Budget], int] = lambda x: -1
        self.budget_updater: Callable[[Budget], None] = lambda x: None
        self.budget_deleter: Callable[[int], None] = lambda x: None
        self.expense_creator: Callable[[Expense], int] = lambda x: -1
        self.expense_updater: Callable[[Expense], None] = lambda x: None
        self.expense_deleter: Callable[[int], None] = lambda x: None

        # Название окна и размер окна в пикселях
        self.setWindowTitle('Бухгалтер')
        self.setFixedSize(800, 600)

        # Центральный виджет, установка его по центру
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)

        # Вкладки
        tabs = QtWidgets.QTabWidget(central_widget)
        tabs.resize(self.size())
        bookkeeper_tab = QtWidgets.QWidget()
        category_tab = QtWidgets.QWidget()
        tabs.addTab(bookkeeper_tab, "Бухгалтер")
        tabs.addTab(category_tab, "Категории")

        # Вкладка "Бухгалтер"
        main_layout = QtWidgets.QVBoxLayout(bookkeeper_tab)
        self.expenses_table = ExpensesWidget()
        self.budget_table = BudgetWidget()
        self.add_expense = AddExpensesWidget()
        main_layout.addWidget(self.expenses_table)
        main_layout.addWidget(self.budget_table)
        main_layout.addWidget(self.add_expense)

        # Вкладка "Категории"
        category_layout = QtWidgets.QVBoxLayout(category_tab)
        self.category_table = CategoryWidget()
        self.add_category = AddCategoryWidget()
        category_layout.addWidget(self.category_table)
        category_layout.addWidget(self.add_category)

        self.expenses_table.activate_editing_mode_signal.connect(
            self.activate_expense_editing_mode)
        self.add_expense.cancel_signal.connect(
            self.deactivate_expense_editing_mode)
        self.add_expense.delete_signal.connect(self.delete_expense)
        self.add_expense.update_signal.connect(self.update_expense)
        self.add_expense.create_signal.connect(self.create_expense)

        self.category_table.activate_editing_mode_signal.connect(
            self.activate_category_editing_mode)
        self.add_category.cancel_signal.connect(
            self.deactivate_category_editing_mode)
        self.add_category.delete_signal.connect(self.delete_category)
        self.add_category.update_signal.connect(self.update_category)
        self.add_category.create_signal.connect(self.create_category)

        self.budget_table.table.itemChanged.connect(self.on_budget_item_changed)

    def activate_expense_editing_mode(self, row_index: int) -> None:
        """
        Активировать режим изменения расхода
        """
        self.expenses_table.set_edit_buttons_active(False)
        self.add_expense.activate_editing_mode(
            self.expenses[row_index],
            self.category_id_name_mapping[self.expenses[row_index].category])

    def deactivate_expense_editing_mode(self) -> None:
        """
        Дективировать режим изменения расхода
        """
        self.expenses_table.set_edit_buttons_active(True)
        self.add_expense.deactivate_editing_mode()

    def create_expense(self, expense: Expense, cat: str) -> None:
        """
        Cоздать расход
        """
        expense.category = self.category_name_id_mapping[cat]
        self.expense_creator(expense)

    def update_expense(self, expense: Expense, cat: str) -> None:
        """
        Изменить расход
        """
        expense.category = self.category_name_id_mapping[cat]
        self.expense_updater(expense)
        self.deactivate_expense_editing_mode()

    def delete_expense(self, pk: int) -> None:
        """
        Удалить расход
        """
        self.expense_deleter(pk)
        self.deactivate_expense_editing_mode()

    def activate_category_editing_mode(self, row_index: int) -> None:
        """
        Активировать режим изменения категории
        """
        self.category_table.set_edit_buttons_active(False)
        self.add_category.activate_editing_mode(
            self.categories[row_index])

    def deactivate_category_editing_mode(self) -> None:
        """
        Деактивировать режим изменения категории
        """
        self.category_table.set_edit_buttons_active(True)
        self.add_category.deactivate_editing_mode()

    def create_category(self, category: Category) -> None:
        """
        Создать категорию
        """
        print('create_category')
        self.category_creator(category)

    def update_category(self, category: Category) -> None:
        """
        Изменить категорию
        """
        self.category_updater(category)
        self.deactivate_category_editing_mode()

    def delete_category(self, pk: int) -> None:
        """
        Удалить категорию
        """
        self.category_deleter(pk)
        self.deactivate_category_editing_mode()

    def set_category_list(self, categories: list[Category]) -> None:
        """
        Получить список категорий
        """
        self.categories = categories
        self.category_id_name_mapping = {c.pk: c.name for c in categories}
        self.category_name_id_mapping = {c.name: c.pk for c in categories}
        self.add_expense.cat_input.clear()
        self.add_expense.cat_input.addItems([c.name for c in categories])
        self.category_table.set_data(categories)

    def set_budget_list(self, budgets: list[Budget]) -> None:
        """
        Получить список бюджетов
        """
        self.budgets = budgets
        for_day = self.get_bud_by_cat_and_dur(budgets, None, self.DAY)
        for_week = self.get_bud_by_cat_and_dur(budgets, None, self.WEEK)
        for_month = self.get_bud_by_cat_and_dur(budgets, None, self.MONTH)
        self.budget_table.set_budgets([for_day, for_week, for_month])

    def set_expense_list(self, expenses: list[Expense]) -> None:
        """
        Получить список расходов
        """
        self.expenses = expenses
        self.expenses_table.set_data(expenses, self.category_id_name_mapping)
        day_exp, week_exp, month_exp = 0, 0, 0
        today = datetime.now()
        for exp in expenses:
            if exp.expense_date >= today - timedelta(days=self.DAY):
                day_exp += exp.amount
            if exp.expense_date >= today - timedelta(days=self.WEEK):
                week_exp += exp.amount
            if exp.expense_date >= today - timedelta(days=self.MONTH):
                month_exp += exp.amount
        self.budget_table.set_expenses([day_exp, week_exp, month_exp])

    def on_budget_item_changed(self,
                               item: QtWidgets.QTableWidgetItem) -> None:
        """
        Изменить структуру бюджета
        """
        old_budgets = self.budget_table.budgets
        if item.column() == 1 and item.text() != '':
            if old_budgets[item.row()] is None:
                new_budget = Budget([self.DAY,
                                     self.WEEK,
                                     self.MONTH][item.row()],
                                    None,
                                    int(item.text()))
                self.budget_creator(new_budget)
            elif item.text() != str(old_budgets[item.row()].amount):
                new_budget = old_budgets[item.row()]
                new_budget.amount = int(item.text())
                self.budget_updater(new_budget)

    @staticmethod
    def get_bud_by_cat_and_dur(
            budgets: list[Budget], cat: int | None, duration: int) -> Budget:
        """
        Получить бюджет по категории и сроку
        """
        return next(
            (b for b in budgets if b.duration == duration
             and b.category == cat),
            None)
