from typing import List
from pydantic import BaseModel


class TaskShemaGet(BaseModel):
    id: int
    title: str
    description: str | None = None
    completed: bool

    model_config = {
        "from_attributes": True
    }


class TaskShemaPost(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False

    model_config = {
        "from_attributes": True
    }


class TaskShemaGetList(BaseModel):
    success: bool
    data: List[TaskShemaGet]


class TaskSchemaSingleGet(BaseModel):
    success: bool
    data: TaskShemaGet
