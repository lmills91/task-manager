from typing import Union, List

from pydantic import BaseModel, validator


class TaskBase(BaseModel):
    title: str
    description: Union[str, None] = None
    owner_id: int
    status: str = "Pending"
    deleted: bool = False

    @validator('status')
    def check_status_value(cls, status):
        allowed_values = ['Doing', 'Pending', 'Blocked', 'Done']
        if status not in allowed_values:
            raise ValueError(f'Status must be one of: {allowed_values}')
        return status

    class Config:
        orm_mode = True


class TaskResponse(TaskBase):
    id: int


class UserBase(BaseModel):
    email: str


class UserResponse(UserBase):
    id: int
    Tasks: List[TaskBase] = []

    class Config:
        orm_mode = True
