from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, field_validator,ConfigDict 
from typing import Optional, List
from models import Groups, db
from peewee import *
from pydantic import Field as PydanticField 
from contextlib import asynccontextmanager
import re
"""Модели"""

def createTables():
    """Создание таблиц в базе данных"""
    db.connect()
    db.create_tables([Groups], safe=True)
    db.close()

class NewGroup(BaseModel):
    year: int = PydanticField(..., ge=2000, le=2999)
    tutor_id: Optional[int] = PydanticField(None, ge=0) 
    student_count: Optional[int] = PydanticField(0, ge=0)
    cipher_of_the_training_area: str = PydanticField(..., min_length=1, max_length=20)
    number: int
    after_class_number: int
    prefix: str = PydanticField(..., min_length=1, max_length=2)
    """Валидаторы"""    
    @field_validator('year')
    @classmethod
    def validate_year(cls, v: int) -> int:
        if not (2000 <= v <= 2999):
            raise ValueError("Год должен быть в диапазоне от 2000 до 2999")
        return v
    
    @field_validator('tutor_id')
    @classmethod
    def validate_tutor_id(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and v <= 0:
            raise ValueError("ID преподавателя должно быть положительным числом или None")
        return v
    
    @field_validator('student_count')
    @classmethod
    def validate_student_count(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and not (0 <= v <= 30):
            raise ValueError("Количество студентов должно быть от 0 до 30")
        return v
    
    @field_validator('cipher_of_the_training_area')
    @classmethod
    def validate_cipher(cls, v: str) -> str:
        if not re.match(r'^\d{2}\.\d{2}\.\d{2}$', v):
            raise ValueError("Шифр должен быть в формате XX.XX.XX")
        return v
    
    @field_validator('number')
    @classmethod
    def validate_number(cls, v: int) -> int:
        if not (1 <= v <= 9999):
            raise ValueError("Номер группы должен быть от 1 до 9999")
        return v
    
    @field_validator('after_class_number')
    @classmethod
    def validate_after_class_number(cls, v: int) -> int:
        if v not in [9, 11]:
            raise ValueError("Количество классов после обучения должно быть 9 или 11")
        return v
    
    @field_validator('prefix')
    @classmethod
    def validate_prefix(cls, v: str) -> str:
        if not (1 <= len(v) <= 2):
            raise ValueError("Префикс должен содержать 1 или 2 символа")
        return v.upper() 

class GroupUpdate(BaseModel):
    tutor_id: Optional[int] = PydanticField(None, ge=0)
    student_count: Optional[int] = PydanticField(None, ge=0)
    
class GroupResponse(BaseModel):
    id: int
    year: int
    is_active: bool
    tutor_id: int
    student_count: int
    cipher_of_the_training_area: str
    number: int
    after_class_number: int
    prefix: str

    model_config = ConfigDict(from_attributes=True)
"""Управление соединением с БД и инициализация таблиц"""

@asynccontextmanager
async def lifespan(app: FastAPI):
    createTables()
    if db.is_closed():
        db.connect()
    yield
    if not db.is_closed():
        db.close()


app = FastAPI(
    title="Сервис групп",
    description="API для управления группами (вариант №7)",
    version="1.0.0",
    lifespan=lifespan
)

"""end-point"""

@app.post("/groups", response_model=GroupResponse, status_code=201)
def add_group(group_data: NewGroup):
    result = Groups.get_or_none(
        (Groups.number == group_data.number)&
        (Groups.after_class_number == group_data.after_class_number)&
        (Groups.prefix == group_data.prefix)
    )

    if result:
        raise HTTPException(
            status_code=409,
            detail="Такая группа уже существует"
        )

    group = Groups(
        year = group_data.year,
        is_active = True,
        tutor_id = group_data.tutor_id,
        student_count = group_data.student_count,
        cipher_of_the_training_area = group_data.cipher_of_the_training_area,
        number = group_data.number,
        after_class_number = group_data.after_class_number,
        prefix = group_data.prefix
    )

    group.save()

    return GroupResponse(
        id = group.id,
        year = group.year,
        is_active = group.is_active,
        tutor_id = group.tutor_id,
        student_count = group.student_count,
        cipher_of_the_training_area = group.cipher_of_the_training_area,
        number = group.number,
        after_class_number = group.after_class_number,
        prefix = group.prefix,
    )

@app.put("/groups/{group_replace_for_id}", response_model=GroupResponse)
def update(group_id: int, update_data:GroupUpdate):
    group = Groups.get_or_none(Groups.id == group_id)
    if group is None:
        raise HTTPException(status_code=404, detail="Группа не найдена")

    if update_data.tutor_id is not None:
        group.tutor_id = update_data.tutor_id

    if update_data.student_count is not None:
        group.student_count = update_data.student_count

    group.save()

    return GroupResponse(
        id = group.id,
        year = group.year,
        is_active = group.is_active,
        tutor_id = group.tutor_id,
        student_count = group.student_count,
        cipher_of_the_training_area = group.cipher_of_the_training_area,
        number = group.number,
        after_class_number = group.after_class_number,
        prefix = group.prefix,
    )

@app.delete("/groups/{group_id}", status_code=204)
def delete_group(group_id: int):
    group = Groups.get_or_none(Groups.id == group_id)
    if group is None:
        raise HTTPException(status_code=404, detail="Группа не найдена")
    
    if not group.is_active:
        raise HTTPException(status_code=409, detail="Группа уже неактивна")
    
    group.is_active = False
    group.save()
    return  

@app.get("/groups/{group_id}", response_model=GroupResponse)
def get_group(group_id: int):
    group = Groups.get_or_none(Groups.id == group_id)
    
    if group:
        return GroupResponse(
        id = group.id,
        year = group.year,
        is_active = group.is_active,
        tutor_id = group.tutor_id,
        student_count = group.student_count,
        cipher_of_the_training_area = group.cipher_of_the_training_area,
        number = group.number,
        after_class_number = group.after_class_number,
        prefix = group.prefix,
        )
    raise HTTPException(status_code=404, detail="Такой группы не найдено")

@app.get("/groups", response_model=List[GroupResponse])
def get_groups(
    year: Optional[int] = None,
    year_filter: Optional[str] = "eq",
    tutor_id: Optional[int] = None,
    is_active: Optional[bool] = None,
    student_count: Optional[int] = None,
    student_count_filter: Optional[str] = "eq",
    cipher_of_the_training_area: Optional[str] = None,
    number: Optional[int] = None,
    after_class_number: Optional[int] = None
):
    query = Groups.select()

    if year is not None:
        if year_filter == "lt":
            query = query.where(Groups.year < year)
        elif year_filter == "gt":
            query = query.where(Groups.year > year)
        else:
            query = query.where(Groups.year == year)

    if tutor_id is not None:
        query = query.where(Groups.tutor_id == tutor_id)

    if is_active is not None:
        query = query.where(Groups.is_active == is_active)

    if student_count is not None:
        if student_count_filter == "lt":
            query = query.where(Groups.student_count < student_count)
        elif student_count_filter == "gt":
            query = query.where(Groups.student_count > student_count)
        else: 
            query = query.where(Groups.student_count == student_count)

    if cipher_of_the_training_area is not None:
        query = query.where(Groups.cipher_of_the_training_area == cipher_of_the_training_area)

    if number is not None:
        query = query.where(Groups.number == number)
    
    if after_class_number is not None:
        query = query.where(Groups.after_class_number == after_class_number)
    
    groups = query.execute()
    
    return [
        GroupResponse(
            id=group.id,
            year=group.year,
            is_active=group.is_active,
            tutor_id=group.tutor_id,
            student_count=group.student_count,
            cipher_of_the_training_area=group.cipher_of_the_training_area,
            number=group.number,
            after_class_number=group.after_class_number,
            prefix=group.prefix,
        )
        for group in groups
    ]

"""Точка входа"""
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("service:app", host="127.0.0.1", port=8000, reload=True)