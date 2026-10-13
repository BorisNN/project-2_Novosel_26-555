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

## CRUD-операции

Записи таблиц сохраняются в отдельных JSON-файлах в папке `data/`.
Столбец `ID` заполняется автоматически.
Поддерживаются типы `int`, `str` и `bool`.
Строковые значения необходимо заключать в кавычки.

### Установка и запуск

```bash
uv sync
uv run database
```

### Пример работы

```text
create_table users name:str age:int is_active:bool
insert into users values ("Sergei", 28, true)
select from users
select from users where age = 28
update users set age = 29 where name = "Sergei"
info users
delete from users where ID = 1
drop_table users
exit
```

### Демонстрация CRUD-операций
https://asciinema.org/a/DV6oWZ1xBg5xUiM0