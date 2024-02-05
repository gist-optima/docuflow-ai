import os
import sys
sys.path.append("..")
from src.utils.gpt import GPT
import json

import threading

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

namespace = Namespace("snippet-extractor")

@namespace.route("")
class snippet_extractor(Resource):
    def post(self):
        body = request.json
        if not "articles" in body:
            abort(400, f"articles should be provided as body object")
        articles = body["articles"]
        
        snippets = []
        threads = []
        for article in articles:
            thread = threading.Thread(
                target=lambda article: snippets.append(self.extract_snippet_from_article(article)), 
                args=[article, ]
            )
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        
        return snippets

    def extract_snippet_from_article(self, article):
        gpt = GPT(prompt, fewshot_examples)
        return gpt.get_response(article)

        