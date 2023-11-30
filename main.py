import logging
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import handlers.users as user_handler
import handlers.tasks as task_handler

from contextlib import asynccontextmanager
from alembic.config import Config
from alembic import command

from database import SessionLocal
from models.user import User

from pydantic_schemas.schemas import *
from fastapi.security import OAuth2PasswordBearer

log = logging.getLogger("uvicorn")


def run_upgrade_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


@asynccontextmanager
async def lifespan(app_: FastAPI):
    log.info("Starting up...")
    log.info("Run alembic upgrade head...")
    run_upgrade_migrations()
    yield
    log.info("Shutting down...")


app = FastAPI(lifespan=lifespan)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def fake_decode_token(token):
    # change the details here if you wanted to use a different user
    # comment/uncomment to try different ones
    return User(
        # id=1, username="test1", email="test1@test.com"
        id=2,
        username="test2",
        email="test2@test.com",
    )


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    # in a production system we would be using some sort of authentication middleware or username/password check
    user = fake_decode_token(token)
    return user


@app.post(
    "/users",
    status_code=201,
    response_model=UserResponse,
    description="Allows user to create a new user",
)
def create_user(user: BaseUser, db: Session = Depends(get_db)) -> UserResponse:
    db_user = user_handler.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_handler.create_user(db=db, user=user)


@app.post(
    "/tasks",
    status_code=201,
    response_model=TaskResponse,
    description="Allows user to create a new task",
)
def create_task(task: BaseTask, db: Session = Depends(get_db)) -> TaskResponse:
    # ensures that user exists before creating task
    # don't let user create task for a different user
    user = user_handler.get_user_by_id(db, task.owner_id)
    if not user:
        raise HTTPException(404, "User not found")
    task = task_handler.create_task(db, task)

    return task


@app.get(
    "/tasks",
    response_model=List[TaskResponse],
    description="Allows user to get a list of all active tasks that belong to them",
)
def get_tasks_for_user(
    current_user: Annotated[BaseUser, Depends(get_current_user)],
    db: Session = Depends(get_db),
) -> TaskResponse:
    # makes use of current user so that nobody can acces any tasks that are not owned by them
    tasks = task_handler.get_tasks_for_user(db, current_user)
    return tasks


@app.delete(
    "/tasks/{task_id}",
    status_code=204,
    description="Allows user to delete a task that is owned by them",
)
def delete_task(
    current_user: Annotated[BaseUser, Depends(get_current_user)],
    task_id: int,
    db: Session = Depends(get_db),
) -> None:
    task = task_handler.get_task_by_id(db, task_id, current_user)
    if not task:
        raise HTTPException(404, "task not found for current user")

    task_handler.delete_undelete_task(db, task, True)

    return


@app.put(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    description="Allows user to update a task that is owned by them",
)
def update_task(
    current_user: Annotated[BaseUser, Depends(get_current_user)],
    task_id: int,
    updates: BaseTask,
    db: Session = Depends(get_db),
) -> TaskResponse:
    task = task_handler.get_task_by_id(db, task_id, current_user)
    if not task:
        raise HTTPException(404, "task not found for current user")
    task = task_handler.update_task(db, task, updates)
    return task


@app.patch(
    "/tasks/restore/{task_id}",
    response_model=TaskResponse,
    description="Allows user to undelete a task that is owned by them",
)
def restore_task(
    current_user: Annotated[BaseUser, Depends(get_current_user)],
    task_id: int,
    db: Session = Depends(get_db),
) -> TaskResponse:
    task = task_handler.get_task_by_id(db, task_id, current_user, True)
    if not task:
        raise HTTPException(404, "task not found for current user")
    task = task_handler.delete_undelete_task(db, task)
    return task
