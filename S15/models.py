from peewee import *
import datetime

db = SqliteDatabase('load_assignment.db')

class BaseModel(Model):
    class Meta:
        database = db

class Teacher(BaseModel):
    external_id = CharField(unique=True, max_length=100, null=False)

class Discipline(BaseModel):
    external_id = CharField(unique=True, max_length=100, null=False)
    name = CharField(max_length=255, null=False)

class Group(BaseModel):
    external_id = CharField(unique=True, max_length=100, null=False)
    name = CharField(max_length=100, null=False)

class TeacherDiscipline(BaseModel):
    teacher = ForeignKeyField(Teacher, backref='disciplines_link', null=False, on_delete='CASCADE')
    discipline = ForeignKeyField(Discipline, backref='teachers_link', null=False, on_delete='CASCADE')

    class Meta:
        primary_key = CompositeKey('teacher', 'discipline')

class Assignment(BaseModel):
    teacher = ForeignKeyField(Teacher, backref='assignments', null=False, on_delete='CASCADE')
    discipline = ForeignKeyField(Discipline, backref='assignments', null=False, on_delete='CASCADE')
    group = ForeignKeyField(Group, backref='assignments', null=False, on_delete='CASCADE')
    semester = CharField(max_length=20, null=False)
    hours = IntegerField(null=False)

    class Meta:
        indexes = (
            (('teacher', 'discipline', 'group', 'semester'), True),
        )

def init_db():
    db.connect()
    db.execute_sql('PRAGMA foreign_keys = ON;')
    db.create_tables([Teacher, Discipline, Group, TeacherDiscipline, Assignment], safe=True)
    db.close()

if __name__ == '__main__':
    init_db()
    print("DB initialized for Load Assignment Service (Вариант 15)")
