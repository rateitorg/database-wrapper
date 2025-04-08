#the gateway to run the whole project.

from flask import Flask
from api.routes import user_bp
from .models import initDatabaseConnection

#initilise all needed for app
def create_app():
    app = Flask(__name__)
    initDatabaseConnection()
    app.register_blueprint(user_bp)
    return app
    

