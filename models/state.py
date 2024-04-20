#!/usr/bin/python3
"""
Defines the State class.
"""
import models
from models.base_model import Base
from models.base_model import BaseModel
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel, Base):
    """
    The State class inherits from BaseModel and Base. It links to the MySQL
    table 'states', and it has the class attribute 'name' which represents a
    string of maximum 128 characters and cannot be null. It also has the
    'cities' relationship which represents a one-to-many relationship between
    the State and City classes.
    """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state", cascade="delete")

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """
            Returns the list of City instances with state_id equals to the
            current State.id. This property method gets invoked only if the
            environment variable HBNB_TYPE_STORAGE is not set to "db".
            """
            return [city for city in models.storage.all(City).values()
                    if city.state_id == self.id]
