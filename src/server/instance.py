from flask import Flask
from flask_restx import Api
from environment.instance import environment_config
from flask_cors import CORS, cross_origin


class Server(object):
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app, supports_credentials=True)

        self.api = Api(
            self.app,
            version="1.0",
            title="Simple Business Loan Application System",
            description="Loan API",
            doc=environment_config["swagger-url"],
            default="LOAN",
        )

    def run(self):
        self.app.run(
            threaded=True,
            host="0.0.0.0",
            debug=environment_config["debug"],
            port=environment_config["port"],
        )


server = Server()
