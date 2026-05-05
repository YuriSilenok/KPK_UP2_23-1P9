from contextlib import asynccontextmanager
from peewee import SqliteDatabase, Model, CharField, IntegerField
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

db = SqliteDatabase('curriculum_plans.db')


class CurriculumPlan(Model):
    discipline_name = CharField(max_length=200, null=False, verbose_name="Название дисциплины")
    specialty_id = IntegerField(null=False, verbose_name="ID специальности")
    semester = IntegerField(null=False, verbose_name="Семестр")
    theory_hours = IntegerField(null=False, verbose_name="Теоретические часы")
    practice_hours = IntegerField(null=False, verbose_name="Практические часы")
    total_hours = IntegerField(null=False, verbose_name="Всего часов")
    assessment_form = CharField(max_length=20, null=False, verbose_name="Форма отчетности")

    class Meta:
        database = db
        table_name = 'curriculum_plans'


def init_db():
    db.connect()
    db.create_tables([CurriculumPlan], safe=True)
    db.close()


class CurriculumPlanCreate(BaseModel):
    discipline_name: str = Field(..., max_length=200, description="Название дисциплины")
    specialty_id: int = Field(..., description="ID специальности")
    semester: int = Field(..., ge=1, le=8, description="Семестр (1-8)")
    theory_hours: int = Field(..., ge=0, description="Теоретические часы")
    practice_hours: int = Field(..., ge=0, description="Практические часы")
    total_hours: int = Field(..., ge=0, description="Всего часов")
    assessment_form: str = Field(..., description="Форма отчетности")

    @field_validator('assessment_form')
    @classmethod
    def validate_assessment_form(cls, v: str) -> str:
        allowed = ['экзамен', 'зачет', 'курсовая']
        if v not in allowed:
            raise ValueError(f'Форма отчетности должна быть одной из: {allowed}')
        return v


class CurriculumPlanUpdate(BaseModel):
    discipline_name: Optional[str] = Field(None, max_length=200, description="Название дисциплины")
    theory_hours: Optional[int] = Field(None, ge=0, description="Теоретические часы")
    practice_hours: Optional[int] = Field(None, ge=0, description="Практические часы")
    total_hours: Optional[int] = Field(None, ge=0, description="Всего часов")
    assessment_form: Optional[str] = Field(None, description="Форма отчетности")

    @field_validator('assessment_form')
    @classmethod
    def validate_assessment_form(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            allowed = ['экзамен', 'зачет', 'курсовая']
            if v not in allowed:
                raise ValueError(f'Форма отчетности должна быть одной из: {allowed}')
        return v


class CurriculumPlanOut(BaseModel):
    id: int
    discipline_name: str
    specialty_id: int
    semester: int
    theory_hours: int
    practice_hours: int
    total_hours: int
    assessment_form: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Запуск сервера Curriculum Plan Service...")
    init_db()
    print("База данных инициализирована")
    yield
    print("Остановка сервера...")
    if not db.is_closed():
        db.close()
    print("Ресурсы освобождены")


app = FastAPI(
    title="Curriculum Plan Service",
    description="Сервис управления учебными планами",
    version="1.0",
    lifespan=lifespan
)


@app.post("/curriculum-plans", response_model=CurriculumPlanOut, status_code=201)
def create_curriculum_plan(plan: CurriculumPlanCreate):
    db.connect()
    try:
        if CurriculumPlan.select().where(
            (CurriculumPlan.discipline_name == plan.discipline_name) &
            (CurriculumPlan.specialty_id == plan.specialty_id) &
            (CurriculumPlan.semester == plan.semester)
        ).exists():
            raise HTTPException(400, "Учебный план для такой дисциплины, специальности и семестра уже существует")

        new_plan = CurriculumPlan.create(
            discipline_name=plan.discipline_name,
            specialty_id=plan.specialty_id,
            semester=plan.semester,
            theory_hours=plan.theory_hours,
            practice_hours=plan.practice_hours,
            total_hours=plan.total_hours,
            assessment_form=plan.assessment_form
        )
        return new_plan
    finally:
        db.close()


@app.get("/curriculum-plans/{plan_id}", response_model=CurriculumPlanOut)
def get_curriculum_plan(plan_id: int):
    db.connect()
    try:
        plan = CurriculumPlan.get_by_id(plan_id)
        return plan
    except CurriculumPlan.DoesNotExist:
        raise HTTPException(404, "Учебный план не найден")
    finally:
        db.close()


@app.get("/curriculum-plans", response_model=List[CurriculumPlanOut])
def list_curriculum_plans(
    specialty_id: Optional[int] = Query(None, description="Фильтр по ID специальности"),
    semester: Optional[int] = Query(None, ge=1, le=8, description="Фильтр по семестру"),
    assessment_form: Optional[str] = Query(None, description="Фильтр по форме отчетности"),
    limit: int = Query(100, ge=1, le=500, description="Лимит записей")
):
    db.connect()
    try:
        query = CurriculumPlan.select()
        if specialty_id:
            query = query.where(CurriculumPlan.specialty_id == specialty_id)
        if semester:
            query = query.where(CurriculumPlan.semester == semester)
        if assessment_form:
            query = query.where(CurriculumPlan.assessment_form == assessment_form)

        result = list(query.limit(limit))
        return result
    finally:
        db.close()


@app.put("/curriculum-plans/{plan_id}", response_model=CurriculumPlanOut)
def update_curriculum_plan(plan_id: int, plan: CurriculumPlanUpdate):
    db.connect()
    try:
        if not CurriculumPlan.select().where(CurriculumPlan.id == plan_id).exists():
            raise HTTPException(404, "Учебный план не найден")

        update_data = {}
        if plan.discipline_name is not None:
            update_data['discipline_name'] = plan.discipline_name
        if plan.theory_hours is not None:
            update_data['theory_hours'] = plan.theory_hours
        if plan.practice_hours is not None:
            update_data['practice_hours'] = plan.practice_hours
        if plan.total_hours is not None:
            update_data['total_hours'] = plan.total_hours
        if plan.assessment_form is not None:
            update_data['assessment_form'] = plan.assessment_form

        if update_data:
            CurriculumPlan.update(update_data).where(CurriculumPlan.id == plan_id).execute()

        updated = CurriculumPlan.get_by_id(plan_id)
        return updated
    finally:
        db.close()


@app.delete("/curriculum-plans/{plan_id}")
def delete_curriculum_plan(plan_id: int):
    db.connect()
    try:
        deleted = CurriculumPlan.delete().where(CurriculumPlan.id == plan_id).execute()
        return {"deleted": bool(deleted)}
    finally:
        db.close()


@app.get("/")
def root():
    return {
        "service": "Curriculum Plan Service",
        "version": "1.0",
        "endpoints": {
            "POST /curriculum-plans": "Создать учебный план",
            "GET /curriculum-plans": "Список учебных планов",
            "GET /curriculum-plans/{id}": "Получить по ID",
            "PUT /curriculum-plans/{id}": "Обновить",
            "DELETE /curriculum-plans/{id}": "Удалить"
        }
    }


if __name__ == "__main__":
    import uvicorn
    print("=" * 50)
    print("Запуск сервера Curriculum Plan Service...")
    print("Документация API: http://localhost:8000/docs")
    print("=" * 50)
    uvicorn.run(app, host="127.0.0.1", port=8000)