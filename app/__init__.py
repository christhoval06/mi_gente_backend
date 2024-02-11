from app.utils.db import get_conflicting_field
from flask import Flask, jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import import_string

extensions = [
    "app.models:db",
    "app.models:ma",
    # "app.admin:admin",
    "app.extension.cors:cors",
    # "app.extension.babel:babel",
    # "app.extension.sentry:sentry",
    # "app.extension.migrate:migrate",
    # "app.extension.session:session",
    # "app.extension.security:security",
]

blueprints = [
    "app.api:api",
]


def create_app():

    app = Flask(__name__)
    app.config.from_object("app.config.Config")
    
    for name in extensions:
        extension = import_string(name)
        extension.init_app(app)

    for name in blueprints:
        blueprint = import_string(name)
        app.register_blueprint(blueprint)

    return app

app = create_app()

@app.route("/")
def hello_world():
    return jsonify(hello="world")

@app.errorhandler(404)
@app.errorhandler(405)
def handle_api_error(err):
    return jsonify(error=str(err)), err.code if request.path.startswith('/api/') else err 
    
@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400

@app.errorhandler(IntegrityError)
def handle_db_integrity_error(err):
    field, value = get_conflicting_field(err)
    return jsonify(message= f'{field}={value} already exists', code=err.code), 400