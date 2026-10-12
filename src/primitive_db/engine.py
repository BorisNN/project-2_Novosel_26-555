import shlex

import prompt

from primitive_db.constants import META_FILE
from primitive_db.core import create_table, drop_table, list_tables
from primitive_db.utils import load_metadata, save_metadata


def print_help():
    """Prints the help message for the current mode."""
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print(
        "<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу"
    )
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def handle_create_table(args):
    if not args:
        print("Некорректное значение: . Попробуйте снова.")
        return

    table_name = args[0]
    columns = args[1:]
    metadata = load_metadata()

    try:
        metadata = create_table(metadata, table_name, columns)
        save_metadata(META_FILE, metadata)
        columns_str = ", ".join(
            f"{col}:{typ}" for col, typ in metadata[table_name].items()
        )
        print(
            f'Таблица "{table_name}" успешно создана со столбцами: {columns_str}'
        )
    except ValueError as error:
        print(error)


def handle_list_tables():
    metadata = load_metadata()
    for table_name in list_tables(metadata):
        print(f"- {table_name}")


def handle_drop_table(args):
    if not args:
        print("Некорректное значение: . Попробуйте снова.")
        return

    table_name = args[0]
    metadata = load_metadata()

    try:
        metadata = drop_table(metadata, table_name)
        save_metadata(META_FILE, metadata)
        print(f'Таблица "{table_name}" успешно удалена.')
    except ValueError as error:
        print(error)


def run():
    print_help()

    while True:
        try:
            user_input = prompt.string("Введите команду: ")
        except (EOFError, KeyboardInterrupt):
            break

        if not user_input.strip():
            continue

        args = shlex.split(user_input)
        if not args:
            continue

        command = args[0]

        if command == "exit":
            break
        elif command == "help":
            print_help()
        elif command == "create_table":
            handle_create_table(args[1:])
        elif command == "list_tables":
            handle_list_tables()
        elif command == "drop_table":
            handle_drop_table(args[1:])
        else:
            print(f"Функции {command} нет. Попробуйте снова.")