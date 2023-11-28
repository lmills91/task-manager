import datetime
from sqlalchemy import Column, ForeignKey, Integer, DateTime, String

from database import Base


class History(Base):
    __tablename__ = "history"
    id = Column(Integer, primary_key=True, index=True)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
    action = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    task_id = Column(Integer, ForeignKey("users.id"))
