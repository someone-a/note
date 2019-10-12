from flask import Flask


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def hw():
        return "Hello World"
    return app
