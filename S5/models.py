from contextlib import asynccontextmanager
from peewee import SqliteDatabase, Model, CharField, IntegerField, BooleanField, DateTimeField
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

db = SqliteDatabase('faculty_service.db')


class Department(Model):
    name = CharField(max_length=200, unique=True, null=False)
    code = CharField(max_length=20, unique=True, null=False)
    head_name = CharField(max_length=150, null=False)
    head_specialty = CharField(max_length=200, null=True)
    head_phone = CharField(max_length=20, null=True)
    head_email = CharField(max_length=100, null=True)
    head_cabinet_id = IntegerField(null=True)
    reception_is_active = BooleanField(default=False)
    reception_schedule = CharField(max_length=500, null=True)
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = db
        table_name = 'departments'


def init_db():
    db.connect()
    db.create_tables([Department], safe=True)
    db.close()


class DepartmentCreate(BaseModel):
    name: str
    code: str
    head_name: str
    head_specialty: Optional[str] = None
    head_phone: Optional[str] = None
    head_email: Optional[str] = None
    head_cabinet_id: Optional[int] = None
    reception_is_active: bool = False
    reception_schedule: Optional[str] = None


class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    head_name: Optional[str] = None
    head_specialty: Optional[str] = None
    head_phone: Optional[str] = None
    head_email: Optional[str] = None
    head_cabinet_id: Optional[int] = None
    reception_is_active: Optional[bool] = None
    reception_schedule: Optional[str] = None


class DepartmentOut(BaseModel):
    id: int
    name: str
    code: str
    head_name: str
    head_specialty: Optional[str] = None
    head_phone: Optional[str] = None
    head_email: Optional[str] = None
    head_cabinet_id: Optional[int] = None
    reception_is_active: bool
    reception_schedule: Optional[str] = None
    created_at: datetime


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Запуск сервера Faculty Service...")
    init_db()
    print("База данных инициализирована")
    yield
    print("Остановка сервера...")
    if not db.is_closed():
        db.close()
    print("Ресурсы освобождены")


app = FastAPI(
    title="Faculty Service",
    description="Сервис управления отделениями СПО",
    version="1.0",
    lifespan=lifespan
)


@app.post("/departments", response_model=DepartmentOut, status_code=201)
def create_department(dept: DepartmentCreate):
    db.connect()
    new_dept = Department.create(
        name=dept.name,
        code=dept.code,
        head_name=dept.head_name,
        head_specialty=dept.head_specialty,
        head_phone=dept.head_phone,
        head_email=dept.head_email,
        head_cabinet_id=dept.head_cabinet_id,
        reception_is_active=dept.reception_is_active,
        reception_schedule=dept.reception_schedule
    )
    db.close()
    return new_dept


@app.get("/departments/{dept_id}", response_model=DepartmentOut)
def get_department(dept_id: int):
    db.connect()
    try:
        dept = Department.get_by_id(dept_id)
        return dept
    except Department.DoesNotExist:
        raise HTTPException(404, "Отделение не найдено")
    finally:
        db.close()


@app.get("/departments", response_model=List[DepartmentOut])
def list_departments(name: Optional[str] = None, limit: int = 100):
    db.connect()
    query = Department.select()
    if name:
        query = query.where(Department.name.contains(name))
    result = list(query.limit(limit))
    db.close()
    return result


@app.put("/departments/{dept_id}", response_model=DepartmentOut)
def update_department(dept_id: int, dept: DepartmentUpdate):
    db.connect()
    update_data = dept.dict(exclude_unset=True)
    if update_data:
        Department.update(update_data).where(Department.id == dept_id).execute()
    updated = Department.get_by_id(dept_id)
    db.close()
    return updated


@app.delete("/departments/{dept_id}")
def delete_department(dept_id: int):
    db.connect()
    deleted = Department.delete().where(Department.id == dept_id).execute()
    db.close()
    return {"deleted": bool(deleted)}


@app.get("/")
def root():
    return {
        "service": "Faculty Service",
        "version": "1.0",
        "endpoints": {
            "POST /departments": "Создать отделение",
            "GET /departments": "Список отделений",
            "GET /departments/{id}": "Получить по ID",
            "PUT /departments/{id}": "Обновить",
            "DELETE /departments/{id}": "Удалить"
        }
    }


if __name__ == "__main__":
    import uvicorn
    print("=" * 50)
    print("Запуск сервера Faculty Service...")
    print("Документация API: http://localhost:8000/docs")
    print("=" * 50)
    uvicorn.run(app, host="127.0.0.1", port=8000)