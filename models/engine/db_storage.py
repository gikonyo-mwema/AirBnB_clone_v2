#!/usr/bin/python3
""" DBStorage Module """

from os import getenv
from sqlalchemy import create_engine, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base


class DBStorage:
    """ DBStorage class """
    __engine = None
    __session = None
    _FileStorage__objects = None


    def __init__(self):
        """ Initialization """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@localhost/{}'.
                                      format(getenv('HBNB_MYSQL_USER'),
                                             getenv('HBNB_MYSQL_PWD'),
                                             getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        self._FileStorage__objects = {}

        if getenv('HBNB_ENV') == 'test':

            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Query all objects """
        result = {}
        if cls is None:
            # Query all objects if no class is passed
            for  cls in [State, City]:
                objs = self.__session.query(cls).all()
                for obj in objs:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    result[key] = obj
        else:
            # Query objects of a specific class if a class is passed
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                result[key] = obj
        return result

    def new(self, obj):
        """ Add object to current database session """
        self.__session.add(obj)

    def save(self):
        """ Commit all changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ Delete  obj from current database session if not None """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ Create all tables in the database and create the current ses """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

