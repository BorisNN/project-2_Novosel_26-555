import prompt


def welcome() -> None:
    print("Первая попытка запустить проект!")
    print("***")
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация")


def print_help() -> None:
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация")


def run() -> None:
    welcome()
    while True:
        try:
            command = prompt.string("Введите команду: ")
        except (EOFError, KeyboardInterrupt):
            break

        if command == "exit":
            break
        elif command == "help":
            print_help()
        else:
            print(f"Функции {command} нет. Попробуйте снова.")