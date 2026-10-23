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