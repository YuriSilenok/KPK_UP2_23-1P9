# Сервис 15: Load Assignment Service (Сервис распределения нагрузки)

## Функционал сервиса
- Добавить Assignment
- Изменить Assignment по ID
- Удаление Assignment по ID
- Получить Assignment по ID
- Получить список Assignment по заданным параметрам
- Добавить Teacher
- Добавить Discipline
- Добавить Group
- Связать Teacher и Discipline (TeacherDiscipline)

## Добавить Assignment
Информация требуемая для создания Assignment представлена в виде таблицы со столбцами:

| Параметр | Обязательность | Тип | Ограничение | Значение по умолчанию |
|---|---|---|---|---|
| teacher_discipline_id | Да | Integer | > 0, внешний ключ | - |
| group_id | Да | Integer | > 0, внешний ключ | - |
| semester | Да | String | Не пустой | - |
| hours | Да | Integer | >= 0 | - |

Перечислить уникальные комбинации параметров, если есть:
Уникальная комбинация `(teacher_discipline_id, group_id, semester)` — один преподаватель не может вести одну дисциплину в одной группе дважды за семестр.

Информация возвращаемая в случае удачного создания Assignment и представлена в виде таблицы со столбцами:

| Параметр | Тип |
|---|---|
| id | Integer |
| teacher_discipline_id | Integer |
| group_id | Integer |
| semester | String |
| hours | Integer |
| created_at | DateTime |

## Добавить Teacher
Информация требуемая для создания Teacher представлена в виде таблицы со столбцами:

| Параметр | Обязательность | Тип | Ограничение | Значение по умолчанию |
|---|---|---|---|---|
| external_id | Да | String | Уникальный, не пустой | - |

Информация возвращаемая в случае удачного создания Teacher и представлена в виде таблицы со столбцами:

| Параметр | Тип |
|---|---|
| id | Integer |
| external_id | String |
| created_at | DateTime |

## Добавить Discipline
Информация требуемая для создания Discipline представлена в виде таблицы со столбцами:

| Параметр | Обязательность | Тип | Ограничение | Значение по умолчанию |
|---|---|---|---|---|
| external_id | Да | String | Уникальный, не пустой | - |
| name | Да | String | Не пустой | - |

Информация возвращаемая в случае удачного создания Discipline и представлена в виде таблицы со столбцами:

| Параметр | Тип |
|---|---|
| id | Integer |
| external_id | String |
| name | String |
| created_at | DateTime |

## Добавить Group
Информация требуемая для создания Group представлена в виде таблицы со столбцами:

| Параметр | Обязательность | Тип | Ограничение | Значение по умолчанию |
|---|---|---|---|---|
| external_id | Да | String | Уникальный, не пустой | - |
| name | Да | String | Не пустой | - |

Информация возвращаемая в случае удачного создания Group и представлена в виде таблицы со столбцами:

| Параметр | Тип |
|---|---|
| id | Integer |
| external_id | String |
| name | String |
| created_at | DateTime |

## Добавить TeacherDiscipline (связь)
Информация требуемая для создания TeacherDiscipline представлена в виде таблицы со столбцами:

| Параметр | Обязательность | Тип | Ограничение | Значение по умолчанию |
|---|---|---|---|---|
| teacher_id | Да | Integer | > 0, внешний ключ | - |
| discipline_id | Да | Integer | > 0, внешний ключ | - |

Перечислить уникальные комбинации параметров, если есть:
Уникальная комбинация `(teacher_id, discipline_id)` — один преподаватель не может быть дважды связан с одной дисциплиной.

Информация возвращаемая в случае удачного создания TeacherDiscipline и представлена в виде таблицы со столбцами:

| Параметр | Тип |
|---|---|
| id | Integer |
| teacher_id | Integer |
| discipline_id | Integer |
| created_at | DateTime |

## Изменить Assignment по ID
Информация требуемая для изменения Assignment по ID представлена в виде таблицы со столбцами:

| Параметр | Обязательность | Тип | Ограничение | Значение по умолчанию |
|---|---|---|---|---|
| id | Да | Integer | > 0 | - |
| semester | Нет | String | Не пустой | - |
| hours | Нет | Integer | >= 0 | - |

Информация возвращаемая в случае удачного изменения Assignment и представлена в виде таблицы со столбцами:

| Параметр | Тип |
|---|---|
| id | Integer |
| teacher_discipline_id | Integer |
| group_id | Integer |
| semester | String |
| hours | Integer |
| updated_at | DateTime |

## Удаление Assignment по ID
Вернет True, если Assignment был удалён, иначе вернет False.

## Получить Assignment по ID
Информация возвращаемая в случае удачного поиска Assignment по ID и представлена в виде таблицы со столбцами:

| Параметр | Тип |
|---|---|
| id | Integer |
| teacher_discipline_id | Integer |
| group_id | Integer |
| semester | String |
| hours | Integer |
| created_at | DateTime |

## Получить список Assignment по заданным параметрам
Информация требуемая для получения списка Assignment представлена в виде таблицы со столбцами:

| Параметр | Тип | Описание |
|---|---|---|
| teacher_id | Integer | Фильтрация по ID преподавателя |
| discipline_id | Integer | Фильтрация по ID дисциплины |
| group_id | Integer | Фильтрация по ID группы |
| semester | String | Фильтрация по семестру |
| hours_min | Integer | Минимальное количество часов |
| hours_max | Integer | Максимальное количество часов |
| limit | Integer | Количество записей в ответе (по умолчанию 50) |
| offset | Integer | Смещение для пагинации (по умолчанию 0) |

Информация возвращается в виде списка Assignment и представлена в виде таблицы со столбцами:

| Параметр | Тип |
|---|---|
| id | Integer |
| teacher_discipline_id | Integer |
| group_id | Integer |
| semester | String |
| hours | Integer |
| created_at | DateTime |

## Получить Teacher по ID
Информация возвращаемая в случае удачного поиска Teacher по ID и представлена в виде таблицы со столбцами:

| Параметр | Тип |
|---|---|
| id | Integer |
| external_id | String |
| created_at | DateTime |

## Получить Discipline по ID
Информация возвращаемая в случае удачного поиска Discipline по ID и представлена в виде таблицы со столбцами:

| Параметр | Тип |
|---|---|
| id | Integer |
| external_id | String |
| name | String |
| created_at | DateTime |

## Получить Group по ID
Информация возвращаемая в случае удачного поиска Group по ID и представлена в виде таблицы со столбцами:

| Параметр | Тип |
|---|---|
| id | Integer |
| external_id | String |
| name | String |
| created_at | DateTime |

## Получить дисциплины преподавателя по ID преподавателя
Информация возвращается в виде списка Discipline и представлена в виде таблицы со столбцами:

| Параметр | Тип |
|---|---|
| id | Integer |
| external_id | String |
| name | String |

## Получить преподавателей дисциплины по ID дисциплины
Информация возвращается в виде списка Teacher и представлена в виде таблицы со столбцами:

| Параметр | Тип |
|---|---|
| id | Integer |
| external_id | String |
