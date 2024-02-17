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
        query = request.args.get("query")
        top_k = request.args.get("top-k")
        threshold = request.args.get("threshold")
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
        json_data = request.json
        texts = [(id, text) for id, text in json_data.items()]
        self.db.add(texts)
        return None
