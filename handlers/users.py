from sqlalchemy.orm import Session
from models.user import User

from pydantic_schemas.schemas import BaseUser


def create_user(db: Session, user: BaseUser) -> User:
    db_user = User(email=user.email, username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


# used to validate a new user email is unique
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
