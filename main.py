from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS

from resources.processing import Processing


app = Flask(__name__)

api = Api(app, prefix="/_internal")

CORS(app)


class HealthCheck(Resource):
    def get(self):
        return {'status': 'UP'}


api.add_resource(HealthCheck, "/health", methods=["GET"])
api.add_resource(Processing, "/data/iot", methods=["POST"])


if __name__ == "__main__":
    app.run(debug=True, port=5005, host="0.0.0.0")
