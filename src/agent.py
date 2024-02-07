import os
import sys
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

import subprocess
import time

from requests import request
from uuid import uuid4

from utils.gpt import GPT

print("Opening API server...")
server = subprocess.Popen(["python", BASE_PATH+"\\src\\api\\api_server.py"], shell=True)
print("Waiting for server to fully start...")
time.sleep(2)

try:
    random_string = uuid4()
    response = request("GET", "http://localhost:5000/echo/" + random_string)
    if random_string != response.text:
        raise ValueError("Echo not working!")
    
    agent = GPT(prompt="JSON", fewshot_examples=[])
finally:
    server.kill()
