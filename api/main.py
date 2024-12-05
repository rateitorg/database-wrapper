#the gateway to run the whole project.

from flask import Flask
from api.routes import api_bp

#run the flask application
app = Flask(__name__)

#register master blueprint
app.register_blueprint(api_bp, url_prefix='/api')


#run app
if __name__ == "__main__":
    app.run(debug=True)