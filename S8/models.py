
## Файл `models.py` (модели БД + инициализация)
"""
Модуль моделей для Subgroup Service (Вариант 8)
Использует peewee ORM + SQLite3
"""

from peewee import *
from datetime import date

# Инициализация базы данных
db = SqliteDatabase('subgroup_service.db')

class BaseModel(Model):
    """Базовый класс для всех моделей"""
    class Meta:
        database = db

class Group(BaseModel):
    """Модель группы (смежный справочник, внешний ключ)"""
    id = AutoField(primary_key=True)
    name = CharField(max_length=50, unique=True, null=False)
    formation_year = IntegerField(null=False)
    status = CharField(max_length=20, null=False, default='active')
    
    class Meta:
        table_name = 'groups'

class Student(BaseModel):
    """Модель студента (смежный справочник, внешний ключ)"""
    id = AutoField(primary_key=True)
    first_name = CharField(max_length=50, null=False)
    last_name = CharField(max_length=50, null=False)
    email = CharField(max_length=100, unique=True, null=False)
    
    class Meta:
        table_name = 'students'

class Subgroup(BaseModel):
    """
    Модель подгруппы
    Не содержит NULL-внешних ключей
    """
    id = AutoField(primary_key=True)
    group_id = ForeignKeyField(Group, backref='subgroups', 
                                on_delete='CASCADE', null=False)
    name = CharField(max_length=100, null=False)
    type = CharField(max_length=20, null=False)
    max_students = IntegerField(null=False, default=30)
    created_at = DateField(null=False, default=date.today)
    
    # Ограничения
    class Meta:
        table_name = 'subgroups'
        constraints = [
            Check('type IN ("лекционная", "практическая", "лабораторная")'),
            Check('max_students BETWEEN 1 AND 500')
        ]

class SubgroupStudent(BaseModel):
    """
    Транзитивная таблица для связи многие-ко-многим
    Между подгруппами и студентами
    """
    id = AutoField(primary_key=True)
    subgroup_id = ForeignKeyField(Subgroup, backref='members',
                                   on_delete='CASCADE', null=False)
    student_id = ForeignKeyField(Student, backref='subgroups',
                                  on_delete='CASCADE', null=False)
    joined_at = DateField(null=False, default=date.today)
    
    class Meta:
        table_name = 'subgroup_students'
        # Уникальность: студент не может быть дважды в одной подгруппе
        indexes = (
            (('subgroup_id', 'student_id'), True),
        )

def init_db():
    """
    Функция инициализации БД.
    Создаёт все таблицы, если они ещё не созданы.
    """
    db.connect()
    # Создаём таблицы (если их нет)
    db.create_tables([Group, Student, Subgroup, SubgroupStudent])
    
    # Заполнение тестовыми данными (только если таблицы пустые)
    if Group.select().count() == 0:
        # Добавляем тестовую группу
        test_group = Group.create(
            name='П-41', 
            formation_year=2024, 
            status='active'
        )
        
        # Добавляем тестовых студентов
        students = []
        for i in range(1, 6):
            s = Student.create(
                first_name=f'Студент{i}',
                last_name='Тестов',
                email=f'test{i}@example.com'
            )
            students.append(s)
        
        # Добавляем тестовую подгруппу
        sub = Subgroup.create(
            group_id=test_group,
            name='Подгруппа А',
            type='практическая',
            max_students=10
        )
        
        # Связываем студентов с подгруппой
        for student in students:
            SubgroupStudent.create(subgroup_id=sub, student_id=student)
    
    db.close()
    print("База данных инициализирована (таблицы созданы)")

# Точка входа для вызова инициализации
if __name__ == '__main__':
    init_db()