from datetime import datetime
from typing import Optional, Union, List

from pydantic import BaseModel, validator


class TaskPatch(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    owner_id: Optional[int] = None
    @validator("status")
    def check_status_value(cls, status):
        allowed_values = ["Doing", "Pending", "Blocked", "Done"]
        if status not in allowed_values:
            raise ValueError(f"Status must be one of: {allowed_values}")
        return status


class TaskBase(BaseModel):
    title: str
    description: Union[str, None] = None
    owner_id: int
    status: str = "Pending"
    deleted: bool = False

    @validator("status")
    def check_status_value(cls, status):
        allowed_values = ["Doing", "Pending", "Blocked", "Done"]
        if status not in allowed_values:
            raise ValueError(f"Status must be one of: {allowed_values}")
        return status


class TaskResponse(TaskBase):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserResponse(UserBase):
    id: int
    Tasks: List[TaskBase] = []

    class Config:
        orm_mode = True


class HistoryBase(BaseModel):
    date_created: datetime
    action: str
    owner_id: int
    task_id: int

    @validator("action")
    def check_action_value(cls, action):
        allowed_values = ["Deleted", "Status Update", "Restored", "Change Details"]
        if action not in allowed_values:
            raise ValueError(f"Action must be one of: {allowed_values}")
        return action

    class Config:
        orm_mode = True


class HistoryResponse(HistoryBase):
    id: int

    class Config:
        orm_mode = True
