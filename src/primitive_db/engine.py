import shlex

import prompt
from prettytable import PrettyTable

from primitive_db.constants import ID_COLUMN, META_FILE
from primitive_db.core import (
    create_table,
    drop_table,
    insert,
    list_tables,
    select,
    validate_clause,
)
from primitive_db.parser import parse_assignment, parse_values
from primitive_db.utils import (
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)


def print_help():
    """Выводит список доступных команд."""
    print("\n***Управление таблицами и записями***")
    print("create_table <имя> <столбец:тип> ... - создать таблицу")
    print("list_tables - показать список таблиц")
    print("drop_table <имя> - удалить таблицу")
    print("insert into <имя> values (...) - добавить запись")
    print("select from <имя> - показать все записи")
    print("select from <имя> where <столбец> = <значение> - выборка")
    print("info <имя> - показать информацию о таблице")
    print("help - показать справку")
    print("exit - выйти из программы\n")


def handle_create_table(args):
    """Создаёт таблицу и сохраняет метаданные."""
    if len(args) < 2:
        raise ValueError(
            "Укажите имя таблицы и хотя бы один столбец."
        )

    table_name = args[0]
    columns = args[1:]
    metadata = load_metadata()

    metadata = create_table(metadata, table_name, columns)
    save_metadata(META_FILE, metadata)

    columns_str = ", ".join(
        f"{column}:{column_type}"
        for column, column_type in metadata[table_name].items()
    )

    print(
        f'Таблица "{table_name}" успешно создана '
        f"со столбцами: {columns_str}"
    )


def handle_list_tables():
    """Показывает имена таблиц."""
    metadata = load_metadata()

    for table_name in list_tables(metadata):
        print(f"- {table_name}")


def handle_drop_table(args):
    """Удаляет таблицу из метаданных."""
    if len(args) != 1:
        raise ValueError("Укажите ровно одно имя таблицы.")

    table_name = args[0]
    metadata = load_metadata()

    metadata = drop_table(metadata, table_name)
    save_metadata(META_FILE, metadata)

    print(f'Таблица "{table_name}" успешно удалена.')


def handle_insert(command_text):
    """Разбирает insert и сохраняет новую запись."""
    header, separator, values_text = command_text.partition(" values ")

    if not separator:
        raise ValueError(
            "Формат: insert into <таблица> values (...)"
        )

    args = shlex.split(header)

    if len(args) != 3 or args[:2] != ["insert", "into"]:
        raise ValueError(
            "Формат: insert into <таблица> values (...)"
        )

    table_name = args[2]

    if not table_name.isidentifier():
        raise ValueError("Некорректное имя таблицы.")

    values = parse_values(values_text)
    metadata = load_metadata()

    table_data = insert(metadata, table_name, values)
    save_table_data(table_name, table_data)

    new_id = table_data[-1][ID_COLUMN]

    print(
        f'Запись с ID={new_id} успешно добавлена '
        f'в таблицу "{table_name}".'
    )


def handle_select(command_text):
    """Выводит все записи или выборку по условию."""
    header, separator, condition = command_text.partition(" where ")
    args = shlex.split(header)

    if len(args) != 3 or args[:2] != ["select", "from"]:
        raise ValueError(
            "Формат: select from <таблица> [where столбец = значение]"
        )

    table_name = args[2]
    metadata = load_metadata()

    if table_name not in metadata:
        raise ValueError(
            f'Таблица "{table_name}" не существует.'
        )

    schema = metadata[table_name]
    where_clause = None

    if separator:
        where_clause = parse_assignment(condition)
        validate_clause(schema, where_clause)

    table_data = load_table_data(table_name)
    selected_rows = select(table_data, where_clause)

    table = PrettyTable()
    table.field_names = list(schema)

    for row in selected_rows:
        table.add_row([
            row[column]
            for column in table.field_names
        ])

    print(table)


def handle_info(args):
    """Показывает схему таблицы и количество записей."""
    if len(args) != 1:
        raise ValueError("Укажите ровно одно имя таблицы.")

    table_name = args[0]
    metadata = load_metadata()

    if table_name not in metadata:
        raise ValueError(
            f'Таблица "{table_name}" не существует.'
        )

    columns_str = ", ".join(
        f"{column}:{column_type}"
        for column, column_type in metadata[table_name].items()
    )
    table_data = load_table_data(table_name)

    print(f"Таблица: {table_name}")
    print(f"Столбцы: {columns_str}")
    print(f"Количество записей: {len(table_data)}")


def run():
    """Запускает цикл обработки команд."""
    print_help()

    while True:
        try:
            user_input = prompt.string("Введите команду: ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        user_input = user_input.strip()

        if not user_input:
            continue

        try:
            command = user_input.split(maxsplit=1)[0]

            if command == "insert":
                handle_insert(user_input)
                continue

            if command == "select":
                handle_select(user_input)
                continue

            args = shlex.split(user_input)

            if command == "exit":
                if len(args) != 1:
                    raise ValueError(
                        "Команда exit не принимает аргументы."
                    )
                break

            elif command == "help":
                if len(args) != 1:
                    raise ValueError(
                        "Команда help не принимает аргументы."
                    )
                print_help()

            elif command == "create_table":
                handle_create_table(args[1:])

            elif command == "list_tables":
                if len(args) != 1:
                    raise ValueError(
                        "Команда list_tables не принимает аргументы."
                    )
                handle_list_tables()

            elif command == "drop_table":
                handle_drop_table(args[1:])

            elif command == "info":
                handle_info(args[1:])

            else:
                print(f"Функции {command} нет. Попробуйте снова.")

        except (ValueError, OSError) as error:
            print(f"Ошибка выполнения команды: {error}")