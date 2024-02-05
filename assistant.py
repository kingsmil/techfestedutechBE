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
        self.ASSISTANT_ID = "asst_PxCjljoYHElWugm0rP1OVrH7"
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
            self.log(run.status,"polling api")
            if run.status == "failed":
                raise Exception(run)
            time.sleep(1)
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
        self.log("added message")
        # Add message to thread
        message = self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message_body,
        )
        self.log("running assistant")
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
            # Find the opening brace of the JSON object
            start_index = input_string.find('{')
            if start_index == -1:
                return None  # No JSON object found

            # Initialize counters for braces
            open_braces = 0
            for end_index in range(start_index, len(input_string)):
                if input_string[end_index] == '{':
                    open_braces += 1
                elif input_string[end_index] == '}':
                    open_braces -= 1

                # When open_braces reaches 0, we've found a matching closing brace
                if open_braces == 0:
                    # Attempt to parse the JSON from start_index to end_index+1
                    json_object = json.loads(input_string[start_index:end_index + 1])
                    return json_object  # Successfully parsed JSON

            return None  # No valid JSON object found or unmatched braces
        except json.JSONDecodeError as e:
            return None  # Return None if JSON is invalid
        except Exception as e:
            return None  # Return None if any other error occurs

# Example usage
# assistant = OpenAIAssistant(debug=True)
#
# new_message = assistant.generate_response("Generate 1:MH1100", "904", "Jun Hong")
# print(new_message)
# filtered_message = assistant.extract_json(new_message)
# print("FINAL OUTPUT", filtered_message)