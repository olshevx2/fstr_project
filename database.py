import os
from sqlalchemy import create_engine, Column, Integer, String, Float, TIMESTAMP, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("FSTR_DB_HOST", "localhost")
DB_PORT = os.getenv("FSTR_DB_PORT", "5432")
DB_LOGIN = os.getenv("FSTR_DB_LOGIN", "postgres")
DB_PASS = os.getenv("FSTR_DB_PASS", "123456")
DB_NAME = os.getenv("FSTR_DB_NAME", "pereval_db")

DATABASE_URL = f"postgresql://{DB_LOGIN}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    fam = Column(String)
    name = Column(String)
    otc = Column(String)
    phone = Column(String)

class Coords(Base):
    __tablename__ = 'coords'
    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    height = Column(Integer)

class Pereval(Base):
    __tablename__ = 'pereval_added'
    id = Column(Integer, primary_key=True, index=True)
    beauty_title = Column(String)
    title = Column(String)
    other_titles = Column(String)
    connect = Column(String)
    add_time = Column(TIMESTAMP)
    user_id = Column(Integer, ForeignKey('users.id'))
    coord_id = Column(Integer, ForeignKey('coords.id'))
    level_winter = Column(String)
    level_spring = Column(String)
    level_summer = Column(String)
    level_autumn = Column(String)
    status = Column(String, default='new')

class PerevalRepository:
    def __init__(self, db_session):
        self.db = db_session

    def add_pereval(self, data):
        user = self.db.query(User).filter(User.email == data['user']['email']).first()
        if not user:
            user = User(**data['user'])
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)

        coords = Coords(**data['coords'])
        self.db.add(coords)
        self.db.commit()
        self.db.refresh(coords)

        pereval = Pereval(
            beauty_title=data.get('beauty_title'),
            title=data.get('title'),
            other_titles=data.get('other_titles'),
            connect=data.get('connect'),
            add_time=data.get('add_time'),
            user_id=user.id,
            coord_id=coords.id,
            level_winter=data['level'].get('winter'),
            level_spring=data['level'].get('spring'),
            level_summer=data['level'].get('summer'),
            level_autumn=data['level'].get('autumn'),
            status='new'
        )
        self.db.add(pereval)
        self.db.commit()
        self.db.refresh(pereval)
        return pereval.id

# --- НОВЫЕ МЕТОДЫ ДЛЯ СПРИНТА 2 ---

    def get_pereval_by_id(self, pereval_id):
        return self.db.query(Pereval).filter(Pereval.id == pereval_id).first()

    def update_pereval(self, pereval_id, data):
        pereval = self.get_pereval_by_id(pereval_id)
        if not pereval:
            return False, "Запись не найдена"
        if pereval.status != 'new':
            return False, "Редактировать можно только записи в статусе 'new'"

        pereval.beauty_title = data.get('beauty_title', pereval.beauty_title)
        pereval.title = data.get('title', pereval.title)
        pereval.other_titles = data.get('other_titles', pereval.other_titles)
        pereval.connect = data.get('connect', pereval.connect)
        pereval.add_time = data.get('add_time', pereval.add_time)

        if 'coords' in data:
            coords = self.db.query(Coords).filter(Coords.id == pereval.coord_id).first()
            if coords:
                coords.latitude = data['coords'].get('latitude', coords.latitude)
                coords.longitude = data['coords'].get('longitude', coords.longitude)
                coords.height = data['coords'].get('height', coords.height)

        if 'level' in data:
            pereval.level_winter = data['level'].get('winter', pereval.level_winter)
            pereval.level_spring = data['level'].get('spring', pereval.level_spring)
            pereval.level_summer = data['level'].get('summer', pereval.level_summer)
            pereval.level_autumn = data['level'].get('autumn', pereval.level_autumn)

        self.db.commit()
        return True, "Успешно отредактировано"

    def get_pereval_by_email(self, email):
        return self.db.query(Pereval).join(User).filter(User.email == email).all()