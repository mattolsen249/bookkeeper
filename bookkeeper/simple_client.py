"""
Скрипт для работы с репозиторием из терминала
"""
from collections import deque
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget


def get_type(type_name: str) -> type:
    """
    Функция возвращает тип по его названию, заданному строкой
    """
    query = deque([object])
    while query:
        type_type = query.popleft()
        if type_type.__name__ == type_name:
            return type_type

        try:
            query.extend(type_type.__subclasses__())
        except TypeError:
            if type_type is type:
                continue


available_command_actions = ['quit',
                             'add',
                             'get_all',
                             'get',
                             'update',
                             'delete',
                             'help']


print('Type \'help\' for simple example of commands')
while True:
    command = input('$> ')
    command_items = command.split(' ')
    command_action = command_items[0]
    if command_action not in available_command_actions:
        print('Wrong command. Use \'help\' to get an example')
        continue
    elif command_action == 'quit':
        break
    elif command_action == 'help':
        print('EXAMPLE:\n'
              'add category Яблоки Фрукты\n'
              'get category 1 (existent or nonexistent pk)\n'
              'get_all category\n'
              'get_all category parent=\'Фрукты\'\n'
              'update category 1 Груши Фрукты\n'
              'delete category 2 (existent or nonexistent pk)\n'
              'quit'
              )
    else:
        cls = get_type(command_items[1].title())
        repo = SQLiteRepository('bookkeeper.db', cls)
        if len(command_items[2:]) > 0:
            args = command_items[2:]
            for arg in args:
                if arg == 'None' or arg == 'NULL':
                    arg = None
        else:
            args = None
        if command_action == 'add':
            try:
                repo.add(cls(args))
            except ValueError:
                print('Wrong syntax of command \'add\'')

        elif command_action == 'get_all':
            try:
                print('\n'.join([str(item) for item in repo.get_all(args)]))
            except ValueError:
                print('Error in \'getall\' method')

        elif command_action == 'get':
            try:
                print(repo.get(int(args[0])))
            except ValueError:
                print('Error in \'get\' method')

        elif command_action == 'update':
            try:
                repo.update(pk=int(args[0]), args=tuple(args[1:]))
            except ValueError:
                print('Error in \'update\' method')

        elif command_action == 'delete':
            try:
                repo.delete(int(args[0]))
            except ValueError:
                print('Error: wrong syntax of command \'delete\'')
