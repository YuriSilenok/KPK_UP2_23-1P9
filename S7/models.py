from peewee import *
import re

db = SqliteDatabase('data.db')

class BaseModel(Model):
    class Meta:
        database = db

class Groups(BaseModel):
    class Meta:
        db_table = "groups"
        indexes = (
            (('number', 'after_class_number', 'prefix'), True),
        )
    
    id = AutoField()
    year = IntegerField(null=False)
    is_active = BooleanField(default=True) 
    tutor_id = IntegerField(null=True, default=None)
    student_count = IntegerField(null=False, default=0)
    cipher_of_the_training_area = CharField(null=False, max_length=8)
    number = IntegerField(null=False)
    after_class_number = IntegerField(null=False)
    prefix = CharField(max_length=2, null=False)

    def validate(self):
        required_fields = {
            'year': self.year,
            'cipher_of_the_training_area': self.cipher_of_the_training_area,
            'number': self.number,
            'after_class_number': self.after_class_number,
            'prefix': self.prefix
        }
        
        for field_name, field_value in required_fields.items():
            if field_value is None:
                raise ValueError(f"Поле '{field_name}' обязательно для заполнения")

        if not isinstance(self.year, int):
            raise ValueError("Год должен быть целым числом")
        if not (2000 <= self.year <= 2999):
            raise ValueError("Год должен быть в диапазоне от 2000 до 2999")

        if self.tutor_id is not None: 
            if not isinstance(self.tutor_id, int):
                raise ValueError("ID преподавателя должно быть целым числом")
            if self.tutor_id <= 0:
                raise ValueError("ID преподавателя должно быть положительным числом")

        # Исправлено: убрана проверка на None, т.к. поле не может быть null
        if not isinstance(self.student_count, int):
            raise ValueError("Количество студентов должно быть целым числом")
        if not (0 <= self.student_count <= 30):
            raise ValueError("Количество студентов должно быть от 0 до 30")

        if not isinstance(self.cipher_of_the_training_area, str):
            raise ValueError("Шифр должен быть строкой")
        if not re.match(r'^\d{2}\.\d{2}\.\d{2}$', self.cipher_of_the_training_area):
            raise ValueError("Шифр должен быть в формате XX.XX.XX")

        if not isinstance(self.number, int):
            raise ValueError("Номер группы должен быть целым числом")
        if self.number < 1:
            raise ValueError("Номер группы должен быть от 1")

        if self.after_class_number not in [9, 11]:
            raise ValueError("После какого класса поступили должно быть 9 или 11")

        if not isinstance(self.prefix, str):
            raise ValueError("Префикс должен быть строкой")
        if not (1 <= len(self.prefix) <= 2):
            raise ValueError("Префикс должен содержать 1 или 2 символа")
        
        return True

    def soft_delete(self):
        self.is_active = False
        self.save()
        return True

def init_db():
    db.connect()
    db.create_tables([Groups])
    print("База данных инициализирована")

if __name__ == '__main__':
    init_db()