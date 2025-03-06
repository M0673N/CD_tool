from pydantic import BaseModel, Field
from typing import Annotated
from fastapi import Form


class DeleteUserRequest(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    master_password: str = Field(min_length=1, max_length=50)


class AddUserRequest(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=1, max_length=50)
    master_password: str = Field(min_length=1, max_length=50)


class ExecuteCommandRequest(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=1, max_length=50)


class ScheduleCommandRequest(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=1, max_length=50)
    hour: int = Field(ge=0, le=23)
    minute: int = Field(ge=0, le=59)


delete_user_dependency = Annotated[DeleteUserRequest, Form()]
add_user_dependency = Annotated[AddUserRequest, Form()]
