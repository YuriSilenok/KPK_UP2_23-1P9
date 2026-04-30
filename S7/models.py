from peewee import *

db = SqliteDatabase('data.db')

class Basemodel(Model):
    class Meta:
        database = db

class Groups(Basemodel):
    class Meta:
        db_table = "Group"

    id_group = AutoField()
    year = IntegerField()
    is_active = BooleanField()
    ruk_id = IntegerField()
    stud_count = IntegerField()
    code_np = CharField(max_length=20)
    number = IntegerField()
    after_class_number = IntegerField()
    prefix = CharField(max_length=2)

class Students(Basemodel):
    class Meta:
        db_table = 'Students'
    
    id_stud = AutoField()
    id_group = ForeignKeyField(Groups, backref='students', on_delete='CASCADE')

def init_db():
    db.connect()
    db.create_tables([Groups, Students])
    print("База данных инициализирована")

if __name__ == '__main__':
    init_db()