from pydantic import BaseModel

class TaskItem(BaseModel):
    task: str
