from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, field_validator, ConfigDict 
from typing import Optional, List
from models import Groups, db
from peewee import *
from pydantic import Field as PydanticField 
from contextlib import asynccontextmanager
import re

def createTables():
    db.connect()
    db.create_tables([Groups], safe=True)
    db.close()

class NewGroup(BaseModel):
    year: int = PydanticField(..., ge=2000, le=2999)
    tutor_id: Optional[int] = PydanticField(None, ge=1)
    student_count: Optional[int] = PydanticField(0, ge=0, le=30)
    cipher_of_the_training_area: str = PydanticField(...)
    number: int = PydanticField(..., ge=1)
    after_class_number: int
    prefix: str = PydanticField(..., min_length=1, max_length=2)
    
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
            raise ValueError("ID преподавателя должен быть положительным числом")
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
        if v < 1:
            raise ValueError("Номер группы должен быть от 1")
        return v
    
    @field_validator('after_class_number')
    @classmethod
    def validate_after_class_number(cls, v: int) -> int:
        if v not in [9, 11]:
            raise ValueError("После какого класса поступили должно быть 9 или 11")
        return v
    
    @field_validator('prefix')
    @classmethod
    def validate_prefix(cls, v: str) -> str:
        if not (1 <= len(v) <= 2):
            raise ValueError("Префикс должен содержать 1 или 2 символа")
        return v
    
    def to_dict(self):
        return self.model_dump()

class GroupUpdate(BaseModel):
    tutor_id: Optional[int] = PydanticField(None, ge=1)
    student_count: Optional[int] = PydanticField(None, ge=0, le=30)
    
    @field_validator('tutor_id')
    @classmethod
    def validate_tutor_id(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and v <= 0:
            raise ValueError("ID преподавателя должен быть положительным числом")
        return v
    
    def model_dump_with_skip_none(self):
        """Возвращает только те поля, которые были явно указаны (не None)"""
        return {k: v for k, v in self.model_dump().items() if v is not None}
    
class GroupResponse(BaseModel):
    id: int
    year: int
    is_active: bool
    tutor_id: Optional[int]
    student_count: int
    cipher_of_the_training_area: str
    number: int
    after_class_number: int
    prefix: str

    model_config = ConfigDict(from_attributes=True)

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

@app.post("/groups", response_model=GroupResponse, status_code=201)
def add_group(group_data: NewGroup):
    # Используем транзакцию для атомарности
    with db.atomic():
        existing_group = Groups.get_or_none(
            (Groups.number == group_data.number) &
            (Groups.after_class_number == group_data.after_class_number) &
            (Groups.prefix == group_data.prefix) &
            (Groups.is_active == True)
        )

        if existing_group:
            raise HTTPException(
                status_code=409,
                detail="Активная группа с такими параметрами уже существует"
            )

        try:
            group = Groups(
                year=group_data.year,
                is_active=True,
                tutor_id=group_data.tutor_id,
                student_count=group_data.student_count,
                cipher_of_the_training_area=group_data.cipher_of_the_training_area,
                number=group_data.number,
                after_class_number=group_data.after_class_number,
                prefix=group_data.prefix
            )
            
            group.validate()
            rows_affected = group.save()
            
            if rows_affected == 0:
                raise HTTPException(status_code=500, detail="Не удалось сохранить группу")
                
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail="Ошибка при сохранении в базу данных")

    return GroupResponse.model_validate(group)

@app.put("/groups/{group_id}", response_model=GroupResponse)
def update(group_id: int, update_data: GroupUpdate):
    group = Groups.get_or_none(Groups.id == group_id)
    if group is None:
        raise HTTPException(status_code=404, detail="Группа не найдена")

    update_dict = update_data.model_dump_with_skip_none()
    
    if not update_dict:
        raise HTTPException(status_code=400, detail="Нет данных для обновления")
    
    for key, value in update_dict.items():
        setattr(group, key, value)
    
    try:
        group.validate()
        rows_affected = group.save()
        
        if rows_affected == 0:
            raise HTTPException(status_code=500, detail="Не удалось обновить группу")
            
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ошибка при обновлении базы данных")

    return GroupResponse.model_validate(group)

@app.delete("/groups/{group_id}")
def delete_group(group_id: int):
    group = Groups.get_or_none(Groups.id == group_id)
    if group is None:
        raise HTTPException(status_code=404, detail="Группа не найдена")
    
    # Используем метод модели вместо прямой установки
    try:
        group.soft_delete()
        rows_affected = group.save()
        
        if rows_affected == 0:
            raise HTTPException(status_code=500, detail="Не удалось удалить группу")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ошибка при удалении группы")
    
    return {"deleted": True}

@app.get("/groups/{group_id}", response_model=GroupResponse)
def get_group(group_id: int):
    group = Groups.get_or_none(Groups.id == group_id)
    
    if group:
        return GroupResponse.model_validate(group)
    
    raise HTTPException(status_code=404, detail="Группа не найдена")

@app.get("/groups", response_model=List[GroupResponse])
def get_groups(
    year: Optional[int] = None,
    year_filter: Optional[str] = Query("eq", regex="^(eq|lt|gt)$"),
    tutor_id: Optional[int] = None,
    is_active: Optional[bool] = None,
    student_count: Optional[int] = None,
    student_count_filter: Optional[str] = Query("eq", regex="^(eq|lt|gt)$"),
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
    
    return [GroupResponse.model_validate(group) for group in groups]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("service:app", host="127.0.0.1", port=8000, reload=True)