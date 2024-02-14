# %%
import os
import sys
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

import subprocess
import time

from requests import request
from uuid import uuid4

from utils.gpt import GPT
import json

current_directory = BASE_PATH + "\\agent"

prompt_file_path = os.path.join(current_directory, "prompt.json")
fewshot_examples_file_path = os.path.join(current_directory, "examples.json")

prompt = {}
with open(prompt_file_path, "r", encoding="UTF8") as f:
    prompt = json.load(f)
    prompt_params = prompt["params"]
    for (key, value) in prompt_params.items():
        prompt["content"] = prompt["content"].replace(f"<{key}/>", value)
    prompt = prompt["content"]

fewshot_examples = []
with open(fewshot_examples_file_path, "r", encoding="UTF-8") as f:
    fewshot_examples = json.load(f)
    for example in fewshot_examples:
        example["input"] = json.dumps(example["input"], ensure_ascii=False, indent=4)
        example["output"] = json.dumps(example["output"], ensure_ascii=False, indent=4)

class Agent:
    def __init__(self, prompt, fewshot_examples=[]):
        self.gpt = GPT(prompt, fewshot_examples)

        print("Opening API server...")
        self.server = subprocess.Popen(["python", BASE_PATH+"\\api\\api_server.py"], shell=True)
        print("Waiting for the server to fully start...")
        time.sleep(5)

    def simulate(self):
        try: 
            self.gpt.get_response("")
            
        finally:
            self.server.kill()
# %%
agent = Agent(prompt, fewshot_examples)

# %%
