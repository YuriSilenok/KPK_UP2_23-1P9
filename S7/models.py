from peewee import *

db = SqliteDatabase('data.db')

class Basemodel(Model):
    class Meta:
        database = db

class Groups(Basemodel):
    class Meta:
        db_table = "Group"

    year = IntegerField()
    is_active = BooleanField()
    tutor_id = IntegerField()
    student_count = IntegerField()
    cipher_of_the_training_area = CharField(max_length=8)
    number = IntegerField()
    after_class_number = IntegerField()
    prefix = CharField(max_length=2)

class Students(Basemodel):
    class Meta:
        db_table = 'Students'
    
    student_id = IntegerField()
    group_id = ForeignKeyField(Groups, backref='students', on_delete='CASCADE')

def init_db():
    db.connect()
    db.create_tables([Groups, Students])
    print("База данных инициализирована")

if __name__ == '__main__':
    init_db()