import os
import sys
sys.path.append("..")
from gpt import GPT
import json
from flask import request, abort
from flask_restx import Resource, Namespace

current_directory = os.path.dirname(os.path.abspath(__file__))

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

namespace = Namespace("query-regenerator")

gpt = GPT(prompt, fewshot_examples)

@namespace.route("")
class QueryRegenerator(Resource):
    def post(self):
        body = request.json

        keys = ["all contents", "focused container", "guiding vector", "previous query", "shown snippets", "preffered snippet", "n"]
        if not all(key in body for key in keys):
            abort(400, f"all keys: {keys} should be provided via body")

        global gpt
        message = json.dumps(body, ensure_ascii=False)
        response = gpt.get_response(message)
        return response["queries"]
        
