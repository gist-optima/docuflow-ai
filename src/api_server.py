from flask import Flask
from flask_restx import Api

app = Flask(__name__)
api = Api(app)

from container_generator.container_generator import namespace as container_generator_namespace
from query_regenerator.query_regenerator import namespace as query_regenerator_namespace
from google_search.google_search import namespace as google_search_namespace
from snippet_extractor.snippet_extractor import namespace as snippet_extractor_namespace

api.add_namespace(container_generator_namespace)
api.add_namespace(query_regenerator_namespace)
api.add_namespace(google_search_namespace)
api.add_namespace(snippet_extractor_namespace)

if __name__ == "__main__":
    app.run(debug=True, host="localhost")