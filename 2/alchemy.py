import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine, Date, Float, ForeignKey, BLOB


import datetime

CBase = declarative_base()
engine = create_engine(f'sqlite:///{os.path.join("counter.db")}')


class Images(CBase):
    # имя таблицы
    __tablename__ = 'images'

    # поля таблицы
    id = Column(Integer, primary_key=True)
    images = Column(BLOB)

    def __init__(self, images):
        self.images = images

CBase.metadata.create_all(engine)

class Connect:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Connect, cls).__new__(cls)

        return cls.instance

    def __init__(self):
        # создадим подключение к базе
        path = os.path.join('counter.db')
        engine = create_engine('sqlite:///{}'.format(path))
        # создадим сессию для базы
        self.session = sessionmaker(bind=engine)()

    def get_session(self):
        return self.session
