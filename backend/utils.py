import json
from pathlib import Path

TASKK_FILE = Path(__file__).resolve().parent.parent / "tasks.json"

def load_tasks():
    try:
        with open(TASKK_FILE, "r") as f:
            return json.load(f)
    except FileExistsError:
        return []
    
def save_tasks(tasks):
    with open(TASKK_FILE, "w") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)