from typing import Union
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.user import User

from pydantic_schemas.schemas import BaseUser


def create_user(db: Session, user: BaseUser) -> User:
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = User(email=user.email, username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


# used to validate a new user email is unique
def get_user_by_email(db: Session, email: str) -> Union[User, None]:
    return db.query(User).filter(User.email == email).first()
