# project-2_Novosel_26-555
## Управление таблицами

Запуск:

    uv run database

Команды:

- `create_table <имя> <столбец:тип> ...` — создать таблицу
- `list_tables` — список таблиц
- `drop_table <имя>` — удалить таблицу
- `help` — справка
- `exit` — выход

Пример:

    create_table users name:str age:int is_active:bool

    ## Демонстрация

    https://asciinema.org/a/hcCmw4ccFtdJy6Zv
