from flask import Flask
from flask_restx import Api

app = Flask(__name__)
api = Api(app)

from container_generator.container_generator import namespace as container_generator_namespace

api.add_namespace(container_generator_namespace)

if __name__ == "__main__":
    app.run(debug=True, host="")