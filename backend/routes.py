from fastapi import APIRouter, HTTPException
from backend.models import Task
from backend.utils import load_tasks, save_tasks
from backend.ai import interpretar_tarefa

router = APIRouter()

@router.post("/tasks")
def listar_tarefas():
    return load_tasks()

@router.post("/tasks")
def adicionar_tarefa(task: Task):
    tasks = load_tasks()
    tasks.append(task.dict())
    save_tasks(tasks)
    return {"message": "Tarefa adicionada com sucesso!"}

@router.post("/tasks/ia")
def adicionar_tarefa_ia(comando: str):
    comando = payload.get("comando")
    if not comando:
        raise HTTPException(status_code=400, detail="Comando não fornecido")
    
    dados = interpretar_tarefa(comando)
    if not dados:
        raise HTTPException(status_code=422, detail="A IA não conseguiu interpretar o comando")
    
    task = Task(
        description=dados.get("descricao", "Tarefa sem descrição"),
        data=dados.get("data"),
        hora=dados.get("hora")  
    )

    tasks = load_tasks()
    tasks.append(task.dict())
    save_tasks(tasks)

    return {"message": "Tarefa adicionada com sucesso (via IA)!"}