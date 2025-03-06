from pydantic import BaseModel, Field
from typing import Annotated
from fastapi import Form


class DeleteUserRequest(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    master_password: str = Field(min_length=1, max_length=50)

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "tool_user",
                "master_password": "pppp1234",
            }
        }
    }


class AddUserRequest(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=1, max_length=50)
    master_password: str = Field(min_length=1, max_length=50)

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "tool_user",
                "password": "mypass1234",
                "master_password": "pppp1234",
            }
        }
    }


class ExecuteCommandRequest(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=1, max_length=50)

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "tool_user",
                "password": "mypass1234",
            }
        }
    }


class ScheduleCommandRequest(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=1, max_length=50)
    hour: int = Field(ge=0, le=23)
    minute: int = Field(ge=0, le=59)

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "tool_user",
                "password": "mypass1234",
                "hour": 23,
                "minute": 45,
            }
        }
    }


delete_user_request = Annotated[DeleteUserRequest, Form()]
add_user_request = Annotated[AddUserRequest, Form()]
