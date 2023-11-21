from datetime import date
from unicodedata import numeric
from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, Date
from sqlalchemy.orm import mapped_column, relationship
from .base import Base


class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"))
    user = relationship("User")
    breed_id = mapped_column(Integer, ForeignKey("breeds.id"))
    breed = relationship("Breed")
    name = Column(String)
    age = Column(Integer)
    weight = Column(Numeric(precision=5, scale=2))
    birthday = Column(Date)
