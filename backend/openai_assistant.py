from openai import OpenAI
import os
import time
from dotenv import load_dotenv
from catsapi_photos import handle_cat_request
import re

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

ASSISTANT_ID = os.getenv("ASSISTANT_ID")

def create_new_thread():
    print("Creating a new thread.")
    thread = client.beta.threads.create()
    print("New thread created with ID:", thread.id)
    return thread

def poll_for_response(thread_id, run_id):
    timeout = time.time() + 60 * 1
    print("Waiting for response from the assistant...")
    while True:
        if time.time() > timeout:
            print("Timeout: No response from the assistant.")
            return None
        time.sleep(1)
        try:
            run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run_status.status == 'completed':
                response_messages = client.beta.threads.messages.list(thread_id=thread_id)
                for message in response_messages.data:
                    if message.role == 'assistant':
                        print(f"Assistant's Response: {message.content[0].text.value}")
                        return message.content[0].text.value
            elif run_status.status in ['failed', 'cancelled']:
                print(f"Run {run_status.status}: No further responses expected.")
                return None
        except Exception as e:
            print(f"Error retrieving run or messages: {e}")
            return None
        
# def is_requesting_cat_image(user_message):

#     image_request_phrases = re.compile(r"(show|send|give|picture|photo).*cat", re.IGNORECASE)

#     meaning_phrases = re.compile(r"(what is the meaning of|define|definition of|explain).*cat", re.IGNORECASE)

#     if meaning_phrases.search(user_message):
#         return False
#     elif image_request_phrases.search(user_message):
#         return True
#     return False

def send_message(user_message):
    print("Sending user message:", user_message)

    if "cat" in user_message.lower():
        return handle_cat_request(user_message)

    thread = create_new_thread()

    print(f"Using Assistant ID: {ASSISTANT_ID}")
    print(f"Using Thread ID: {thread.id}")

    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID
    )

    print(f"Running message with Assistant ID: {ASSISTANT_ID} and Thread ID: {thread.id}")

    return poll_for_response(thread.id, run.id)




