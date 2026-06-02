from peewee import *
import re
from playhouse.shortcuts import model_to_dict
from playhouse.signals import pre_save

db = SqliteDatabase('data.db')

class BaseModel(Model):
    class Meta:
        database = db

class Groups(BaseModel):
    class Meta:
        db_table = "groups"
        indexes = (
            (('number', 'after_class_number', 'prefix'), False), 
        )
    
    id = AutoField()
    year = IntegerField(null=False)
    is_active = BooleanField(default=True) 
    tutor_id = IntegerField(null=True, default=None)
    student_count = IntegerField(null=True, default=0) 
    cipher_of_the_training_area = CharField(null=False, max_length=8)  
    number = IntegerField(null=False)
    after_class_number = IntegerField(null=False)
    prefix = CharField(max_length=2, null=False)

    def validate(self):
        """Валидация с учётом дефолтных значений"""
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

        if self.student_count is None:
            self.student_count = 0 
        elif not isinstance(self.student_count, int):
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

    def save(self, *args, **kwargs):
        """Переопределяем save для автоматической валидации и проверки уникальности активных групп"""
        self.validate()

        if not self.id: 
            existing = (Groups
                       .select()
                       .where(
                           (Groups.number == self.number) &
                           (Groups.after_class_number == self.after_class_number) &
                           (Groups.prefix == self.prefix) &
                           (Groups.is_active == True)  
                       )
                       .first())
            if existing:
                raise ValueError(
                    f"Активная группа с номером {self.number}, "
                    f"после {self.after_class_number} класса "
                    f"и префиксом '{self.prefix}' уже существует"
                )
        
        try:
            return super().save(*args, **kwargs)
        except IntegrityError as e:
            raise ValueError(f"Ошибка целостности данных: {str(e)}") from e

    def soft_delete(self):
        """Мягкое удаление с проверкой успешности операции и возвратом количества обновленных строк"""
        try:
            if not self.is_active:
                return 0  
                
            self.is_active = False
            rows_updated = self.save()
            
            if rows_updated == 0:
                raise RuntimeError("Не удалось сохранить изменения при мягком удалении")
            return rows_updated
        except Exception as e:
            raise RuntimeError(f"Ошибка при мягком удалении: {e}")

    def hard_delete(self):
        """Полное удаление группы из БД"""
        try:
            rows_deleted = self.delete_instance()
            if rows_deleted == 0:
                raise RuntimeError("Не удалось удалить группу")
            return rows_deleted
        except Exception as e:
            raise RuntimeError(f"Ошибка при удалении группы: {e}")

    @classmethod
    def create_validated(cls, **kwargs):
        """Фабричный метод для создания и валидации группы"""
        group = cls(**kwargs)
        group.validate()
        return group

    def update_student_count(self, new_count):
        """Безопасное обновление количества студентов с валидацией"""
        if not isinstance(new_count, int):
            raise ValueError("Количество студентов должно быть целым числом")
        if not (0 <= new_count <= 30):
            raise ValueError("Количество студентов должно быть от 0 до 30")
        
        self.student_count = new_count
        rows_updated = self.save()
        return rows_updated > 0

    def reactivate(self):
        """Реактивация группы с проверкой уникальности"""
        if self.is_active:
            return False  

        existing = (Groups
                   .select()
                   .where(
                       (Groups.number == self.number) &
                       (Groups.after_class_number == self.after_class_number) &
                       (Groups.prefix == self.prefix) &
                       (Groups.is_active == True) &
                       (Groups.id != self.id) 
                   )
                   .first())
        
        if existing:
            raise ValueError(
                f"Невозможно реактивировать группу: уже существует активная группа "
                f"с номером {self.number}, после {self.after_class_number} класса "
                f"и префиксом '{self.prefix}'"
            )
        
        self.is_active = True
        rows_updated = self.save()
        return rows_updated > 0

    def to_dict(self):
        """Преобразование модели в словарь"""
        return model_to_dict(self)

@pre_save(sender=Groups)
def validate_cipher_on_save(model_class, instance, created):
    """
    Дополнительная проверка формата шифра на уровне БД через сигналы
    Срабатывает перед сохранением любой группы
    """
    if not re.match(r'^\d{2}\.\d{2}\.\d{2}$', instance.cipher_of_the_training_area):
        raise ValueError("Неверный формат шифра. Ожидается формат XX.XX.XX")

def init_db():
    """Инициализация базы данных с проверкой существования"""
    try:
        db.connect()
        db.create_tables([Groups], safe=True)
        print("База данных успешно инициализирована")
    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {e}")
        raise
    finally:
        if not db.is_closed():
            db.close()

if __name__ == '__main__':
    init_db()