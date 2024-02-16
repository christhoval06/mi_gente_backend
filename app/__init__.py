from app.utils.db import get_conflicting_field
from flask import Flask, jsonify, request, json
from flask_cors import CORS
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import import_string

json.provider.DefaultJSONProvider.ensure_ascii = False

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
    # "app.api:api",
]

routers = [
    "app.router.people:init",
    "app.router.voting_place:init",
]



def create_app():

    App = Flask(__name__)
    App.config.from_object("app.config.Config")
    App.json = json.provider.DefaultJSONProvider(App)
    
    for name in extensions:
        extension = import_string(name)
        extension.init_app(App)

    for name in blueprints:
        blueprint = import_string(name)
        App.register_blueprint(blueprint)

    for name in routers:
        route = import_string(name)
        route(App)

    return App

app = create_app()

@app.route("/")
def info():
    return jsonify(version="v1.0.0", name="Mi Gente")

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