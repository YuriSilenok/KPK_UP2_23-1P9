from peewee import *

db = SqliteDatabase("sqlite3.db")

class Base(Model):
    """Базовый класс"""
    id = AutoField(primary_key=True)

    class Meta:
        database = db

class User(Base):
    """Модель таблицы User"""
    username = CharField(unique=True, null=Flase)
    password = CharField(null=False)
    is_active = BooleanField(default=True)
    created_at = DateField()

class UserData(Base):
    """Модель таблицы UserData"""
    first_name = CharField(null=True)
    last_name = CharField(null=True)
    middle_name = CharField(null=True)
    user_id = ForeignKeyField(User, backref="profile", unique=True, null=False, on_delete="CASCADE")
    email = CharField(unique=True, null=False)
    phone_number = CharField(null=True, unique=True)
    avatar = CharField(null=True)
    notification = BooleanField(default=True)
    is_active = BooleanField(default=True)

def init_db():
    """Подключение БД и создание таблиц"""
    tables = [User, UserData]
    db.connect()
    db.create_tables(tables) 
    db.close()


if __name__ == '__main__':
    init_db()
