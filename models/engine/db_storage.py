#!/usr/bin/python3
""" DBStorage Module """

from os import getenv
from sqlalchemy import create_engine, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.review import Review
from models.place import Place
from models.city import City
from models.amenity import Amenity


class DBStorage:
    """ DBStorage class """
    __engine = None
    __session = None

    def __init__(self):
        """ Initialization """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(getenv('HBNB_MYSQL_USER'),
                                             getenv('HBNB_MYSQL_PWD'),
                                             getenv("HBNB_MYSQL_HOST"),
                                             getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self._engine)

    def all(self, cls=None):
        """ Query all objects """
        classDict = {'City': City, 'State': State, 'User': User,
                     'Place': Place, 'Review': Review, 'Amenity': Amenity}
        if cls is None:
            objs = []
            for className in classDict:
                objs.extend(self.__session.query(classDict[className]).all())
            else:
                # Query objects of a specific class if a class is passed
                if isinstance(cls, str):
                    cls = classDict[cls]
                    objs = self.__session.query(cls).all()
                    return {"{}.{}".format(type(o).__name__, o.id): o
                            for o in objs}

    def new(self, obj):
        """ Add object to current database session """
        self.__session.add(obj)

    def save(self):
        """ Commit all changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ Delete  obj from current database session if not None """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """ Create all tables in the database and create the current ses """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Closes the current database session"""
        self.__session.close()
