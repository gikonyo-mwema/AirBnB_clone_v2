#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv

Base = declarative_base()


class State(BaseModel):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        cities = relationship("City", backref="state", cascade="all, delete")
    else:
        @property
        def cities(self):
            """
            getter attribute cities that returns the list of City
            instances with state_id equals to the current State.id
            """
            from models.city import City
            from models import storage
            return [city for city in storage.all(City).values()
                    if city.state_id == self.id]
