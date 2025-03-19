import time
import logging
import os
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv

# Configuração de logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ================== Funções para interação com o OpenAI Assistant ==================

def create_thread(client):
    """Cria uma nova thread e retorna o ID."""
    try:
        logging.info("Criando uma nova thread...")
        thread = client.beta.threads.create()
        logging.info(f"Thread {thread.id} criada com sucesso.")
        return thread.id
    except OpenAIError as e:
        logging.error(f"Erro ao criar a thread: {e}")
        return None


def add_message_to_thread(client,thread_id: str, content: str) -> str | None:
    """Adiciona uma mensagem na thread e retorna o ID da mensagem."""
    try:
        logging.info("Adicionando mensagem à thread...")
        mensagem = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=content
        )
        logging.info(f"Mensagem adicionada com sucesso, ID {mensagem.id}")
        return mensagem.id
    except OpenAIError as e:
        logging.error(f"Erro ao adicionar mensagem na thread {thread_id}: {e}")
        return None


def run_assistant(client,assisten_id: str, thread_id: str) -> str | None:
    """Executa o assistente na thread e retorna o ID da execução."""
    try:
        logging.info("Iniciando o assistente...")
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assisten_id
        )
        logging.info("Assistente iniciado. Aguardando resposta...")
        return run.id
    except OpenAIError as e:
        logging.error(f"Erro ao iniciar o assistente na thread {thread_id}: {e}")
        return None


def wait_for_run_completion(client,thread_id: str, run_id: str) -> bool:
    """Aguarda até que o assistente finalize a execução."""
    try:
        logging.info("Aguardando conclusão da execução do assistente...")
        while True:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.status == "completed":
                logging.info("Execução do assistente concluída.")
                return True
            time.sleep(1)
    except OpenAIError as e:
        logging.error(f"Erro ao aguardar execução na thread {thread_id}: {e}")
        return False


def get_assistant_response(client,thread_id: str) -> list[str] | None:
    """Obtém apenas as respostas do assistente após a última mensagem do usuário na thread."""
    try:
        logging.info(f"Obtendo respostas do assistente na thread {thread_id}...")

        messages = client.beta.threads.messages.list(thread_id=thread_id)
        messages = sorted(messages.data, key=lambda msg: msg.created_at)

        last_user_message_index = None
        for i in range(len(messages) - 1, -1, -1):  # Percorre de trás para frente
            if messages[i].role == "user":
                last_user_message_index = i
                break

        if last_user_message_index is None:
            return [msg.content[0].text.value for msg in messages if msg.role == "assistant"]

        assistant_messages = [
            msg.content[0].text.value for msg in messages[last_user_message_index + 1:] if msg.role == "assistant"
        ]

        if assistant_messages:
            logging.info(f"{len(assistant_messages)} respostas do assistente encontradas.")
            return assistant_messages
        else:
            logging.info("Nenhuma nova resposta do assistente encontrada.")
            return None
    except OpenAIError as e:
        logging.error(f"Erro ao obter resposta da thread {thread_id}: {e}")
        return None


def delete_thread(client,thread_id: str) -> None:
    """Deleta a thread."""
    try:
        logging.info(f"Deletando a thread {thread_id}...")
        client.beta.threads.delete(thread_id)
        logging.info("Thread deletada com sucesso.")
    except OpenAIError as e:
        logging.error(f"Erro ao deletar thread {thread_id}: {e}")


def processoGPT(api_key: str, assistant_id: str, prompts: list[str]) -> list[str]:
    """Executa o fluxo completo para processar as interações com o assistente."""
    respostas = []
    client = OpenAI(api_key=api_key)
    thread_id = create_thread(client)

    if not thread_id:
        logging.error("Falha ao criar thread. Processo abortado.")
        return []

    try:
        for i, prompt in enumerate(prompts):
            logging.info(f"\nProcessando prompt {i + 1}/{len(prompts)}...")

            message_id = add_message_to_thread(client,thread_id, prompt)
            if not message_id:
                logging.warning(f"Falha ao adicionar mensagem na thread {thread_id}. Pulando...")
                continue

            run_id = run_assistant(client,assistant_id,thread_id)
            if not run_id:
                logging.warning(f"Falha ao iniciar assistente na thread {thread_id}. Pulando...")
                continue

            if wait_for_run_completion(client,thread_id, run_id):
                response = get_assistant_response(client,thread_id)
                if response:
                    respostas.extend(response)
    finally:
        delete_thread(client,thread_id)  # Garante que a thread será deletada mesmo em caso de erro.

    return respostas

# SOMENTE PARA TESTES
if __name__ == "__main__":
    load_dotenv()
    # Lê as credenciais do ambiente
    api = os.getenv("API_KEY")
    ASSISTANT_ID = os.getenv("ASSISTANT_ID")

    # Lista de prompts para testar
    prompts = [
        "quanto e 1+1",


    ]

    print("Executando teste do assistente...")
    respostas = processoGPT(api,ASSISTANT_ID, prompts)

    print("\n=== RESPOSTAS OBTIDAS ===")
    for i, resposta in enumerate(respostas):
        print(f"Resposta {i + 1}: {resposta}")

