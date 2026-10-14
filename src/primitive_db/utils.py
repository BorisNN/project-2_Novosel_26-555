import json
import os

from primitive_db.constants import DATA_DIR, META_FILE


def load_metadata(file_path=META_FILE):
    """Загружает метаданные из JSON-файла."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_metadata(file_path, data):
    """Сохраняет метаданные в JSON-файл."""
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def load_table_data(table_name):
    """Загружает записи таблицы из JSON-файла."""
    file_path = os.path.join(DATA_DIR, f"{table_name}.json")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_table_data(table_name, data):
    """Сохраняет записи таблицы в JSON-файл."""
    os.makedirs(DATA_DIR, exist_ok=True)
    file_path = os.path.join(DATA_DIR, f"{table_name}.json")

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def remove_table_data(table_name):
    """Удаляет файл записей таблицы, если он существует."""
    file_path = os.path.join(DATA_DIR, f"{table_name}.json")

    try:
        os.remove(file_path)
    except FileNotFoundError:
        pass
