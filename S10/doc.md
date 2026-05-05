# Сервис статуса сотрудника (вариант 10)

## Список функций
- `create_employee` – создание сотрудника  
- `update_employee` – изменение сотрудника по ID  
- `delete_employee` – удаление (закрытие) сотрудника по ID  
- `get_employee` – получение сотрудника по ID  
- `list_employees` – получение списка сотрудников по заданным параметрам  

---

## Сущность «Сотрудник»

### 1. Создание сотрудника

**Информация, требуемая для создания сотрудника**

| Параметр      | Обязательность | Тип     | Ограничение                                  | Значение по умолчанию |
|---------------|----------------|---------|----------------------------------------------|-----------------------|
| `full_name`   | Да             | string  | длина ≤ 255                                  | –                     |
| `birth_date`  | Да             | date    | не может быть в будущем                      | –                     |
| `hire_date`   | Да             | date    | не может раньше 1900 года                    | –                     |
| `email`       | Нет            | string  | уникальный, формат email                     | `NULL`                |
| `phone`       | Нет            | string  | формат +7XXXXXXXXXX                          | `NULL`                |
| `address`     | Нет            | string  | –                                            | `NULL`                |
| `status`      | Нет            | string  | active / on_vacation / sick_leave / fired    | `'active'`            |

**Уникальные комбинации параметров:**  
- `email` (глобальная уникальность)  
- `(full_name, birth_date)` – уникальный идентификатор личности

**Информация, возвращаемая при успешном создании**

| Параметр      | Тип     |
|---------------|---------|
| `id`          | int     |
| `full_name`   | string  |
| `hire_date`   | date    |
| `status`      | string  |

---

### 2. Изменение сотрудника по ID

**Информация, требуемая для изменения сотрудника** (все поля опциональны)

| Параметр      | Обязательность | Тип     | Ограничение                                  | Значение по умолчанию |
|---------------|----------------|---------|----------------------------------------------|-----------------------|
| `full_name`   | Нет            | string  | длина ≤ 255                                  | –                     |
| `birth_date`  | Нет            | date    | не может быть в будущем                      | –                     |
| `hire_date`   | Нет            | date    | не может раньше 1900 года                    | –                     |
| `email`       | Нет            | string  | уникальный, формат email                     | –                     |
| `phone`       | Нет            | string  | формат +7XXXXXXXXXX                          | –                     |
| `address`     | Нет            | string  | –                                            | –                     |
| `status`      | Нет            | string  | active / on_vacation / sick_leave / fired    | –                     |

**Информация, возвращаемая при успешном изменении**

| Параметр      | Тип      |
|---------------|----------|
| `id`          | int      |
| `full_name`   | string   |
| `status`      | string   |
| `updated_at`  | datetime |

---

### 3. Удаление сотрудника по ID

> Вернёт `True`, если сотрудник был закрыт (удалён), иначе `False`.  
> *Примечание:* «Удаление» понимается как мягкое удаление – установка статуса `fired`. Физического удаления из БД не происходит.

---

### 4. Получение сотрудника по ID

**Информация, возвращаемая при успешном поиске**

| Параметр      | Тип               |
|---------------|-------------------|
| `id`          | int               |
| `full_name`   | string            |
| `birth_date`  | date              |
| `hire_date`   | date              |
| `email`       | string (или null) |
| `phone`       | string (или null) |
| `address`     | string (или null) |
| `status`      | string            |
| `positions`   | list (должности)  |

---

### 5. Получение списка сотрудников по заданным параметрам

**Параметры для получения списка**

| Параметр        | Тип     | Описание                                      |
|-----------------|---------|-----------------------------------------------|
| `full_name`     | string  | поиск по частичному совпадению (подстрока)    |
| `status`        | string  | точное совпадение статуса                     |
| `position_id`   | int     | ID должности (фильтр по транзитивной таблице) |
| `hire_date_from`| date    | дата найма не ранее                           |
| `hire_date_to`  | date    | дата найма не позднее                         |
| `limit`         | int     | максимальное количество записей (default 100) |
| `offset`        | int     | смещение для пагинации                        |

**Информация, возвращаемая в виде списка сотрудников**  
(каждый элемент списка)

| Параметр    | Тип     |
|-------------|---------|
| `id`        | int     |
| `full_name` | string  |
| `hire_date` | date    |
| `status`    | string  |

---

## ER-диаграмма (3НФ, с транзитивной таблицей)

```mermaid
erDiagram
    Employee {
        int id PK
        string full_name
        date birth_date
        date hire_date
        string email UK
        string phone
        string address
        string status
    }
    Position {
        int id PK
        string title
        string description
    }
    EmployeePosition {
        int id PK
        int employee_id FK
        int position_id FK
        date start_date
        date end_date
        float load_factor
    }
    Vacation {
        int id PK
        int employee_id FK
        date start_date
        date end_date
        string type
    }
    SickLeave {
        int id PK
        int employee_id FK
        date start_date
        date end_date
        string diagnosis
    }

    Employee ||--o{ EmployeePosition : has
    Position ||--o{ EmployeePosition : has
    Employee ||--o{ Vacation : has
    Employee ||--o{ SickLeave : has