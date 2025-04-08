from flask import Blueprint

#create a blueprint with all api functions in it for easy exporting
user_bp = Blueprint('users', __name__)
dev_bp = Blueprint('dev', __name__)
