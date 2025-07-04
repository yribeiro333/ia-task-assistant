import json

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

    tasks = load_tasks()    # Carrega as tarefas que já existem
    tasks.append(task)     # Adiciona a nova
    
    save_tasks(tasks)            # Salva tudo de volta no arquivo
    
    print("✅ Tarefa adicionada com sucesso!")
    
def list_tasks():
    tasks = load_tasks()
    
    if not tasks:
        print("📭 Nenhuma tarefa encontrada.")
        return

    print("📝 Suas Tarefas:")
    for i, task in enumerate(tasks, 1):
        print(f" {i} - {task['description']}")

def menu():
    while True:
        print("\n=== Assistente de Tarefas ===")
        print("1 - Adicionar Tarefa")
        print("2 - Listar Tarefas")
        print("3 - Marcar/Remover Tarefa")
        print("4 - Sair")
        
        option = input("Escolha um opção:")
        
        if option == '1':
            add_task()
        elif option == '2':
            list_tasks()
        elif option == '3':
            update_or_remove_task()
        elif option == '4':
            print("👋 Até mais!")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")
            
            
if __name__ == "__main__":
    menu()
    
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