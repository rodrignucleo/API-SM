from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    projects: Optional[List[dict]] = Field(default_factory=list)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Alice Smith",
                "email": "alice@example.com",
                "password": "hashed_password_here",
                "projects": [
                    {
                        "project_id": "609ac3e1a2eb02db7c2d425e",
                        "role": "Owner"
                    },
                    {
                        "project_id": "609ac3f1a2eb02db7c2d4261",
                        "role": "Project Lead"
                    }
                ]
            }
        }


class UpdateUserModel(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    projects: Optional[List[dict]]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Alice Smith",
                "email": "alice@example.com",
                "password": "new_hashed_password_here",
                "projects": [
                    {
                        "project_id": "609ac3e1a2eb02db7c2d425e",
                        "role": "Owner"
                    },
                    {
                        "project_id": "609ac3f1a2eb02db7c2d4261",
                        "role": "Project Lead"
                    }
                ]
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
