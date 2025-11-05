import os
import json
import uuid
from openai import OpenAI
from datetime import datetime

class LLMClient:
    def __init__(self):
        self.client = OpenAI(
            base_url=os.getenv("_OPENAI_BASE_URL"),
            api_key=os.getenv("_OPENAI_API_KEY"),
        )
        self.model_name = os.getenv("_MODEL_NAME")
        self.log_dir = "logs"
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def invoke(self, messages):
        request_id = str(uuid.uuid4())
        request_timestamp = datetime.utcnow().isoformat()

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            extra_body={"reasoning_split": True},
        )

        response_timestamp = datetime.utcnow().isoformat()

        self.log_interaction(request_id, request_timestamp, response_timestamp, messages, response)

        return response

    def log_interaction(self, request_id, request_timestamp, response_timestamp, messages, response):
        log_entry = {
            "request_id": request_id,
            "request_timestamp": request_timestamp,
            "response_timestamp": response_timestamp,
            "model_name": self.model_name,
            "request": {
                "messages": messages
            },
            "response": {
                "thinking": response.choices[0].message.reasoning_details[0]['text'],
                "text": response.choices[0].message.content
            }
        }
        
        log_file = os.path.join(self.log_dir, f"{request_id}.json")
        with open(log_file, "w") as f:
            json.dump(log_entry, f, indent=2)
        
        self.commit_log(log_file)
    
    def commit_log(self, log_file):
        os.system(f"git add {log_file}")
        os.system(f"git commit -m 'Log LLM interaction for {log_file}'")

