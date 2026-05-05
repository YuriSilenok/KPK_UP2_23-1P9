# Сервис пула ресурсов (Resource Pool Service)

## Описание сервиса
Сервис предназначен для учёта ресурсов (спортивный инвентарь, библиотечные фонды, передвижные лаборатории и т.п.), их категорий и бронирований. Реализует базовые CRUD операции над ресурсами.

## Основная сущность: `Resource` (Ресурс)

### 1. Создание ресурса

**Параметры запроса**

| Параметр (англ) | Пояснение | Обязательность | Тип | Ограничение | Значение по умолчанию |
|----------------|-----------|----------------|-----|-------------|-----------------------|
| name           | Название ресурса | Да | string | 1–100 символов | - |
| description    | Описание ресурса | Нет | string | до 500 символов | null |
| category_id    | Идентификатор категории | Да | integer | существующий id из ResourceCategory | - |
| total_quantity | Общее количество единиц | Да | integer | ≥ 1 | 1 |
| unit           | Единица измерения | Да | string | 'шт', 'компл', 'экз' | 'шт' |
| status         | Статус ресурса | Нет | string | 'available', 'maintenance', 'retired' | 'available' |

**Уникальные комбинации параметров**
- `(name, category_id)` – в пределах одной категории не может быть двух ресурсов с одинаковым названием.

**Возвращаемые данные (при успешном создании)**

| Параметр (англ) | Тип |
|----------------|-----|
| id             | integer |
| name           | string |
| description    | string или null |
| category_id    | integer |
| total_quantity | integer |
| available_quantity | integer |
| unit           | string |
| status         | string |
| created_at     | string (ISO 8601) |
| updated_at     | string (ISO 8601) |

### 2. Изменение ресурса по ID

**Параметры запроса** (все поля, кроме `id`, необязательны)

| Параметр (англ) | Пояснение | Обязательность | Тип | Ограничение | Значение по умолчанию |
|----------------|-----------|----------------|-----|-------------|-----------------------|
| name           | Новое название | Нет | string | 1–100 символов | - |
| description    | Новое описание | Нет | string | до 500 символов | - |
| category_id    | Новая категория | Нет | integer | существующий id | - |
| total_quantity | Новое общее количество | Нет | integer | ≥ 1 | - |
| unit           | Новая единица измерения | Нет | string | 'шт', 'компл', 'экз' | - |
| status         | Новый статус | Нет | string | 'available', 'maintenance', 'retired' | - |

**Возвращаемые данные** – полный объект ресурса (те же поля, что при создании).

### 3. Удаление ресурса по ID

- **Возвращает**: `true`, если ресурс был удалён (физически удалена запись), иначе `false`.

### 4. Получение ресурса по ID

**Возвращаемые данные** (при успешном поиске)

| Параметр (англ) | Тип |
|----------------|-----|
| id             | integer |
| name           | string |
| description    | string или null |
| category_id    | integer |
| total_quantity | integer |
| available_quantity | integer |
| unit           | string |
| status         | string |
| created_at     | string |
| updated_at     | string |

### 5. Получение списка ресурсов по параметрам

**Параметры запроса**

| Параметр (англ) | Пояснение | Тип | Описание |
|----------------|-----------|-----|----------|
| category_id    | Фильтр по категории | integer | опционально |
| status         | Фильтр по статусу | string | 'available', 'maintenance', 'retired' |
| search         | Поиск по имени | string | частичное совпадение |
| limit          | Количество записей | integer | от 1 до 100, по умолчанию 20 |
| offset         | Смещение | integer | ≥ 0, по умолчанию 0 |

**Возвращаемые данные** – массив объектов ресурсов (каждый объект содержит поля, перечисленные в п.4).

---

## ER-диаграмма

```mermaid
erDiagram
    ResourceCategory {
        int id PK
        string name UK
        string description
    }
    
    Resource {
        int id PK
        string name
        string description
        int category_id FK
        int total_quantity
        int available_quantity
        string unit
        string status
        datetime created_at
        datetime updated_at
    }
    
    User {
        int id PK
        string username UK
        string email
    }
    
    ResourceReservation {
        int id PK
        int resource_id FK
        int reserved_by FK
        datetime start_time
        datetime end_time
        string purpose
        string status
    }
    
    ResourceCategory ||--o{ Resource : "содержит"
    Resource ||--o{ ResourceReservation : "бронируется"
    User ||--o{ ResourceReservation : "создаёт"