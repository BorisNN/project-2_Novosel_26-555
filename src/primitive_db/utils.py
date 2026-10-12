import json

from primitive_db.constants import META_FILE


def load_metadata(file_path=META_FILE):
    """Загружает метаданные из JSON-файла."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_metadata(file_path, data):
    """Сохраняет данные в JSON-файл."""
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)