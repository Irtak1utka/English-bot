import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_models import Base

DATABASE_URL = "sqlite:///" + os.path.abspath("db.sqlite")

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def create_db():
    Base.metadata.create_all(engine)
    print("База данных успешно создана!")