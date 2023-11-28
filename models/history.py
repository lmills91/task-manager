from sqlalchemy import Column, ForeignKey, Integer

from database import Base


class History(Base):
    __tablename__ = "history"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    task_id = Column(Integer, ForeignKey("users.id"))
