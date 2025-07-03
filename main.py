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
        
def add_task(task):
    description = input("Digite a descrição da tarefa: ")
    tasks = {"description": description}
    
    tasks = load_tasks()    # Carrega as tarefas que já existem
    tasks.append(tasks)     # Adiciona a nova
    
    save_tasks()            # Salva tudo de volta no arquivo
    
    print("✅ Tarefa adicionada com sucesso!")
    

add_task()

def menu():
    while True:
        print("\n=== Assistente de Tarefas ===")
        print("1 - Adicionar Tarefa")
        print("2 - Listar Tarefas")
        print("3 - Sair")
        
        option = input("Escolha um opção:")
        
        if option == '1':
            add_task()
        elif option == '2':
            list_tasks()
        elif option == '3':
            print("👋 Até mais!")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")
            
            
if __name__ == "__main__":
    menu()
    
    
def list_tasks():
    tasks = load_tasks()
    
    if not tasks:
        print("📭 Nenhuma tarefa encontrada.")
        return

    print("📝 Suas Tarefas:")
    for i, task in enumerate(tasks, 1):
        print(f" {i} - {task['description']}")