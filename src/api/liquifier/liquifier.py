from flask_restx import Resource, Namespace, fields
from flask import request, abort
import json
from utils.gpt import GPT
import os
import sys
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)


current_directory = BASE_PATH + "/liquifier"

prompt_file_path = os.path.join(current_directory, "prompt.json")
# fewshot_examples_file_path = os.path.join(current_directory, "examples.json")

prompt = {}
with open(prompt_file_path, "r", encoding="UTF8") as f:
    prompt = json.load(f)
    prompt = prompt["content"]

# fewshot_examples = []
# with open(fewshot_examples_file_path, "r", encoding="UTF-8") as f:
#     fewshot_examples = json.load(f)
#     for example in fewshot_examples:
#         example["input"] = json.dumps(
#             example["input"], ensure_ascii=False, indent=4)
#         example["output"] = json.dumps(
#             example["output"], ensure_ascii=False, indent=4)

namespace = Namespace("liquifier")

gpt = GPT(prompt)

input_schema = namespace.model('Payload', {
    'snippets': fields.List(fields.List(fields.String, required=True, description="A sentence or semantic unit"), required=True, description="Array of arrays of sentences or semantic units making up the document"),
})

@namespace.route("")
class QueryRegenerator(Resource):
    @namespace.expect(input_schema)
    def post(self):
        body = request.json

        global gpt
        message = json.dumps(body, ensure_ascii=False, indent=4)
        response = gpt.get_response(message, confinement=False)
        return response