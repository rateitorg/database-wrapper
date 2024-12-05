from flask import Blueprint
from api.routes.user_routes import user_bp

#create a blueprint with all api functions in it for easy exporting
api_bp = Blueprint('api', __name__)

#register individual blueprints
api_bp.register(user_bp, url_prefix="/users")
