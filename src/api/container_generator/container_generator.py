from flask_restx import Resource, Namespace
import threading
import json
from api.container_generator.container_validator import validate_container_structure
from utils.gpt import GPT
import os
import sys
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)


current_directory = BASE_PATH + "/container_generator"

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
        example["input"] = json.dumps(
            example["input"], ensure_ascii=False, indent=4)
        example["output"] = json.dumps(
            example["output"], ensure_ascii=False, indent=4)

namespace = Namespace("container-generator")


@namespace.route("/<string:title>")
class ContainerGenerator(Resource):
    def get(self, title):
        templates = []

        def generate_templates():
            gpt = GPT(prompt, fewshot_examples)
            templates.append(
                gpt.get_response(title)
            )

        n = 3
        threads = []
        for i in range(n):
            thread = threading.Thread(target=generate_templates, args=[])
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

        templates = list(
            filter(lambda template: validate_container_structure(template), templates))
        return templates
# %%
