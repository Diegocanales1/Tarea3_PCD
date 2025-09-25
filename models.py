import json
from sqlalchemy import Column, Integer, String, Text
from typing import List
from database import Base 

class User(Base):
    """
    Modelo de SQLAlchemy para la tabla de usuarios.
    """
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String)
    user_email = Column(String, unique=True, index=True)
    age = Column(Integer, nullable=True)
    # recommendations se almacena como un string JSON
    recommendations = Column(Text, default=json.dumps([]))
    ZIP = Column(String, nullable=True)

    def __repr__(self):
        return f"<User(user_id={self.user_id}, user_name='{self.user_name}', user_email='{self.user_email}')>"

    @property
    def recommendations_list(self) -> List[str]:
        """Convierte el string JSON a una lista de Python."""
        return json.loads(self.recommendations)

    @recommendations_list.setter
    def recommendations_list(self, value: List[str]):
        """Serializa la lista de Python a un string JSON."""
        self.recommendations = json.dumps(value)