import datetime
from peewee import *

db = SqliteDatabase('employee_status.db')


class BaseModel(Model):
    class Meta:
        database = db

class Employee(BaseModel):
    full_name = CharField(max_length=255, null=False)
    birth_date = DateField(null=False)
    hire_date = DateField(null=False)
    email = CharField(unique=True, null=True)
    phone = CharField(max_length=20, null=True)
    address = TextField(null=True)
    status = CharField(max_length=20, default='active') 

class Position(BaseModel):
    title = CharField(max_length=100, null=False)
    description = TextField(null=True)

class EmployeePosition(BaseModel):
    employee = ForeignKeyField(Employee, backref='positions', on_delete='CASCADE', null=False)
    position = ForeignKeyField(Position, backref='employees', on_delete='CASCADE', null=False)
    start_date = DateField(null=False)
    end_date = DateField(null=True)
    load_factor = FloatField(null=False, constraints=[Check('load_factor > 0 AND load_factor <= 1')])

class Vacation(BaseModel):
    employee = ForeignKeyField(Employee, backref='vacations', on_delete='CASCADE', null=False)
    start_date = DateField(null=False)
    end_date = DateField(null=False)
    type = CharField(max_length=50, null=False)

class SickLeave(BaseModel):
    employee = ForeignKeyField(Employee, backref='sick_leaves', on_delete='CASCADE', null=False)
    start_date = DateField(null=False)
    end_date = DateField(null=False)
    diagnosis = TextField(null=True)

def initialize_db():
    """Создаёт таблицы, если они не существуют."""
    db.connect()
    db.create_tables([Employee, Position, EmployeePosition, Vacation, SickLeave], safe=True)
    db.close()

if __name__ == '__main__':
    initialize_db()
    print("База данных инициализирована. Таблицы созданы.")