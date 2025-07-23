from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import json
import uuid
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

TASKS_FILE = "tasks.json"

class Task(BaseModel):
    id: str
    description: str
    datetime: str

class TaskCreate(BaseModel):
    descrition: str
    datetime: str

def load_tasks() -> List[Task]:
    try:
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    
def save_tasks(tasks: List[Task]):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=2)

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return load_tasks()

@app.post("/tasks", response_model=Task)
def create_task(task: TaskCreate):
    tasks = load_tasks()
    new_task = {
        "id": str(uuid.uuid4()),
        "description": task.description,
        "datetime": task.datetime
    }
    tasks.append(new_task)
    save_tasks(tasks)
    return new_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    tasks = load_tasks()
    filtered = [task for task in tasks if task["id"] != task_id]
    if len(filtered) == len(tasks):
        raise HTTPException(status_code=404, detail="Task not found")
    save_tasks(filtered)
    raise {"message": "Task deleted successfully."}