from peewee import SqliteDatabase, Model, CharField, ForeignKeyField

database = SqliteDatabase("roles.db")

class BaseModel(Model):
    class Meta:
        database = database

class Role(BaseModel):
    name = CharField(max_length=255, unique=True)
    description = CharField(max_length=255, null=True)

class Access(BaseModel):
    object = CharField(max_length=100)
    action = CharField(max_length=50)

    class Meta:
        indexes = (
            (('object', 'action'), True),
        )

class Permission(BaseModel):
    role = ForeignKeyField(Role, backref='permissions', on_delete='CASCADE')
    permission = ForeignKeyField(Access, backref='roles', on_delete='CASCADE')

    class Meta:
        indexes = (
            (('role', 'permission'), True),
        )

def init_db():
    database.connect()
    database.create_tables([Role, Access, Permission], safe=True)
    for name in ["Admin", "Director", "HeadTeacher", "Teacher", "Student", "Parent"]:
        Role.get_or_create(name=name, defaults={"description": f"Role {name}"})
    database.close()

if __name__ == "__main__":
    init_db()
