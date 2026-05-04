# Документация сервиса движения студентов

# Сущность: MovementRecord (Запись о движении)

# 1. Информация для создания MovementRecord

| Parameter | Explanation | Required | Type | Constraint | Default |
|-----------|-------------|----------|------|------------|---------|
| student_id | ID студента | Yes | int | exists in Student, >0 | - |
| group_from_id | ID группы откуда | Yes | int | exists in Group, >0 | - |
| group_to_id | ID группы куда | Yes | int | exists in Group, >0 | - |
| movement_type_id | ID типа движения | Yes | int | exists in MovementType, >0 | - |
| movement_date | дата движения | Yes | date | YYYY-MM-DD, not future | - |
| order_number | номер приказа | Yes | str | 1-50 chars | - |
| reason | причина | Yes | str | 1-500 chars | - |

# 2. Уникальные комбинации параметров

- (student_id, movement_date, movement_type_id)

# 3. Информация возвращаемая при успешном создании

| Parameter | Type |
|-----------|------|
| id | int |
| student_id | int |
| group_from_id | int |
| group_to_id | int |
| movement_type_id | int |
| movement_date | date |
| order_number | str |
| reason | str |

# 4. Информация для изменения MovementRecord по ID

| Parameter | Explanation | Required | Type | Constraint | Default |
|-----------|-------------|----------|------|------------|---------|
| group_from_id | ID группы откуда | No | int | exists in Group, >0 | unchanged |
| group_to_id | ID группы куда | No | int | exists in Group, >0 | unchanged |
| movement_date | дата движения | No | date | YYYY-MM-DD, not future | unchanged |
| order_number | номер приказа | No | str | 1-50 chars | unchanged |
| reason | причина | No | str | 1-500 chars | unchanged |

# 5. Информация возвращаемая при успешном изменении

| Parameter | Type |
|-----------|------|
| id | int |
| student_id | int |
| group_from_id | int |
| group_to_id | int |
| movement_type_id | int |
| movement_date | date |
| order_number | str |
| reason | str |

# 6. Удаление MovementRecord по ID

Вернет True, если запись была удалена, иначе False

# 7. Получение MovementRecord по ID

| Parameter | Explanation | Type |
|-----------|-------------|------|
| id | ID записи | int |
| student_id | ID студента | int |
| group_from_id | ID группы откуда | int |
| group_to_id | ID группы куда | int |
| movement_type_id | ID типа движения | int |
| movement_date | дата движения | date |
| order_number | номер приказа | str |
| reason | причина | str |

# 8. Параметры для получения списка MovementRecord

| Parameter | Explanation | Type | Description |
|-----------|-------------|------|-------------|
| student_id | ID студента | int | фильтр по студенту |
| group_from_id | ID исходной группы | int | фильтр |
| group_to_id | ID целевой группы | int | фильтр |
| movement_type_id | ID типа движения | int | фильтр |
| movement_date_from | дата движения от | date | >= |
| movement_date_to | дата движения до | date | <= |
| limit | лимит записей | int | по умолчанию 100 |
| offset | смещение | int | по умолчанию 0 |

# 9. Информация возвращаемая при получении списка

| Parameter | Type |
|-----------|------|
| id | int |
| student_id | int |
| group_from_id | int |
| group_to_id | int |
| movement_type_id | int |
| movement_date | date |
| order_number | str |
| reason | str |

# Список функций

1. init_db() - создание таблиц и заполнение справочников
2. create_movement_record() - создание записи о движении
3. get_movement_by_id() - получение записи по ID
4. update_movement_record() - обновление записи
5. delete_movement_record() - удаление записи по ID
6. get_movements_list() - получение списка записей с фильтрацией

# Диаграмма классов

**Student**
- id: int
- full_name: str

**Group**
- id: int
- name: str
- course: int
- faculty: str

**MovementType**
- id: int
- name: str
- code: str

**MovementRecord**
- id: int
- student_id: int
- group_from_id: int
- group_to_id: int
- movement_type_id: int
- movement_date: date
- order_number: str
- reason: str

**Связи**
- Student 1 ----< MovementRecord
- Group 1 ----< MovementRecord
- MovementType 1 ----< MovementRecord

# ER-диаграмма

См. файл er_diagram.png