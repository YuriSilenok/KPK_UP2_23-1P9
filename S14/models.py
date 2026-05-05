from peewee import SqliteDatabase, Model, IntegerField, CharField, FloatField

# ==================== БАЗА ДАННЫХ ====================
db = SqliteDatabase('workload.db')


class Workload(Model):
    """Модель нагрузки преподавателя"""
    teacher_id = IntegerField(null=False, verbose_name="ID преподавателя")
    discipline = CharField(max_length=200, null=False, verbose_name="Дисциплина")
    hours_per_week = FloatField(null=False, verbose_name="Часов в неделю")
    groups_count = IntegerField(null=False, verbose_name="Количество групп")
    semester = IntegerField(null=False, verbose_name="Семестр (1 или 2)")
    year = IntegerField(null=False, verbose_name="Учебный год")
    total_hours = FloatField(null=False, verbose_name="Общая нагрузка за семестр")
    notes = CharField(max_length=500, null=True, verbose_name="Примечания")

    class Meta:
        database = db
        table_name = 'workloads'


def init_db():
    """Функция инициализации базы данных"""
    db.connect()
    db.create_tables([Workload], safe=True)
    db.close()


# ==================== ТОЧКА ВХОДА ====================
if __name__ == "__main__":
    init_db()
    print("✅ База данных инициализирована")
    print("📊 Таблица Workload создана")