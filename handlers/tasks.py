from typing import List, Optional, Union
from sqlalchemy.orm import Session
from models.task import Task
from models.history import History
from pydantic_schemas.schemas import BaseUser
import handlers.users as user_handler

from pydantic_schemas.schemas import BaseTask, TaskResponse


def create_task(db: Session, task: BaseTask) -> TaskResponse:
    new_task = Task(
        title=task.title,
        description=task.description,
        owner_id=task.owner_id,
        due_date=task.due_date,
        status=task.status,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def delete_task(db: Session, task: TaskResponse) -> None:
    # task should be moved to history and marked as deleted
    # can only delete a task if user is the owner
    task.deleted = True
    new_history = History(owner_id=task.owner_id, task_id=task.id, action="Deleted")
    db.add(new_history)
    db.commit()
    db.refresh(task)
    db.refresh(new_history)
    return


def restore_task(db: Session, task: TaskResponse) -> TaskResponse:
    # undelete a task
    task.deleted = False
    new_history = History(owner_id=task.owner_id, task_id=task.id, action="Restored")
    db.add(new_history)
    db.commit()
    db.refresh(task)
    db.refresh(new_history)
    return task


def update_task(db: Session, task: TaskResponse, updates: BaseTask) -> TaskResponse:
    # allow user to update any field except for deleted. Can be restored from another endpoint.
    task.title = updates.title if updates.title else task.title
    task.owner_id = updates.owner_id if updates.owner_id else task.owner_id
    task.description = updates.description if updates.description else task.description
    task.status = updates.status if updates.status else task.status
    task.due_date = updates.due_date if updates.due_date else task.due_date

    db.commit()
    db.refresh(task)
    return task


def get_task_by_id(
    db: Session, task_id: int, current_user: BaseUser, deleted: Optional[bool] = False
) -> Union[TaskResponse, None]:
    # get specific non-deleted task for current user
    user_id = user_handler.get_user_by_email(db, current_user.email).id
    return (
        db.query(Task)
        .filter(Task.deleted == deleted)
        .filter(Task.id == task_id)
        .filter(Task.owner_id == user_id)
        .first()
    )


def get_tasks_for_user(db: Session, current_user: BaseUser) -> List[TaskResponse]:
    # should get all non-deleted tasks for current_user
    user_id = user_handler.get_user_by_email(db, current_user.email).id
    return (
        db.query(Task)
        .filter(Task.owner_id == user_id)
        .filter(Task.deleted == False)
        .all()
    )
