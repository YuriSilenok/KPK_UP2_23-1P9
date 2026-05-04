from peewee import *

db = SqliteDatabase("sqlite3.db")

class Base(Model):
    """Базовый класс"""
    id = AutoField(primary_key=True)

    class Meta:
        database = db

class User(Base):
    """Модель таблицы User"""
    email = CharField(unique=True, null=False)
    password = CharField(null=False)
    is_active = BooleanField(default=True)
    created_at = DateField()

class UserData(Base):
    """Модель таблицы UserData"""
    user_id = ForeignKeyField(User, backref="profile", unique=True)
    phone_number = CharField(null=True)
    avatar = BlobField(null=True)
    notification = BooleanField(default=True)

def init_db():
    """Подключение БД и создание таблиц"""
    tables = [User, UserData]
    db.connect()
    db.create_tables(tables) 
    db.close()


if __name__ == '__main__':
    init_db()
