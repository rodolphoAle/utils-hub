import time
import logging
import os
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def create_thread(client):
    """Create a new thread."""
    try:
        logging.info("Creating a new thread...")
        thread = client.beta.threads.create()
        logging.info(f"Thread {thread.id} created successfully.")
        return thread.id
    except OpenAIError as e:
        logging.error(f"Error creating thread: {e}")
        return None


def add_message(client, thread_id, content):
    """Add a message to the thread."""
    try:
        logging.info("Adding message to thread...")
        message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=content
        )
        logging.info(f"Message {message.id} added successfully.")
        return message.id
    except OpenAIError as e:
        logging.error(f"Error adding message to thread {thread_id}: {e}")
        return None


def run_assistant(client, assistant_id, thread_id):
    """Run the assistant on the thread."""
    try:
        logging.info("Starting assistant...")
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )
        logging.info("Assistant started. Waiting for response...")
        return run.id
    except OpenAIError as e:
        logging.error(f"Error starting assistant on thread {thread_id}: {e}")
        return None


def wait_for_completion(client, thread_id, run_id):
    """Wait until the assistant completes execution."""
    try:
        logging.info("Waiting for assistant completion...")
        while True:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.status == "completed":
                logging.info("Assistant execution completed.")
                return True
            time.sleep(1)
    except OpenAIError as e:
        logging.error(f"Error waiting for execution on thread {thread_id}: {e}")
        return False


def get_responses(client, thread_id):
    """Retrieve assistant responses."""
    try:
        logging.info(f"Fetching assistant responses from thread {thread_id}...")
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        messages = sorted(messages.data, key=lambda msg: msg.created_at)

        last_user_index = next((i for i in reversed(range(len(messages))) if messages[i].role == "user"), None)
        responses = [msg.content[0].text.value for msg in messages[last_user_index + 1:] if
                     msg.role == "assistant"] if last_user_index is not None else [msg.content[0].text.value for msg in
                                                                                   messages if msg.role == "assistant"]

        logging.info(f"{len(responses)} responses found.")
        return responses if responses else None
    except OpenAIError as e:
        logging.error(f"Error fetching responses from thread {thread_id}: {e}")
        return None


def delete_thread(client, thread_id):
    """Delete the thread."""
    try:
        logging.info(f"Deleting thread {thread_id}...")
        client.beta.threads.delete(thread_id)
        logging.info("Thread deleted successfully.")
    except OpenAIError as e:
        logging.error(f"Error deleting thread {thread_id}: {e}")


def process_gpt(api_key, assistant_id, prompts):
    """Run the full assistant process."""
    responses = []
    client = OpenAI(api_key=api_key)
    thread_id = create_thread(client)
    if not thread_id:
        logging.error("Thread creation failed. Aborting.")
        return []
    try:
        for i, prompt in enumerate(prompts):
            logging.info(f"Processing prompt {i + 1}/{len(prompts)}...")
            message_id = add_message(client, thread_id, prompt)
            if not message_id:
                logging.warning(f"Failed to add message to thread {thread_id}. Skipping...")
                continue
            run_id = run_assistant(client, assistant_id, thread_id)
            if not run_id:
                logging.warning(f"Failed to start assistant on thread {thread_id}. Skipping...")
                continue
            if wait_for_completion(client, thread_id, run_id):
                response = get_responses(client, thread_id)
                if response:
                    responses.extend(response)
    finally:
        delete_thread(client, thread_id)
    return responses

''' This session is only for teste'''
if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("API_KEY")
    assistant_id = os.getenv("ASSISTANT_ID")
    prompts = ["1+1?"]
    print("Running assistant test...")
    responses = process_gpt(api_key, assistant_id, prompts)
    print("\n=== ASSISTANT RESPONSES ===")
    for i, response in enumerate(responses):
        print(f"Response {i + 1}: {response}")
