from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from database import SessionLocal, PerevalRepository

app = FastAPI()

class UserSchema(BaseModel):
    email: str
    fam: str
    name: str
    otc: str
    phone: str

class CoordsSchema(BaseModel):
    latitude: float
    longitude: float
    height: int

class LevelSchema(BaseModel):
    winter: Optional[str] = ""
    summer: Optional[str] = ""
    autumn: Optional[str] = ""
    spring: Optional[str] = ""

class ImageSchema(BaseModel):
    data: str
    title: str

class PerevalSchema(BaseModel):
    beauty_title: str
    title: str
    other_titles: str
    connect: str
    add_time: str
    user: UserSchema
    coords: CoordsSchema
    level: LevelSchema
    images: List[ImageSchema]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/submitData")
def submit_data(data: PerevalSchema, db=Depends(get_db)):
    try:
        repo = PerevalRepository(db)
        new_id = repo.add_pereval(data.dict())
        return {"status": 200, "message": None, "id": new_id}
    except Exception as e:
        return {"status": 500, "message": f"Ошибка: {str(e)}", "id": None}

# --- НОВЫЕ МЕТОДЫ ДЛЯ СПРИНТА 2 ---

@app.get("/submitData/{pereval_id}")
def get_submit_data(pereval_id: int, db=Depends(get_db)):
    repo = PerevalRepository(db)
    pereval = repo.get_pereval_by_id(pereval_id)
    if not pereval:
        raise HTTPException(status_code=404, detail="Перевал не найден")
    
    # Формируем ответ (можно использовать словарь)
    return {
        "id": pereval.id,
        "beauty_title": pereval.beauty_title,
        "title": pereval.title,
        "other_titles": pereval.other_titles,
        "connect": pereval.connect,
        "add_time": pereval.add_time,
        "status": pereval.status,
        "level": {
            "winter": pereval.level_winter,
            "summer": pereval.level_summer,
            "autumn": pereval.level_autumn,
            "spring": pereval.level_spring
        }
    }

@app.patch("/submitData/{pereval_id}")
def patch_submit_data(pereval_id: int, data: PerevalSchema, db=Depends(get_db)):
    repo = PerevalRepository(db)
    success, message = repo.update_pereval(pereval_id, data.dict())
    if success:
        return {"state": 1, "message": message}
    else:
        return {"state": 0, "message": message}

@app.get("/submitData/")
def get_submit_data_by_email(user__email: str, db=Depends(get_db)):
    repo = PerevalRepository(db)
    perevals = repo.get_pereval_by_email(user__email)
    if not perevals:
        raise HTTPException(status_code=404, detail="Записи не найдены")

    result = []
    for pereval in perevals:
        result.append({
            "id": pereval.id,
            "title": pereval.title,
            "status": pereval.status,
            "add_time": pereval.add_time
        })
    return result