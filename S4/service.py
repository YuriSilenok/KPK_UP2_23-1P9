from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List
from peewee import IntegrityError
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


class RolePermissionCreate(BaseModel):
    role_id: int = Field(..., description="ID роли (из Role Service)")
    permission_id: int = Field(..., description="ID разрешения")


class RolePermissionOut(BaseModel):
    id: int
    role_id: int
    permission_id: int


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
        with db.atomic():
            new_perm = Permission.create(
                name=perm.name,
                description=perm.description or ''
            )
            return new_perm
    except IntegrityError:
        raise HTTPException(400, "Разрешение с таким названием уже существует")
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
    name: Optional[str] = Query(None, description="Фильтр по названию (частичное совпадение)"),
    is_active: Optional[bool] = Query(None, description="Фильтр по активности"),
    limit: int = Query(100, ge=1, description="Лимит записей"),
    offset: int = Query(0, ge=0, description="Смещение для пагинации")
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
            update_data['name'] = perm.name
        if perm.description is not None:
            update_data['description'] = perm.description

        if update_data:
            try:
                with db.atomic():
                    Permission.update(update_data).where(Permission.id == perm_id).execute()
            except IntegrityError:
                raise HTTPException(400, "Разрешение с таким названием уже существует")

        updated = Permission.get_by_id(perm_id)
        return updated
    finally:
        db.close()


@app.delete("/permissions/{perm_id}", response_model=DeleteResponse)
def delete_permission(perm_id: int):
    db.connect()
    try:
        existing = Permission.get_or_none(Permission.id == perm_id)
        if existing is None:
            return DeleteResponse(deleted=False)

        existing.is_active = False
        existing.save()
        return DeleteResponse(deleted=True)
    finally:
        db.close()


@app.post("/role-permissions", response_model=RolePermissionOut, status_code=201)
def create_role_permission(rp: RolePermissionCreate):
    """Назначить разрешение роли"""
    db.connect()
    try:
        permission = Permission.get_or_none(
            (Permission.id == rp.permission_id) & (Permission.is_active == True)
        )
        if permission is None:
            raise HTTPException(404, f"Активное разрешение с id={rp.permission_id} не найдено")

        existing = RolePermission.get_or_none(
            (RolePermission.role_id == rp.role_id) &
            (RolePermission.permission_id == rp.permission_id)
        )
        if existing:
            raise HTTPException(400, "Связь между этой ролью и разрешением уже существует")

        with db.atomic():
            new_rp = RolePermission.create(
                role_id=rp.role_id,
                permission_id=rp.permission_id
            )
            return new_rp
    finally:
        db.close()


@app.delete("/role-permissions", response_model=DeleteResponse)
def delete_role_permission(
    role_id: int = Query(..., description="ID роли"),
    permission_id: int = Query(..., description="ID разрешения")
):
    db.connect()
    try:
        existing = RolePermission.get_or_none(
            (RolePermission.role_id == role_id) &
            (RolePermission.permission_id == permission_id)
        )
        if existing is None:
            return DeleteResponse(deleted=False)

        with db.atomic():
            RolePermission.delete().where(
                (RolePermission.role_id == role_id) &
                (RolePermission.permission_id == permission_id)
            ).execute()
            return DeleteResponse(deleted=True)
    finally:
        db.close()


@app.get("/role-permissions/{role_id}", response_model=List[PermissionOut])
def get_permissions_by_role(role_id: int):
    db.connect()
    try:
        query = (Permission
                 .select()
                 .join(RolePermission, on=RolePermission.permission_id == Permission.id)
                 .where(
                     (RolePermission.role_id == role_id) &
                     (Permission.is_active == True)
                 ))
        permissions = list(query)
        return permissions
    finally:
        db.close()


@app.get("/")
def root():
    return {
        "service": "Permission Service",
        "version": "1.0",
        "endpoints": {
            "POST /permissions": "Создать разрешение",
            "GET /permissions/{id}": "Получить разрешение по ID",
            "GET /permissions": "Список разрешений с фильтрацией",
            "PUT /permissions/{id}": "Обновить разрешение",
            "DELETE /permissions/{id}": "Удалить разрешение (soft delete)",
            "POST /role-permissions": "Назначить разрешение роли",
            "DELETE /role-permissions": "Отозвать разрешение у роли",
            "GET /role-permissions/{role_id}": "Получить разрешения для роли"
        }
    }


if __name__ == "__main__":
    import uvicorn
    print("=" * 50)
    print("Запуск Permission Service...")
    print("Документация API: http://localhost:8000/docs")
    print("=" * 50)
    uvicorn.run(app, host="127.0.0.1", port=8000)