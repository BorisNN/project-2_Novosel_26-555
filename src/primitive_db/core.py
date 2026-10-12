from primitive_db.constants import ID_COLUMN, ID_TYPE, VALID_TYPES


def create_table(metadata, table_name, columns):
    """Создаёт таблицу и возвращает обновлённые метаданные."""
    if table_name in metadata:
        raise ValueError(f'Ошибка: Таблица "{table_name}" уже существует.')

    parsed_columns = {}
    for column in columns:
        if ":" not in column:
            raise ValueError(
                f"Некорректное значение: {column}. Попробуйте снова."
            )
        name, column_type = column.split(":", 1)
        if column_type not in VALID_TYPES:
            raise ValueError(
                f"Некорректное значение: {column_type}. Попробуйте снова."
            )
        parsed_columns[name] = column_type

    metadata[table_name] = {ID_COLUMN: ID_TYPE, **parsed_columns}
    return metadata


def drop_table(metadata, table_name):
    """Удаляет таблицу и возвращает обновлённые метаданные."""
    if table_name not in metadata:
        raise ValueError(f'Ошибка: Таблица "{table_name}" не существует.')
    del metadata[table_name]
    return metadata


def list_tables(metadata):
    """Возвращает список имён всех таблиц."""
    return list(metadata.keys())