import os
import sys
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

from utils.gpt import GPT
import json

import threading

from flask import request, abort
from flask_restx import Resource, Namespace

current_directory = BASE_PATH + "\\snippet_extractor"

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
    def __init__(self,*args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.gpt = GPT(prompt, fewshot_examples)
        
    def post(self):
        body = request.json
        keys = ["articles", "all contents", "focused container", "guiding vector", "shown snippets", "preffered snippet"]
        if not all(key in body for key in keys):
            abort(400, f"all keys: {keys} should be provided via body")
        articles = body["articles"]
        all_contents = body["all contents"]
        focused_container = body["focused container"]
        guiding_vector = body["guiding vector"]
        shown_snippets = body["shown snippets"]
        preffered_snippet = body["preffered snippet"]
        
        snippets = []
        threads = []
        context = {
            "all contents": all_contents, 
            "focused container": focused_container, 
            "guiding vector": guiding_vector, 
            "shown snppets": shown_snippets, 
            "preffered snippet": preffered_snippet
        }
        for article in articles:
            thread = threading.Thread(
                target=lambda article: snippets.append(
                    self.extract_snippet_from_article(context, article)
                    ), 
                args=[article, ]
            )
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        
        return snippets

    def extract_snippet_from_article(self, context, article):
        context["article"] = article
        return self.gpt.get_response(json.dumps(context, ensure_ascii=False, indent=4))["snippets"]

        