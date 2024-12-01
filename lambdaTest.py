from neo4j import GraphDatabase
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import json
import logging

import os

#initilise flask
app = Flask(__name__)

#initilise logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

#run a query
def runQuery(query, parameters):
    return driver.session().run(query, parameters)


# initilise the connection to the database
def initDatabaseConnection():
    global driver # the access to the database
    load_dotenv() # so we can get the data to connnect to the db

    # user data to connect
    URI = os.getenv("NEO4J_URI")
    USERNAME = os.getenv("NEO4J_USERNAME")
    PASSWORD = os.getenv("NEO4J_PASSWORD")

    # declare driver to connect to the database
    driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))


#get all data in the database
@app.route('/get-all-data', methods=['POST'])
def getAllData():
    data = request.json
    query = data.get("query")
    parameters = data.get("parameters", {})

    #get result. Throw error if fails
    try:
        result = runQuery(query, parameters)
        return jsonify([record.data() for record in result])
    except Exception as e:
        return jsonify({"error":str(e)}), 500





if __name__ == "__main__":
    initDatabaseConnection() #connect to the database
    app.run(debug=True)


