from typing import List, Optional
from pydantic import BaseModel, Field


class ProjectSchema(BaseModel):
    name: str = Field(...)
    description: str = Field(...)
    owner: str = Field(...)
    team: List[dict] = Field(...)
    tasks: Optional[List[dict]] = Field(...)
    documents: Optional[List[dict]] = Field(...)
    milestones: Optional[List[dict]] = Field(...)
    budget: dict = Field(...)

    class Config:
        json_schema_extra = {
           "example": {
                "name": "Research Project on Climate Change",
                "description": "Investigating the impact of climate change on marine ecosystems.",
                "owner": "609ac3a2a2eb02db7c2d425d",
                "team": [
                    {
                        "user_id": "609ac3a2a2eb02db7c2d425d",
                        "role": "Owner"
                    },
                    {
                        "user_id": "609ac3d1a2eb02db7c2d425f",
                        "role": "Project Lead"
                    },
                    {
                        "user_id": "609ac3e1a2eb02db7c2d4260",
                        "role": "Project Manager"
                    }
                ],
                "tasks": [
                    {
                        "title": "Literature Review",
                        "description": "Review existing literature on climate change effects on marine life.",
                        "assigned_to": "609ac3a2a2eb02db7c2d425d",
                        "due_date": "2024-06-30T00:00:00.000Z"
                    },
                    {
                        "title": "Data Collection",
                        "description": "Collect data on ocean temperature and acidity levels.",
                        "assigned_to": "609ac3d1a2eb02db7c2d425f",
                        "due_date": "2024-07-15T00:00:00.000Z"
                    }
                ],
                "documents": [
                    {
                        "name": "Research Paper",
                        "file_url": "https://example.com/research_paper.pdf"
                    },
                    {
                        "name": "Dataset",
                        "file_url": "https://example.com/dataset.csv"
                    }
                ],
                "milestones": [
                    {
                        "name": "Research Proposal Submission",
                        "due_date": "2024-05-15T00:00:00.000Z"
                    },
                    {
                        "name": "Data Analysis Completed",
                        "due_date": "2024-08-15T00:00:00.000Z"
                    }
                ],
                "reminders": [
                    {
                        "name": "Research Proposal Submission",
                        "due_date": "2024-05-15T00:00:00.000Z"
                    },
                    {
                        "name": "Data Analysis Completed",
                        "due_date": "2024-08-15T00:00:00.000Z"
                    }
                ],
                  "budget": {
                    "total": 5000,
                    "spent": 2000,
                    "remaining": 3000
                }
            }
        }

class UpdateProjectModel(BaseModel):
    name: Optional[str]
    description: Optional[str]
    owner: Optional[str]
    team: Optional[List[dict]]
    tasks: Optional[List[dict]]
    documents: Optional[List[dict]]
    milestones: Optional[List[dict]]
    reminders: Optional[List[dict]]
    budget: Optional[dict]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Research Project on Climate Change",
                "description": "Investigating the impact of climate change on marine ecosystems.",
                "owner": "609ac3a2a2eb02db7c2d425d",
                "team": [
                    {
                        "user_id": "609ac3a2a2eb02db7c2d425d",
                        "role": "Owner"
                    },
                    {
                        "user_id": "609ac3d1a2eb02db7c2d425f",
                        "role": "Project Lead"
                    },
                    {
                        "user_id": "609ac3e1a2eb02db7c2d4260",
                        "role": "Project Manager"
                    }
                ],
                "tasks": [
                    {
                        "title": "Literature Review",
                        "description": "Review existing literature on climate change effects on marine life.",
                        "assigned_to": "609ac3a2a2eb02db7c2d425d",
                        "due_date": "2024-06-30T00:00:00.000Z"
                    },
                    {
                        "title": "Data Collection",
                        "description": "Collect data on ocean temperature and acidity levels.",
                        "assigned_to": "609ac3d1a2eb02db7c2d425f",
                        "due_date": "2024-07-15T00:00:00.000Z"
                    }
                ],
                "documents": [
                    {
                        "name": "Research Paper",
                        "file_url": "https://example.com/research_paper.pdf"
                    },
                    {
                        "name": "Dataset",
                        "file_url": "https://example.com/dataset.csv"
                    }
                ],
                "milestones": [
                    {
                        "name": "Research Proposal Submission",
                        "due_date": "2024-05-15T00:00:00.000Z"
                    },
                    {
                        "name": "Data Analysis Completed",
                        "due_date": "2024-08-15T00:00:00.000Z"
                    }
                ],
                "reminders": [
                    {
                        "name": "Research Proposal Submission",
                        "due_date": "2024-05-15T00:00:00.000Z"
                    },
                    {
                        "name": "Data Analysis Completed",
                        "due_date": "2024-08-15T00:00:00.000Z"
                    }
                ],
                "budget": {
                    "total": 5000,
                    "spent": 2000,
                    "remaining": 3000
                }
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
