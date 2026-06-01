from peewee import *
import re
db = SqliteDatabase('data.db')

class BaseModel(Model):
    class Meta:
        database = db

class Groups(BaseModel):
    class Meta:
        db_table = "groups"
    
    id = AutoField()
    year = IntegerField(null=False)
    is_active = BooleanField(default=True) 
    tutor_id = IntegerField(null=True, default=None)
    student_count = IntegerField(default=0)
    cipher_of_the_training_area = CharField(null=False, max_length=8)
    number = IntegerField(null=False)
    after_class_number = IntegerField(null=False)
    prefix = CharField(null=False)

    def validate(self):

        if self.year is not None and not (2000 <= self.year <= 2999):
            raise ValueError("Год должен быть в диапазоне от 2000 до 2999")

        if self.tutor_id is not None and self.tutor_id <= 0:
            raise ValueError("ID преподавателя должно быть положительным числом или None")

        if self.student_count is not None and not (0 <= self.student_count <= 30):
            raise ValueError("Количество студентов должно быть от 0 до 30")

        if self.cipher_of_the_training_area:
            if not re.match(r'^\d{2}\.\d{2}\.\d{2}$', self.cipher_of_the_training_area):
                raise ValueError("Шифр должен быть в формате XX.XX.XX")

        if self.number is not None and not (1 <= self.number <= 9999):
            raise ValueError("Номер группы должен быть от 1 до 9999")

        if self.after_class_number is not None and self.after_class_number not in [9, 11]:
            raise ValueError("Количество классов после обучения должно быть 9 или 11")

        if self.prefix and not (1 <= len(self.prefix) <= 2):
            raise ValueError("Префикс должен содержать 1 или 2 символа")

def init_db():
    db.connect()
    db.create_tables([Groups])
    print("База данных инициализирована")

if __name__ == '__main__':
    init_db()