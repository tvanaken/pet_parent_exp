from datetime import date
from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, Date, Text
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.dialects.postgresql import ARRAY
from .base import Base


class Reminder(Base):
    __tablename__ = "reminders"

    # id = Column(Integer, primary_key=True)
    # user_id = mapped_column(Integer, ForeignKey("users.id"))
    # user = relationship("User")
    # title = Column(String)
    # frequency = Column(String)
    # start_date = Column(Date)
    # end_date = Column(Date)

    id = Column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"))
    user = relationship("User")
    title = Column(String)
    daysOfWeek = Column(ARRAY(Integer))
    start = Column(Date)
    end = Column(Date)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "type": self.type,
            "daysOfWeek": self.daysOfWeek,
            "start": self.start.isoformat() if self.start else None,
            "end": self.end.isoformat() if self.end else None
        }