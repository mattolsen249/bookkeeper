"""
Простой тестовый скрипт для терминала
"""
from collections import deque
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.models.expense import Expense


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
              'add category Огурцы Овощи\n'
              'add category Памидоры Овощи\n'
              'get_all category\n'
              'update category 3 Помидоры Овощи\n'
              'get_all category parent Овощи\n'
              'delete category 2\n'
              'add category Груши Фрукты\n'
              'get_all category\n'
              'delete category 1\n'
              'delete category 3\n'
              'delete category 4\n'
              'quit'
              )
    else:
        cls = get_type(command_items[1].title())
        repo = SQLiteRepository('bookkeeper.db', cls)
        if command_action == 'add':
            try:
                attrs = command_items[2:]
                for attr in attrs:
                    if attr == 'None':
                        attr = None
                repo.add(cls(tuple(attrs)))
            except ValueError:
                print('Wrong syntax of command \'add\'')
        elif command_action == 'get_all':
            try:
                if len(command.split(' ')) == 2:
                    print('\n'.join([str(item) for item in repo.get_all()]))
                else:
                    attrs = command_items[2:]
                    [where_attr, where_value] = attrs
                    print('\n'.join([str(item) for item in
                                     repo.get_all({where_attr: where_value})]))
            except ValueError:
                print('Error in \'getall\' method')
        elif command_action == 'get':
            try:
                attrs = command_items[2:]
                print(repo.get(int(attrs[0])))
            except ValueError:
                print('Error in \'get\' method')
        elif command_action == 'update':
            try:
                attrs = command_items[2:]
                repo.update(pk=int(attrs[0]), attrs=tuple(attrs))
            except ValueError:
                print('Error in \'update\' method')
        elif command_action == 'delete':
            try:
                attrs = command_items[2:]
                repo.delete(int(attrs[0]))
            except ValueError:
                print('Error: wrong syntax of command \'delete\'')
