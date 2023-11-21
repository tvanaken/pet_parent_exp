from datetime import date
from unicodedata import numeric
from sqlalchemy import Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import mapped_column, relationship
from .base import Base


class Food(Base):
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True)
    type = Column(String)
    name = Column(String)
    ingredients = Columns(String)
    crude_protein = Column(Numeric(precision=5, scale=2))
    crude_fat = Column(Numeric(precision=5, scale=2))
    crude_fiber = Column(Numeric(precision=5, scale=2))
    moisture = Column(Numeric(precision=5, scale=2))
    dietary_starch = Column(Numeric(precision=5, scale=2))
    epa = Column(Numeric(precision=5, scale=2))
    calcium = Column(Numeric(precision=5, scale=2))
    phosphorus = Column(Numeric(precision=5, scale=2))
    vitamin_e = Column(Integer)
    Omega_6 = Column(Numeric(precision=5, scale=2))
    Omega_3 = Column(Numeric(precision=5, scale=2))
    glucosamine = Column(Integer)
    microorganisms = Column(Integer)
