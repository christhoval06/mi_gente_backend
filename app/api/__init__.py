from flask import Blueprint

from .people import people_router


api = Blueprint("api", __name__, url_prefix="/api")

api.register_blueprint(people_router)