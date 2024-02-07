import os
import sys
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

from flask_restx import Resource, Namespace

namespace = Namespace("echo")

@namespace.route("/<string:echo>")
class Echo(Resource):
    def get(self, echo):
        return echo