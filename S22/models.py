from peewee import *

db = SqliteDatabase('S22.db')


class BaseModel(Model):
    class Meta:
        database = db


class Weekday(BaseModel):
    name = CharField(
        max_length=20, 
        unique=True, 
        constraints=[Check("name GLOB '[А-Яа-я]*'")],
    )
    order_number = IntegerField(
        unique=True, 
        constraints=[Check('order_number BETWEEN 1 AND 7')]
    )

    class Meta:
        table_name = 'weekday'


class Timeslot(BaseModel):
    pair_number = IntegerField(
        constraints=[Check('pair_number BETWEEN 1 AND 7')],
    )
    start_time = TimeField()
    end_time = TimeField()
    duration_min = IntegerField()

    class Meta:
        table_name = 'timeslot'


class WeekdayTimeslot(BaseModel):
    weekday = ForeignKeyField(
        Weekday, 
        backref='weekday_timeslots', 
        on_delete='CASCADE',
        on_update="CASCADE"
    )
    timeslot = ForeignKeyField(
        Timeslot, 
        backref='weekday_timeslots', 
        on_delete='CASCADE',
        on_update="CASCADE"
    )
    is_shortened = BooleanField(
        default=False
    )
    is_holiday = BooleanField(
        default=False
    )

    class Meta:
        table_name = 'weekday_timeslot'


def create_tables():
    db.create_tables([Weekday, Timeslot, WeekdayTimeslot])


if __name__ == '__main__':
    create_tables()
