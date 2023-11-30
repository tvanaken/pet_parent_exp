from datetime import date
from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, Date, Text
from sqlalchemy.orm import mapped_column, relationship
from .base import Base


class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"))
    user = relationship("User")
    type = Column(String)
    frequency = Column(String)
    start_date = Column(String)
    end_date = Column(String)