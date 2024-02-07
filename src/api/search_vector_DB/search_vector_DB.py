import os
import sys
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

from utils.vector_DB import VectorDB

# flask rest api
from flask_restx import Resource, Namespace

namespace = Namespace("search-vector-DB")

@namespace.route("/<string:query>/<int:n>")
class SearchVectorDB(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.db = VectorDB()
    
    def get(self, query, n=5):
        result = self.db.search(query, top_k=n)
        return result