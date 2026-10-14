from primitive_db.constants import (
    ID_COLUMN,
    ID_TYPE,
    TYPE_MAPPING,
    VALID_TYPES,
)
from primitive_db.decorators import handle_db_errors
from primitive_db.utils import load_table_data


@handle_db_errors
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

@handle_db_errors
def drop_table(metadata, table_name):
    """Удаляет таблицу и возвращает обновлённые метаданные."""
    if table_name not in metadata:
        raise ValueError(f'Ошибка: Таблица "{table_name}" не существует.')
    del metadata[table_name]
    return metadata


def list_tables(metadata):
    """Возвращает список имён всех таблиц."""
    return list(metadata.keys())

@handle_db_errors
def insert(metadata, table_name, values):
    """Добавляет запись с автоматическим ID и возвращает данные."""
    if table_name not in metadata:
        raise ValueError(
            f'Ошибка: Таблица "{table_name}" не существует.'
        )

    schema = metadata[table_name]

    if schema.get(ID_COLUMN) != ID_TYPE:
        raise ValueError("Столбец ID должен иметь тип int.")

    columns = [
        column for column in schema
        if column != ID_COLUMN
    ]

    if len(values) != len(columns):
        raise ValueError(
            f"Ожидалось значений: {len(columns)}, "
            f"получено: {len(values)}."
        )

    for column, value in zip(columns, values):
        expected_type = TYPE_MAPPING[schema[column]]

        if type(value) is not expected_type:
            raise ValueError(
                f'Столбец "{column}" требует тип {schema[column]}.'
            )

    table_data = load_table_data(table_name)

    new_id = max(
        (row[ID_COLUMN] for row in table_data),
        default=0,
    ) + 1

    new_record = {ID_COLUMN: new_id}

    for column, value in zip(columns, values):
        new_record[column] = value

    table_data.append(new_record)
    return table_data

def matches_where(row, where_clause):
    """Проверяет соответствие записи условию."""
    return all(
        row[column] == value
        for column, value in where_clause.items()
    )

@handle_db_errors
def select(table_data, where_clause=None):
    """Возвращает все записи или записи по условию."""
    if where_clause is None:
        return table_data

    return [
        row
        for row in table_data
        if matches_where(row, where_clause)
    ]

@handle_db_errors
def update(table_data, set_clause, where_clause):
    """Обновляет все записи, соответствующие условию."""
    if ID_COLUMN in set_clause:
        raise ValueError("Изменять ID нельзя.")

    for row in table_data:
        if matches_where(row, where_clause):
            row.update(set_clause)

    return table_data

@handle_db_errors
def delete(table_data, where_clause):
    """Удаляет записи по условию и возвращает оставшиеся."""
    return [
        row
        for row in table_data
        if not matches_where(row, where_clause)
    ]

def validate_clause(schema, clause):
    """Проверяет имена столбцов и типы значений условия."""
    for column, value in clause.items():
        if column not in schema:
            raise ValueError(
                f'Столбец "{column}" не существует.'
            )

        expected_type = TYPE_MAPPING[schema[column]]

        if type(value) is not expected_type:
            raise ValueError(
                f'Столбец "{column}" требует тип {schema[column]}.'
            )