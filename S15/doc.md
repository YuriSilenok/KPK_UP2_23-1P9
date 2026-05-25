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

| Параметр | Обязательность | Тип | Ограничение | Значение по умолчанию | Пояснение |
|---|---|---|---|---|---|
| teacher_id | Да | Integer | > 0, внешний ключ | - | ID преподавателя (из Teacher) |
| discipline_id | Да | Integer | > 0, внешний ключ | - | ID дисциплины (из Discipline) |
| group_id | Да | Integer | > 0, внешний ключ | - | ID группы |
| semester | Да | String | Не пустой | - | Семестр |
| hours | Да | Integer | >= 0 | - | Количество часов |

**Уникальная комбинация:** `(teacher_id, discipline_id, group_id, semester)`

**Возврат при успехе:**

| Параметр | Тип | Пояснение |
|---|---|---|
| id | Integer | ID назначения |
| teacher_id | Integer | ID преподавателя |
| discipline_id | Integer | ID дисциплины |
| group_id | Integer | ID группы |
| semester | String | Семестр |
| hours | Integer | Часы |
| created_at | DateTime | Дата создания |

## Изменить Assignment по ID

| Параметр | Обязательность | Тип | Ограничение | Значение по умолчанию | Пояснение |
|---|---|---|---|---|---|
| id | Да | Integer | > 0 | - | ID назначения |
| semester | Нет | String | Не пустой | - | Новый семестр |
| hours | Нет | Integer | >= 0 | - | Новые часы |

**Возврат при успехе:**

| Параметр | Тип | Пояснение |
|---|---|---|
| id | Integer | ID назначения |
| teacher_id | Integer | ID преподавателя |
| discipline_id | Integer | ID дисциплины |
| group_id | Integer | ID группы |
| semester | String | Семестр |
| hours | Integer | Часы |
| updated_at | DateTime | Дата обновления |

## Добавить Teacher

| Параметр | Обязательность | Тип | Ограничение | Значение по умолчанию | Пояснение |
|---|---|---|---|---|---|
| external_id | Да | String | Уникальный, не пустой | - | ID из сервиса профилей |

**Возврат при успехе:**

| Параметр | Тип | Пояснение |
|---|---|---|
| id | Integer | ID преподавателя |
| external_id | String | Внешний ID |
| created_at | DateTime | Дата создания |

## Добавить Discipline

| Параметр | Обязательность | Тип | Ограничение | Значение по умолчанию | Пояснение |
|---|---|---|---|---|---|
| external_id | Да | String | Уникальный, не пустой | - | ID из сервиса дисциплин |
| name | Да | String | Не пустой | - | Название дисциплины |

**Возврат при успехе:**

| Параметр | Тип | Пояснение |
|---|---|---|
| id | Integer | ID дисциплины |
| external_id | String | Внешний ID |
| name | String | Название |
| created_at | DateTime | Дата создания |

## Добавить Group

| Параметр | Обязательность | Тип | Ограничение | Значение по умолчанию | Пояснение |
|---|---|---|---|---|---|
| external_id | Да | String | Уникальный, не пустой | - | ID из сервиса групп |
| name | Да | String | Не пустой | - | Название группы |

**Возврат при успехе:**

| Параметр | Тип | Пояснение |
|---|---|---|
| id | Integer | ID группы |
| external_id | String | Внешний ID |
| name | String | Название |
| created_at | DateTime | Дата создания |

## Добавить TeacherDiscipline (связь многие ко многим)

| Параметр | Обязательность | Тип | Ограничение | Значение по умолчанию | Пояснение |
|---|---|---|---|---|---|
| teacher_id | Да | Integer | > 0, внешний ключ | - | ID преподавателя |
| discipline_id | Да | Integer | > 0, внешний ключ | - | ID дисциплины |

**Уникальная комбинация:** `(teacher_id, discipline_id)`

**Возврат при успехе:**

| Параметр | Тип | Пояснение |
|---|---|---|
| id | Integer | ID связи |
| teacher_id | Integer | ID преподавателя |
| discipline_id | Integer | ID дисциплины |
| created_at | DateTime | Дата создания |

## Удаление Assignment по ID
Вернет `True`, если удалён, иначе `False`.

## Получить Assignment по ID

| Параметр | Тип | Пояснение |
|---|---|---|
| id | Integer | ID назначения |
| teacher_id | Integer | ID преподавателя |
| discipline_id | Integer | ID дисциплины |
| group_id | Integer | ID группы |
| semester | String | Семестр |
| hours | Integer | Часы |
| created_at | DateTime | Дата создания |

## Получить список Assignment по параметрам

| Параметр | Тип | Описание | Пояснение |
|---|---|---|---|
| teacher_id | Integer | Фильтр | ID преподавателя |
| discipline_id | Integer | Фильтр | ID дисциплины |
| group_id | Integer | Фильтр | ID группы |
| semester | String | Фильтр | Семестр |
| hours_min | Integer | Фильтр | Часы >= |
| hours_max | Integer | Фильтр | Часы <= |
| limit | Integer | Пагинация | По умолчанию 50 |
| offset | Integer | Пагинация | По умолчанию 0 |

**Возврат:** список Assignment (те же поля, что при получении по ID)

## Получить Teacher по ID

| Параметр | Тип | Пояснение |
|---|---|---|
| id | Integer | ID преподавателя |
| external_id | String | Внешний ID |
| created_at | DateTime | Дата создания |

## Получить Discipline по ID

| Параметр | Тип | Пояснение |
|---|---|---|
| id | Integer | ID дисциплины |
| external_id | String | Внешний ID |
| name | String | Название |
| created_at | DateTime | Дата создания |

## Получить Group по ID

| Параметр | Тип | Пояснение |
|---|---|---|
| id | Integer | ID группы |
| external_id | String | Внешний ID |
| name | String | Название |
| created_at | DateTime | Дата создания |

## Получить дисциплины преподавателя по ID преподавателя

**Возврат:** список Discipline (id, external_id, name)

## Получить преподавателей дисциплины по ID дисциплины

**Возврат:** список Teacher (id, external_id)
