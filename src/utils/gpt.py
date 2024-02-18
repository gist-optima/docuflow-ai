from openai import AzureOpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()

class GPT:
    def __init__(self, prompt, fewshot_examples=[], model=os.getenv("AZURE_OPENAI_DEPLOYMENT_GPT")):
        self.model = model
        self.prompt = prompt
        self.fewshot_examples = fewshot_examples
        self.messages = [{"role": "system", "content": prompt}]
        for example in fewshot_examples:
            self.messages.append({"role": "user", "content": example["input"]})
            self.messages.append({"role": "assistant", "content": example["output"]})
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_KEY"), 
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"), 
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        self.MAX_RETRY = 1
        self.response = ""

    def get_response(self, message, confinement=True):
        self.messages.append({"role": "user", "content": message})

        for i in range(self.MAX_RETRY):
            if confinement: 
                response = self.client.chat.completions.create(
                    model=self.model,
                    response_format={"type": "json_object"},
                    messages=self.messages,
                )
            elif not confinement:
                response = self.client.chat.completions.create(
                    model=self.model,
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