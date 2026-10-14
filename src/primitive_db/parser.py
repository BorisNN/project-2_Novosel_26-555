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


def parse_values(text):
    """Разбирает значения в скобках с учётом кавычек."""
    text = text.strip()

    if not text.startswith("(") or not text.endswith(")"):
        raise ValueError("Значения должны быть внутри скобок.")

    content = text[1:-1].strip()

    if not content:
        return []

    values = []
    current = []
    quote = None
    escaped = False

    for character in content:
        if escaped:
            current.append(character)
            escaped = False
            continue

        if quote is not None:
            current.append(character)

            if character == "\\":
                escaped = True
            elif character == quote:
                quote = None

        elif character in ("'", '"'):
            quote = character
            current.append(character)

        elif character == ",":
            values.append(parse_value("".join(current)))
            current = []

        else:
            current.append(character)

    if quote is not None:
        raise ValueError("Строка должна быть в парных кавычках.")

    values.append(parse_value("".join(current)))
    return values


def split_keyword(text, keyword):
    """Разделяет команду по ключевому слову вне кавычек."""
    marker = f" {keyword} "
    quote = None
    escaped = False

    for index, character in enumerate(text):
        if escaped:
            escaped = False
            continue

        if quote is not None:
            if character == "\\":
                escaped = True
            elif character == quote:
                quote = None
            continue

        if character in ("'", '"'):
            quote = character
            continue

        if text.startswith(marker, index):
            return (
                text[:index].strip(),
                True,
                text[index + len(marker) :].strip(),
            )

    return text.strip(), False, ""
