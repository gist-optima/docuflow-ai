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
        top_k = request.headers.get("top-k")
        threshold = request.headers.get("threshold")
        top_k = int(top_k) if top_k else None
        threshold = float(threshold) if threshold else None
        params = {
            "query": query, 
            "top_k": top_k, 
            "threshold": threshold, 
        }
        params = dict((k, v) for k, v in params.items() if v is not None)
        return self.db.search(**params)
    
    def post(self):
        texts = request.json
        self.db.add(texts)
        return None
