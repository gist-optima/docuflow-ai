from openai import OpenAI
import json
import os
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

class GPT:
    def __init__(self, prompt, fewshot_examples=[], model="gpt-3.5-turbo-1106"):
        self.model = model
        self.prompt = prompt
        self.fewshot_examples = fewshot_examples
        self.messages = [{"role": "system", "content": prompt}]
        for example in fewshot_examples:
            self.messages.append({"role": "user", "content": example["input"]})
            self.messages.append({"role": "assistant", "content": example["output"]})
        self.gpt = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.MAX_RETRY = 3
        self.response = ""

    def get_response(self, message):
        self.messages.append({"role": "user", "content": message})
        for i in range(self.MAX_RETRY):
            response = self.gpt.chat.completions.create(
                model=self.model,
                response_format={"type": "json_object"},
                messages=self.messages,
            )
            try:
                self.response = json.loads(response.choices[0].message.content)
            except:
                continue
            break
        else:
            return None
        return self.response
        