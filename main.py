from asyncio import exceptions
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import handlers.users as user_handler
import handlers.tasks as task_handler

from database import SessionLocal, engine
from models.history import History
from models.task import Task
from models.user import User

from pydantic_schemas.schemas import *
from fastapi.security import OAuth2PasswordBearer

History.metadata.create_all(bind=engine)
Task.metadata.create_all(bind=engine)
User.metadata.create_all(bind=engine)

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# would use a better way to do this in real life with oauth usernames and passwords.
def fake_decode_token(token)-> BaseUser:
    return User(username=token + "fakedecoded", email="laura@test.com")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)])-> BaseUser:
    user = fake_decode_token(token)
    return user


@app.post("/users", response_model=UserResponse)
def create_user(user: BaseUser, db: Session = Depends(get_db)) -> UserResponse:
    db_user = user_handler.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user.create_user(db=db, user=user)


@app.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskBase, db: Session = Depends(get_db)) -> TaskResponse:
    # ensures that user exists before creating task
    user = user_handler.get_user_by_id(db, task.owner_id)
    if not user:
        raise HTTPException(404, "User not found")
    task = task_handler.create_task(db, task)

    return task


@app.get("/tasks", response_model=List[TaskResponse])
def get_tasks_for_user(
    current_user: Annotated[BaseUser, Depends(get_current_user)],
    db: Session = Depends(get_db),
) -> TaskResponse:
    # makes use of current user so that nobody can acces any tasks that are not owned by them
    tasks = task_handler.get_tasks_for_user(db, current_user)
    return tasks


@app.delete("/tasks/{task_id}")
def delete_task(
    current_user: Annotated[BaseUser, Depends(get_current_user)],
    task_id: int,
    db: Session = Depends(get_db),
) -> None:
    task = task_handler.get_task_by_id(db, task_id, current_user)
    if not task:
        raise HTTPException(404, "task not found for current user")

    task_handler.delete_task(db, task)

    return


@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    current_user: Annotated[BaseUser, Depends(get_current_user)],
    task_id: int,
    updates: TaskBase,
    db: Session = Depends(get_db),
) -> TaskResponse:
    task = task_handler.get_task_by_id(db, task_id, current_user)
    if not task:
        raise HTTPException(404, "task not found for current user")
    task = task_handler.update_task(db, task, updates)
    return task


@app.patch("/tasks/restore/{task_id}", response_model=TaskResponse)
def restore_task(
    current_user: Annotated[BaseUser, Depends(get_current_user)],
    task_id: int,
    db: Session = Depends(get_db),
) -> TaskResponse:
    # allows user to undelete a task that is owned by them
    task = task_handler.get_task_by_id(db, task_id, current_user, True)
    if not task:
        raise HTTPException(404, "task not found for current user")
    task = task_handler.restore_task(db, task)
    return task
