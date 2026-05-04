import datetime
from peewee import *

db = SqliteDatabase('student_movement.db')


class BaseModel(Model):
    class Meta:
        database = db


class Student(BaseModel):
    id = AutoField()
    full_name = CharField(max_length=200)

    class Meta:
        table_name = 'students'


class Group(BaseModel):
    id = AutoField()
    name = CharField(max_length=100, unique=True)
    course = IntegerField()
    faculty = CharField(max_length=100)

    class Meta:
        table_name = 'groups'


class MovementType(BaseModel):
    id = AutoField()
    name = CharField(max_length=50, unique=True)
    code = CharField(max_length=30, unique=True)

    class Meta:
        table_name = 'movement_types'


class MovementRecord(BaseModel):
    id = AutoField()
    student = ForeignKeyField(Student, backref='movements', on_delete='CASCADE')
    group_from = ForeignKeyField(Group, backref='movements_from', on_delete='RESTRICT')
    group_to = ForeignKeyField(Group, backref='movements_to', on_delete='RESTRICT')
    movement_type = ForeignKeyField(MovementType, backref='movements', on_delete='RESTRICT')
    movement_date = DateField()
    order_number = CharField(max_length=50)
    reason = TextField()

    class Meta:
        table_name = 'movement_records'
        indexes = (
            (('student', 'movement_date', 'movement_type'), True),
        )


def init_db():
    db.connect()
    db.create_tables([Student, Group, MovementType, MovementRecord], safe=True)
    
    if not Group.select().where(Group.name == 'Expelled').exists():
        Group.create(name='Expelled', course=0, faculty='-')
    
    if not Group.select().where(Group.name == 'AcademicLeave').exists():
        Group.create(name='AcademicLeave', course=0, faculty='-')
    
    if not MovementType.select().exists():
        MovementType.create(name='Transfer', code='transfer')
        MovementType.create(name='Expulsion', code='expelled')
        MovementType.create(name='Reinstatement', code='reinstated')
        MovementType.create(name='AcademicLeave', code='academic_leave')
        MovementType.create(name='ReturnFromLeave', code='academic_leave_end')
    
    db.close()


if __name__ == '__main__':
    init_db()
    print('Database initialized')