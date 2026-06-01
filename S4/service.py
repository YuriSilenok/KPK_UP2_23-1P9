from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List
from models import db, Permission, RolePermission, init_db


class PermissionCreate(BaseModel):
    name: str = Field(..., max_length=100, description="Название разрешения")
    description: Optional[str] = Field('', max_length=255, description="Описание")


class PermissionUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100, description="Название разрешения")
    description: Optional[str] = Field(None, max_length=255, description="Описание")


class PermissionOut(BaseModel):
    id: int
    name: str
    description: str
    is_active: bool


class DeleteResponse(BaseModel):
    deleted: bool


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Запуск Permission Service...")
    init_db()
    print("База данных инициализирована")
    yield
    print("Остановка сервера...")
    if not db.is_closed():
        db.close()


app = FastAPI(
    title="Permission Service",
    description="Сервис управления разрешениями",
    version="1.0",
    lifespan=lifespan
)


@app.post("/permissions", response_model=PermissionOut, status_code=201)
def create_permission(perm: PermissionCreate):
    db.connect()
    try:
        if Permission.select().where(Permission.name == perm.name).exists():
            raise HTTPException(400, "Разрешение с таким названием уже существует")

        new_perm = Permission.create(
            name=perm.name,
            description=perm.description or ''
        )
        return new_perm
    finally:
        db.close()


@app.get("/permissions/{perm_id}", response_model=PermissionOut)
def get_permission(perm_id: int):
    db.connect()
    try:
        perm = Permission.get_or_none(Permission.id == perm_id)
        if perm is None:
            raise HTTPException(404, "Разрешение не найдено")
        return perm
    finally:
        db.close()


@app.get("/permissions", response_model=List[PermissionOut])
def list_permissions(
    name: Optional[str] = Query(None, description="Фильтр по названию"),
    is_active: Optional[bool] = Query(None, description="Фильтр по активности"),
    limit: int = Query(100, ge=1, le=500, description="Лимит записей"),
    offset: int = Query(0, ge=0, description="Смещение")
):
    db.connect()
    try:
        query = Permission.select()
        if name:
            query = query.where(Permission.name.contains(name))
        if is_active is not None:
            query = query.where(Permission.is_active == is_active)

        permissions = list(query.offset(offset).limit(limit))
        return permissions
    finally:
        db.close()


@app.put("/permissions/{perm_id}", response_model=PermissionOut)
def update_permission(perm_id: int, perm: PermissionUpdate):
    db.connect()
    try:
        existing = Permission.get_or_none(Permission.id == perm_id)
        if existing is None:
            raise HTTPException(404, "Разрешение не найдено")

        update_data = {}
        if perm.name is not None:
            if Permission.select().where(
                (Permission.name == perm.name) & (Permission.id != perm_id)
            ).exists():
                raise HTTPException(400, "Разрешение с таким названием уже существует")
            update_data['name'] = perm.name
        if perm.description is not None:
            update_data['description'] = perm.description

        if update_data:
            Permission.update(update_data).where(Permission.id == perm_id).execute()

        updated = Permission.get_by_id(perm_id)
        return updated
    finally:
        db.close()


@app.delete("/permissions/{perm_id}", response_model=PermissionOut)
def delete_permission(perm_id: int):
    db.connect()
    try:
        existing = Permission.get_or_none(Permission.id == perm_id)
        if existing is None:
            raise HTTPException(404, "Разрешение не найдено")

        existing.is_active = False
        existing.save()
        
        return existing
    finally:
        db.close()


@app.get("/")
def root():
    return {
        "service": "Permission Service",
        "version": "1.0",
        "endpoints": {
            "POST /permissions": "Создать разрешение",
            "GET /permissions/{id}": "Получить по ID",
            "GET /permissions": "Список с фильтрацией",
            "PUT /permissions/{id}": "Обновить",
            "DELETE /permissions/{id}": "Удалить (soft delete)"
        }
    }


if __name__ == "__main__":
    import uvicorn
    print("=" * 50)
    print("Запуск Permission Service...")
    print("Документация API: http://localhost:8000/docs")
    print("=" * 50)
    uvicorn.run(app, host="127.0.0.1", port=8000)