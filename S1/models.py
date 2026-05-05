from datetime import datetime
from peewee import (
    Model,
    CharField,
    BooleanField,
    DateTimeField,
    ForeignKeyField,
    AutoField,
    SqliteDatabase
)

DB = SqliteDatabase('auth.db')

class BaseModel(Model):
    """Базовая модель"""
    class Meta:
        database = DB


class User(BaseModel):
    """Класс пользователя"""
    id = AutoField()
    username = CharField(unique=True, null=False)
    email = CharField(unique=True, null=False)
    pass_hash = CharField(null=False)
    is_active = BooleanField(default=True, null=False)
    created_at = DateTimeField(default=datetime.now, null=False)


class Token(BaseModel):
    """Класс токена"""
    id = AutoField()
    user = ForeignKeyField(
        User,
        backref='tokens',
        on_delete='CASCADE',
        null=False
    )
    token = CharField(unique=True, null=False)
    expires_at = DateTimeField(null=False)
    created_at = DateTimeField(default=datetime.now, null=False)


def create_tables():
    """Создаёт таблицы"""
    with DB:
        DB.create_tables([User, Token])


if __name__ == "__main__":
    create_tables()