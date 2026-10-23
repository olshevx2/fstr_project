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