from pydantic import BaseModel
from typing import Optional

class Task(BaseModel):
    description: str
    done: bool = False
    data: Optional[str] = None
    hora: Optional[str] = None