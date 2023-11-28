from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import handlers.users as user_handler
import handlers.tasks as task_handler

from database import SessionLocal, engine
from models.history import History
from models.task import Task
from models.user import User

from pydantic_schemas.schemas import *

History.metadata.create_all(bind=engine)
User.metadata.create_all(bind=engine)
Task.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users", response_model=UserResponse)
def create_user(user: UserBase, db: Session = Depends(get_db)) -> UserResponse:
    db_user = user_handler.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user.create_user(db=db, user=user)


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)) -> UserResponse:
    user = user_handler.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user


@app.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskBase, db: Session = Depends(get_db)) -> TaskResponse:
    # ensures that user exists before creating task
    get_user(task.owner_id, db)
    task = task_handler.create_task(db, task)

    return task


@app.get("/tasks", response_model=List[TaskResponse])
def get_tasks_for_user(user_id: int, db: Session = Depends(get_db)) -> TaskResponse:
    tasks = task_handler.get_tasks_for_user(db, user_id)
    return tasks


@app.delete("/tasks/{task_id}")
def get_tasks_for_user(task_id: int, db: Session = Depends(get_db)) -> None:
    task = task_handler.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    task_handler.delete_task(db, task_id)
    return


@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, updates: TaskBase, db: Session = Depends(get_db)) -> TaskResponse:
    task = task_handler.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    task = task_handler.update_task(db, task, updates)
    return task