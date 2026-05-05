import os
from datetime import datetime
from peewee import (
    SqliteDatabase, Model, AutoField, CharField, TextField, IntegerField,
    ForeignKeyField, DateTimeField, Check, fn
)

# Инициализация БД
db = SqliteDatabase('resource_pool.db')


class BaseModel(Model):
    class Meta:
        database = db


class ResourceCategory(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField(max_length=100, unique=True, constraints=[Check("length(name) >= 1")])
    description = TextField(null=True)

    class Meta:
        table_name = 'resource_categories'


class User(BaseModel):
    """Внешняя сущность для связи бронирований (заглушка)"""
    id = AutoField(primary_key=True)
    username = CharField(max_length=50, unique=True)
    email = CharField(max_length=100, unique=True)

    class Meta:
        table_name = 'users'


class Resource(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField(max_length=100, constraints=[Check("length(name) >= 1")])
    description = TextField(null=True)
    category = ForeignKeyField(ResourceCategory, backref='resources', on_delete='RESTRICT')
    total_quantity = IntegerField(constraints=[Check('total_quantity >= 1')], default=1)
    unit = CharField(max_length=10, choices=['шт', 'компл', 'экз'], default='шт')
    status = CharField(max_length=20, choices=['available', 'maintenance', 'retired'], default='available')
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'resources'
        indexes = (
            (('name', 'category'), True),  # уникальная комбинация name + category_id
        )

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)

    @property
    def available_quantity(self):
        """Вычисляемое поле: общее количество минус забронированные активные"""
        active_reservations = (ResourceReservation
                               .select(fn.SUM(ResourceReservation.quantity))
                               .where(
                                   (ResourceReservation.resource == self) &
                                   (ResourceReservation.status == 'active') &
                                   (ResourceReservation.end_time > datetime.now())
                               )
                               .scalar() or 0)
        return self.total_quantity - active_reservations


class ResourceReservation(BaseModel):
    """Транзитивная таблица для связи Resource и User (многие ко многим)"""
    id = AutoField(primary_key=True)
    resource = ForeignKeyField(Resource, backref='reservations', on_delete='CASCADE')
    reserved_by = ForeignKeyField(User, backref='reservations', on_delete='CASCADE')
    quantity = IntegerField(constraints=[Check('quantity >= 1')], default=1)
    start_time = DateTimeField()
    end_time = DateTimeField()
    purpose = TextField(null=True)
    status = CharField(max_length=20, choices=['active', 'completed', 'cancelled'], default='active')
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'resource_reservations'


def init_db():
    """Создание таблиц и заполнение тестовыми данными"""
    db.connect()
    db.create_tables([ResourceCategory, Resource, User, ResourceReservation], safe=True)

    # Добавим категорию по умолчанию, если таблица пуста
    if not ResourceCategory.select().exists():
        ResourceCategory.create(name='Спортивный инвентарь', description='Мячи, маты и т.д.')
        ResourceCategory.create(name='Библиотечный фонд', description='Книги, учебники')
        ResourceCategory.create(name='Лабораторное оборудование', description='Приборы и инструменты')

    if not User.select().exists():
        User.create(username='teacher1', email='teacher1@example.com')
        User.create(username='student1', email='student1@example.com')

    if not Resource.select().exists():
        category = ResourceCategory.get(name='Спортивный инвентарь')
        Resource.create(
            name='Баскетбольный мяч',
            description='Wilson Evolution',
            category=category,
            total_quantity=10,
            unit='шт'
        )
        Resource.create(
            name='Гимнастический мат',
            category=category,
            total_quantity=5,
            unit='шт',
            status='maintenance'
        )


if __name__ == '__main__':
    init_db()
    print("База данных resource_pool.db успешно инициализирована.")