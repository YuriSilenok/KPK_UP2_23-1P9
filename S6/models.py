from peewee import (
    SqliteDatabase,
    Model,
    AutoField,
    CharField,
    IntegerField,
    TextField,
    ForeignKeyField,
)

db = SqliteDatabase("specialty_service.db")


class BaseModel(Model):
    class Meta:
        database = db


class FGOS(BaseModel):
    """Федеральный государственный образовательный стандарт."""

    id = AutoField()
    number = CharField(max_length=50, unique=True)
    name = CharField(max_length=255)
    approval_year = IntegerField()

    class Meta:
        table_name = "fgos"


class Specialty(BaseModel):
    """Специальность СПО."""

    id = AutoField()
    code = CharField(max_length=20, unique=True)
    name = CharField(max_length=255)
    description = TextField(default="")
    fgos = ForeignKeyField(FGOS, backref="specialties", on_delete="RESTRICT")

    class Meta:
        table_name = "specialty"


def init_db():
    """Создаёт таблицы в базе данных, если они ещё не существуют."""
    with db:
        db.create_tables([FGOS, Specialty])


if __name__ == "__main__":
    init_db()
    print("База данных инициализирована.")
