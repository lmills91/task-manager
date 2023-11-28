from typing import List
from sqlalchemy.orm import Session
from models.task import Task

from pydantic_schemas.schemas import TaskBase, TaskResponse


def create_task(db: Session, task: TaskBase) -> TaskResponse:
    new_task = Task(
        title=task.title,
        description=task.description,
        owner_id=task.owner_id,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def get_tasks_for_user(db: Session, user_id: int) -> List[TaskResponse]:
    return db.query(Task).filter(Task.owner_id == user_id).all()
