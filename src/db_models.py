from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Float, DateTime
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
import datetime

Base = declarative_base()


class UserTg(Base):
    __tablename__ = "users_tg"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    admin = Column(Integer, default=0)
    ban = Column(Integer, default=0)
    language = Column(String, default='ru')
    date = Column(DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f"<UserTg(id={self.id}, username='{self.username}', admin={self.admin}, ban={self.ban}, language='{self.language}', date='{self.date}')>"


class UserBot(Base):
    __tablename__ = "users_bot"

    id = Column(Integer, primary_key=True)
    nick = Column(String, unique=True)
    pass_hash = Column(String)
    count_of_cards = Column(Integer, default=0)
    rank = Column(Integer, default=0)
    premium = Column(DateTime)

    def __repr__(self):
        return f"<UserBot(id={self.id}, nick='{self.nick}', count_of_cards={self.count_of_cards}, rank={self.rank}, premium={self.premium})>"


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    translation = Column(String)
    collection = Column(Integer, ForeignKey('collection.id'))
    collection_rel = relationship("Collection", back_populates="cards")
    image_path = Column(String, nullable=True)  # Добавляем поле для хранения пути к изображению

    def __repr__(self):
        return f"<Card(id={self.id}, name='{self.name}', translation='{self.translation}', collection={self.collection})>"


class Collection(Base):
    __tablename__ = "collection"

    id = Column(Integer, primary_key=True)
    owner = Column(Integer)  # Добавлено поле owner
    name = Column(String)
    descript = Column(String)
    lang1 = Column(String)  # Язык оригинала
    lang2 = Column(String)  # Язык перевода
    cards = relationship("Card", back_populates="collection_rel")

    def __repr__(self):
        return f"<Collection(id={self.id}, owner={self.owner}, name='{self.name}', descript='{self.descript}, lang1='{self.lang1}, lang2='{self.lang2}')>"


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    id_to = Column(Integer)
    id_from = Column(Integer)
    review = Column(String)
    score = Column(Integer)

    def __repr__(self):
        return f"<Review(id={self.id}, id_to={self.id_to}, id_from={self.id_from}, score={self.score})>"