from flask import Blueprint
from flask_cors import CORS

from .people import people_router


api = Blueprint("api", __name__, url_prefix="/api")
CORS(api)

api.register_blueprint(people_router)