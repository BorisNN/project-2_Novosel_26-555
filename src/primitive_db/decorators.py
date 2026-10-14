import prompt


def handle_db_errors(func):
    """Перехватывает ошибки базы данных и выводит сообщение."""
    def wrapper(*args, **kwargs):
        """Вызывает функцию с обработкой ошибок."""
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print(
                "Ошибка: Файл данных не найден. "
                "Возможно, база данных не инициализирована."
            )
        except KeyError as error:
            print(
                f"Ошибка: Таблица или столбец {error} не найден."
            )
        except ValueError as error:
            print(f"Ошибка валидации: {error}")
        except OSError as error:
            print(f"Ошибка работы с файлами: {error}")

        return None

    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper


def confirm_action(action_name):
    """Создаёт декоратор подтверждения опасного действия."""
    def decorator(func):
        """Оборачивает функцию запросом подтверждения."""
        def wrapper(*args, **kwargs):
            """Выполняет действие только после подтверждения."""
            try:
                answer = prompt.string(
                    f'Вы уверены, что хотите выполнить '
                    f'"{action_name}"? [y/n]: '
                )
            except (EOFError, KeyboardInterrupt):
                print("\nОперация отменена.")
                return None

            if answer.strip().lower() != "y":
                print("Операция отменена.")
                return None

            return func(*args, **kwargs)

        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper

    return decorator