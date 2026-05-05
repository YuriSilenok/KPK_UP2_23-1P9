from peewee import *

db = SqliteDatabase('student_movement.db')


class Basemodel(Model):
    class Meta:
        database = db


class MovementType(Basemodel):
    class Meta:
        db_table = "movement_types"

    name = CharField(max_length=50, unique=True)
    code = CharField(max_length=30, unique=True)


class MovementRecord(Basemodel):
    class Meta:
        db_table = "movement_records"

    student_id = IntegerField()
    group_from_id = IntegerField()
    group_to_id = IntegerField()
    movement_type = ForeignKeyField(MovementType, backref='records', on_delete='RESTRICT')
    movement_date = DateField()
    order_number = CharField(max_length=20)
    reason = CharField(max_length=200)


def init_db():
    db.connect()
    db.create_tables([MovementType, MovementRecord])
    
    if not MovementType.select().exists():
        MovementType.create(name='Transfer', code='transfer')
        MovementType.create(name='Expulsion', code='expelled')
        MovementType.create(name='Reinstatement', code='reinstated')
        MovementType.create(name='AcademicLeave', code='academic_leave')
        MovementType.create(name='ReturnFromLeave', code='academic_leave_end')
    
    print("База данных инициализирована")


if __name__ == '__main__':
    init_db()