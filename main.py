import json
from dotenv import load_dotenv
import os
from openai import OpenAI


load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    print("❌ Erro: A variavel OPENROUTER_API_KEY não foi econtrada no ambiente.")
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

    tasks = load_tasks()   # Carrega as tarefas que já existem
    tasks.append(task)     # Adiciona a nova
    save_tasks(tasks)      # Salva tudo de volta no arquivo
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

Extraia e retorne em JSON apenas o seguinte:
- descrição (texto da tarefa)
- data (no formato DD/MM/AAAA, se houver)
- hora (no formato HH:MM, se houver)

Exemplo de resposta:
{{"descricao": "...", "data": "...", "hora": "..."}}
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
    except json.JSONDecodeError:
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

def menu():
    while True:
        print("\n=== Assistente de Tarefas ===")
        print("1 - Adicionar Tarefa")
        print("2 - Listar Tarefas")
        print("3 - Marcar/Remover Tarefa")
        print("4 - Adicionar por IA") # <-- nova opção
        print("5 - Sair")
        
        option = input("Escolha um opção:")
        
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
    menu()
