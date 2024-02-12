import os
import sys
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

from utils.gpt import GPT
import json
from flask import request, abort
from flask_restx import Resource, Namespace, fields

current_directory = BASE_PATH + "\\query_generator"

prompt_file_path = os.path.join(current_directory, "prompt.json")
fewshot_examples_file_path = os.path.join(current_directory, "examples.json")

prompt = {}
with open(prompt_file_path, "r", encoding="UTF-8") as f:
    prompt = json.load(f)
    prompt = prompt["content"]

fewshot_examples = []
with open(fewshot_examples_file_path, "r", encoding="UTF-8") as f:
    fewshot_examples = json.load(f)
    for example in fewshot_examples:
        example["input"] = json.dumps(example["input"], ensure_ascii=False, indent=4)
        example["output"] = json.dumps(example["output"], ensure_ascii=False, indent=4)

namespace = Namespace("query-generator")

gpt = GPT(prompt, fewshot_examples)

model=namespace.model('Payload',{
    'focused container': fields.String(required=True, description="보고서의 전체 내용 중 현재 사용자가 관심있는 부분"),
    'guiding vector': fields.String(required=True, description="사용자가 원하는 검색의 방향성") # guiding vector may not be required: todo
})

query_params=[]

@namespace.route('/')
class QueryGenerator(Resource):
    @namespace.expect(model)
    def post(self):
        body=request.json

        global gpt
        message = json.dumps(body, ensure_ascii=False)
        response = gpt.get_response(message)
        return {"query list": response["queries"]}
        
