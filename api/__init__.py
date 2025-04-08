#the gateway to run the whole project.

from flask import Flask
from routes.user_routes import user_bp
from routes.dev_routes import dev_bp
from models.user_models import initDatabaseConnection


#initilise all needed for app
def create_app():
    app = Flask(__name__)

    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(dev_bp, url_prefix="/dev")

    with app.app_context():
        initDatabaseConnection(app)
        initiliseDailyData(app)

    return app

def initiliseDailyData(app):
    #Init the daily data
    app.config['TODAYSTOPIC'] = {} #default initially
    app.config['ALLDAILYTOPICS'] = [{}] #all previous topics.
    
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
