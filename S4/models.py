from peewee import SqliteDatabase, Model, CharField, IntegerField, BooleanField, ForeignKeyField

db = SqliteDatabase('permissions.db')


class Permission(Model):
    name = CharField(max_length=100, unique=True, null=False)
    description = CharField(max_length=255, null=True)
    is_active = BooleanField(null=False, default=True)

    class Meta:
        database = db
        table_name = 'permissions'


class RolePermission(Model):
    role_id = IntegerField(null=False)
    permission_id = ForeignKeyField(Permission, backref='role_permissions', null=False)

    class Meta:
        database = db
        table_name = 'role_permissions'
        indexes = (
            (('role_id', 'permission_id'), True),
        )


def init_db():
    db.connect()
    db.create_tables([Permission, RolePermission], safe=True)


if __name__ == "__main__":
    init_db()
    print("База данных permissions.db успешно создана")