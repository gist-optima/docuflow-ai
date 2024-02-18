import os
import sys
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

from flask import Flask
from flask_restx import Api

app = Flask(__name__)
api = Api(app)

from api.container_generator.container_generator import namespace as container_generator_namespace
from api.query_regenerator.query_regenerator import namespace as query_regenerator_namespace
from api.google_search.google_search import namespace as google_search_namespace
from api.snippet_extractor.snippet_extractor import namespace as snippet_extractor_namespace
from api.echo.echo import namespace as echo_namespace
from api.query_generator.query_generator import namespace as query_generator
from api.modulizer.modulizer import namespace as modulizer
from api.liquifier.liquifier import namespace as liquifier_namespace
from api.soft_cache.soft_cache import namespace as soft_cache_namespace

api.add_namespace(container_generator_namespace)
api.add_namespace(query_regenerator_namespace)
api.add_namespace(google_search_namespace)
api.add_namespace(snippet_extractor_namespace)
api.add_namespace(echo_namespace)
api.add_namespace(soft_cache_namespace)
api.add_namespace(query_generator)
api.add_namespace(modulizer)
api.add_namespace(liquifier_namespace)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")