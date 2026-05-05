from peewee import SqliteDatabase, Model, CharField, IntegerField, ForeignKeyField
from pydantic import BaseModel, Field
from typing import Optional

db = SqliteDatabase('disciplines.db')

# Таблица категорий (например: Естественно-научные, Общепрофессиональные)
class Category(Model):
    name = CharField(unique=True, max_length=100)

    class Meta:
        database = db

# Таблица дисциплин с обязательным внешним ключом
class Discipline(Model):
    name = CharField(unique=True, max_length=100)
    code = CharField(unique=True, max_length=20)
    total_hours = IntegerField()
    # null=False гарантирует выполнение требования из задания
    category = ForeignKeyField(Category, backref='disciplines', null=False)

    class Meta:
        database = db

# --- Схемы Pydantic для FastAPI ---

class CategoryCreate(BaseModel):
    name: str

class DisciplineCreate(BaseModel):
    name: str = Field(..., max_length=100)
    code: str = Field(..., max_length=20)
    total_hours: int = Field(..., gt=0)
    category_id: int

def init_db():
    db.connect()
    # Создаем две таблицы
    db.create_tables([Category, Discipline], safe=True)
    
    # Можно сразу создать тестовую категорию, так как FK не может быть NULL
    if Category.select().count() == 0:
        Category.create(name="Общий цикл")
        
    db.close()

if __name__ == "__main__":
    init_db()
    print("Реляционная БД с двумя таблицами инициализирована.")
