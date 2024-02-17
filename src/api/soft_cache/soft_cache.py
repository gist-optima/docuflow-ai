import os
import sys
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

from utils.vector_DB import VectorDB

import json

# flask rest api
from flask_restx import Resource, Namespace
from flask import request

namespace = Namespace("soft-cache")

@namespace.route("")
class SearchVectorDB(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.db = VectorDB()
    
    def get(self):
        query = request.headers["query"]
        top_k = int(request.headers.get("top-k"))
        threshold = float(request.headers.get("threshold"))
        return self.db.search(query, top_k, threshold)
    
    def post(self):
        texts = request.json
        self.db.add(texts)
        return None
