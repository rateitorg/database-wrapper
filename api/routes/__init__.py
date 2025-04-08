from flask import Blueprint
from api.routes.user_routes import user_bp
from api.routes.dev_routes import dev_bp

#create a blueprint with all api functions in it for easy exporting
user_bp = Blueprint('api', __name__)

#register individual blueprints
user_bp.register(user_bp, url_prefix="/users")


dev_bp = Blueprint('api', __name__)

#register individual blueprints
dev_bp.register(dev_bp, url_prefix="/dev")