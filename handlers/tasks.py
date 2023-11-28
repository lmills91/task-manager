from http.client import HTTPException
from typing import List, Union
from sqlalchemy.orm import Session
from models.task import Task
from models.history import History

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


def delete_task(db: Session, task_id: int) -> None:
    # task should be moved to history and marked as deleted
    task = (
        db.query(Task).filter(Task.deleted == False).filter(Task.id == task_id).first()
    )
    if not task:
        raise HTTPException(404, "Task not found")
    task.deleted = True
    db.commit()
    new_history = History(owner_id=task.owner_id, task_id=task_id, action="Deleted")
    db.add(new_history)
    db.commit()
    db.refresh(task)
    db.refresh(new_history)
    return


def update_task(db: Session, task: TaskResponse, updates: TaskBase)-> TaskResponse:
    # allow user to update any field except for deleted. Can be restored from another endpoint.
    task.title = updates.title if updates.title else task.title
    task.owner_id = updates.owner_id if updates.owner_id else task.owner_id
    task.description = updates.description if updates.description else task.description
    task.status = updates.status if updates.status else task.status

    db.commit()
    db.refresh(task)
    return task


def get_task_by_id(db: Session, task_id: int) -> Union[TaskResponse, None]:
    return db.query(Task).get(task_id)


def get_tasks_for_user(db: Session, user_id: int) -> List[TaskResponse]:
    # should get all non-deleted tasks for user
    return (
        db.query(Task)
        .filter(Task.owner_id == user_id)
        .filter(Task.deleted == False)
        .all()
    )
