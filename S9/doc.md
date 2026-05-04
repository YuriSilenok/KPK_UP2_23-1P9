Документация сервиса движения студентов

Список функций

1. init_db() - создание таблиц и заполнение справочников
2. create_movement_record() - создание записи о движении
3. get_movement_by_id() - получение записи по ID
4. update_movement_record() - обновление записи
5. delete_movement_record() - удаление записи по ID
6. get_movements_list() - получение списка записей с фильтрацией

Диаграмма классов

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
- Student 1 < MovementRecord
- Group 1 < MovementRecord
- MovementType 1 < MovementRecord