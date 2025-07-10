import os 
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)


def interpretar_tarefa(comando: str):
    prompt = f"""
    Você é um assistente que ajuda a organixar tarefas.
    A seguinte frase foi dita por um usuário: "{comando}"

    Extraia e retorne em JSON os seguintes campos obrigatórios:
    - descrição (texto da tarefa):
    - data (no formato DD/MM/AAAA, ou "hoje", "amanhã", convertido para data real)
    - hora (no formato HH:MM, se houver)

    Exemplo:
    {{"descrição": "Lavar a roupa", "data": "07/07/2025" "hoje", "hora": "14:00"}}
    """
    resposta = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    conteudo = resposta.choices[0].message.content
    try:
        dados = json.loads(conteudo)
        return dados
    except Exception as e:
        print("Erro ao interpretar IA", conteudo)
        return None