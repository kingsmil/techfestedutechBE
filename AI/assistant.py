import shelve
import requests
import os
from dotenv import load_dotenv
from openai import OpenAI
import time
import json
class OpenAIAssistant:
    def __init__(self, debug=False):
        # Load environment variables from .env file
        load_dotenv()
        self.OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
        self.client = OpenAI(api_key=self.OPEN_AI_API_KEY)
        self.ASSISTANT_ID = "asst_kIeZdHA64m2dPaBQDY0BCVI8"
        self.debug = debug

    def log(self, *messages):
        """Log messages if debugging is enabled."""
        if self.debug:
            print(' '.join(map(str, messages)))

    def run_assistant(self, thread):
        # Retrieve the Assistant
        assistant = self.client.beta.assistants.retrieve(self.ASSISTANT_ID)

        # Run the assistant
        run = self.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )

        # Wait for completion
        while run.status != "completed":
            # Be nice to the API
            time.sleep(0.5)
            run = self.client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

        # Retrieve the Messages
        messages = self.client.beta.threads.messages.list(thread_id=thread.id)
        new_message = messages.data[0].content[0].text.value
        self.log(new_message)
        return new_message

    def generate_response(self, message_body, wa_id, name):
        # Check if there is already a thread_id for the wa_id
        thread_id = self.check_if_thread_exists(wa_id)
        # If a thread doesn't exist, create one and store it
        if thread_id is None:
            thread = self.client.beta.threads.create()
            self.store_thread(wa_id, thread.id)
            thread_id = thread.id

        # Otherwise, retrieve the existing thread
        else:
            thread = self.client.beta.threads.retrieve(thread_id)

        # Add message to thread
        message = self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message_body,
        )

        # Run the assistant and get the new message
        new_message = self.run_assistant(thread)
        return new_message

    def check_if_thread_exists(self, wa_id):
        with shelve.open("threads_db") as threads_shelf:
            return threads_shelf.get(wa_id, None)

    def store_thread(self, wa_id, thread_id):
        with shelve.open("threads_db", writeback=True) as threads_shelf:
            threads_shelf[wa_id] = thread_id

    def extract_json(self,input_string):
        try:
            # Attempt to find the JSON start and end
            # This assumes the JSON object is enclosed in curly braces {}
            start_index = input_string.find('{')
            end_index = input_string.rfind('}') + 1

            # If start_index or end_index are not found, JSON is not present
            if start_index == -1 or end_index == -1:
                print("No JSON object found in the input string.")
                return None

            # Extract the JSON string from the input string
            json_str = input_string[start_index:end_index]

            # Parse the JSON string into a Python dictionary
            json_obj = json.loads(json_str)

            return json_obj
        except ValueError as e:
            print(f"Error parsing JSON: {e}")
            return None

# Example usage
assistant = OpenAIAssistant(debug=True)

new_message = assistant.generate_response("Generate 1:MH1100", "123", "Jun Hong")
print(new_message)
filtered_message = assistant.extract_json(new_message)

print("FINAL OUTPUT", filtered_message)