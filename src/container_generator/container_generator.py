import sys
sys.path.append("..")
from gpt import GPT
import json
from pprint import pprint
import threading

prompt = {}
with open("prompt.json", "r", encoding="UTF8") as f:
    prompt = json.load(f)
    prompt_params = prompt["params"]
    for (key, value) in prompt_params.items():
        prompt["content"] = prompt["content"].replace(f"<{key}/>", value)
    prompt = prompt["content"]

fewshot_examples = []
with open("examples.json", "r", encoding="UTF-8") as f:
    fewshot_examples = json.load(f)
    for example in fewshot_examples:
        example["input"] = json.dumps(example["input"], ensure_ascii=False, indent=4)
        example["output"] = json.dumps(example["output"], ensure_ascii=False, indent=4)

containers = []
def generate_containers():
    gpt = GPT(prompt, fewshot_examples)
    containers.append(
        gpt.get_response("KPMG 아이디어톤 계획서 - 아이디어톤을 통한 신사업 및 인재 발굴")
    )

n = 3
threads = []
for i in range(n):
    thread = threading.Thread(target=generate_containers, args=[])
    threads.append(thread)
    thread.start()
for thread in threads:
    thread.join()

# for container in containers:
#     pprint(container)

