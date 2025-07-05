import json
from dotenv import load_dotenv
import os
from openai import OpenAI
from datetime import datetime, timedelta
import threading
import subprocess
from plyer import notification
import time

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    print("❌ Erro: A variável OPENROUTER_API_KEY não foi encontrada no ambiente.")
    print("Por favor, crie um arquivo .env com sua chave da OpenRouter.")
    print("OPENROUTER_API_KEY=xxxxx")
    exit(1)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

def load_tasks():
    try:
        with open('tasks.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)

def add_task():
    description = input("Digite a descrição da tarefa: ")
    task = {
        "description": description,
        "done": False
    }

    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)
    print("✅ Tarefa adicionada com sucesso!")

def list_tasks():
    tasks = load_tasks()

    if not tasks:
        print("📭 Nenhuma tarefa encontrada.")
        return

    print("📝 Suas Tarefas:")
    for i, task in enumerate(tasks, 1):
        status = "✅" if task.get('done') else "❌"
        print(f"{i}. [{status}] {task['description']}")

def update_or_remove_task():
    tasks = load_tasks()

    if not tasks:
        print("📭 Nenhuma tarefa encontrada.")
        return

    print("\n📝 Tarefas:")
    for i, task in enumerate(tasks, 1):
        status = "✅" if task.get('done') else "❌"
        print(f"{i}. [{status}] {task['description']}")

    try:
        choice = int(input("Digite o número da tarefa que deseja alterar/remover: "))
        if choice < 1 or choice > len(tasks):
            print("Número inválido.")
            return
    except ValueError:
        print("Entrada inválida. Por favor, digite um número.")
        return

    task = tasks[choice - 1]

    action = input("Digite 'm' para marcar como feita, 'r' para remover: ").lower()
    if action == 'm':
        task['done'] = True
        print(f"✅ Tarefa '{task['description']}' marcada como feita.")
    elif action == 'r':
        tasks.pop(choice - 1)
        print("Tarefa removida com sucesso.")
    else:
        print("Ação inválida.")
        return

    save_tasks(tasks)

def interpret_command(command):
    prompt = f"""
Você é um assistente que ajuda a organizar tarefas.
A seguinte frase foi dita por um usuário: "{command}"

Extraia e retorne em JSON e os seguintes campos obrigatórios:
- descrição (texto da tarefa)
- data (no formato DD/MM/AAAA, ou "hoje", "amanhã", convertido para data real)
- hora (no formato HH:MM, se houver)

A data nunca deve ser omitida. Se o usuário disser "hoje" ou "amanhã", retorne a data real.
Exemplo de resposta:
{{"descricao": "...", "data": "04/07/2025", "hora": "14:30"}}
"""
    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    conteudo = response.choices[0].message.content

    try:
        dados = json.loads(conteudo)
        return dados
    except (ArithmeticError, json.JSONDecodeError):
        print("❌ A IA não conseguiu interpretar o comando corretamente.")
        print("🧪 Resposta bruta:", conteudo)
        return None

def add_task_ia():
    command = input("Descreva a tarefa com linguagem natural: ")
    dados = interpret_command(command)
    if not dados:
        return

    task = {
        "description": dados.get("descricao", "Tarefa sem descrição"),
        "done": False
    }

    if dados.get("data"):
        task["data"] = dados["data"]
    if dados.get("hora"):
        task["hora"] = dados["hora"]

    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)

    print("✅ Tarefa adicionada com sucesso (via IA)!")

    try:
        agendar_lembrete(task)
    except Exception as e:
        print("❌ Erro ao agendar lembrete.")
        print("→", e)

def mostrar_lembrete(task):
    print(f"\n Lembrete: {task['description']} agora ({task.get('data')} às {task.get('hora')})!\n")
    notification.notify(
        title='Lembrete de Tarefa',
        message=f"{task['description']} às {task.get('hora')}",
        timeout=10
    )

def tocar_som():
    os.system('aplay som.wav')

def agendar_lembrete(task):
    if "data" in task and "hora" in task:
        now = datetime.now()
        data_str = task["data"].lower()

        if data_str == "hoje":
            data_real = datetime.now().strftime("%d/%m/%Y")
        elif data_str == "amanhã" or data_str == "amanha":
            data_real = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
        else:
            data_real = data_str

        datahora = datetime.strptime(data_real + " " + task["hora"], "%d/%m/%Y %H:%M")
        if datahora > now:
            segundos = (datahora - now).total_seconds()
            threading.Timer(segundos, mostrar_lembrete, args=[task]).start()

def verificar_tarefas():
    tasks = load_tasks()
    for task in tasks:
        try:
            agendar_lembrete(task)
        except Exception as e:
            print(f"❌ Erro ao processar data/hora da tarefa: {task}")
            print("→", e)


def menu():
    while True:
        print("\n=== Assistente de Tarefas ===")
        print("1 - Adicionar Tarefa")
        print("2 - Listar Tarefas")
        print("3 - Marcar/Remover Tarefa")
        print("4 - Adicionar por IA")
        print("5 - Sair")

        option = input("Escolha uma opção: ")

        if option == '1':
            add_task()
        elif option == '2':
            list_tasks()
        elif option == '3':
            update_or_remove_task()
        elif option == '4':
            add_task_ia()
        elif option == '5':
            print("👋 Até mais!")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    threading.Thread(target=verificar_tarefas, daemon=True).start()
    menu()
