import shlex


def parse_value(text):
    """Преобразует текст в строку, целое число или bool."""
    text = text.strip()

    if not text:
        raise ValueError("Значение не должно быть пустым.")

    if text.startswith(("'", '"')):
        quote = text[0]

        if len(text) < 2 or not text.endswith(quote):
            raise ValueError("Строка должна быть в парных кавычках.")

        parts = shlex.split(text)

        if len(parts) != 1:
            raise ValueError("Ожидалось одно строковое значение.")

        return parts[0]

    if text.lower() == "true":
        return True

    if text.lower() == "false":
        return False

    try:
        return int(text)
    except ValueError:
        raise ValueError(
            "Ожидалось целое число, true, false или строка в кавычках."
        ) from None

def parse_assignment(text):
    """Разбирает выражение вида столбец = значение."""
    column, separator, value_text = text.partition("=")
    column = column.strip()

    if not separator:
        raise ValueError("В условии должен быть знак =.")

    if not column or not column.isidentifier():
        raise ValueError("Некорректное имя столбца.")

    value = parse_value(value_text)
    return {column: value}