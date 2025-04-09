#handles database interactions

#import database info
from dotenv import load_dotenv
from neo4j import GraphDatabase
from flask import current_app, jsonify
from utils.Constants import *
import os

load_dotenv() # so we can get the data to connnect to the db
#---------------------------------------------------------------------------------------------------------------

# initilise the connection to the database
def initDatabaseConnection(app):
    # user data to connect
    URI = os.getenv("NEO4J_LOCALHOSTURI")
    USERNAME = os.getenv("NEO4J_USERNAME")
    PASSWORD = os.getenv("NEO4J_PASSWORD")
    #"12345678" or 12345678
    # declare driver to connect to the database
    driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
    app.config['NEO4J_DRIVER'] = driver # store the driver in the app config for later use


#get the driver in teh flask instance
def getDriver():
    driver = current_app.config.get('NEO4J_DRIVER')
    if driver is None: #if db not initilised
        raise Exception("Database connection not initialized.")
    return driver

#run a query. literally just sends the data to run to the database. needs to be a seperate function so driver is contained.
def runQuery(query, parameters, is_write=False):
    with getDriver().session() as session:
        result = session.run(query, parameters)
        if is_write:
            result.consume()
            return jsonify({"success": "write operation successful"})
        return list(result)

#handle a query. Attempts to run and errors if not possible
def handleQuery(QUERY, PARAMETERS, ERRORMESSAGE, is_write=False):
    try:
        result = runQuery(QUERY, PARAMETERS) #run a query and its parameters
        return  jsonify([record.data() for record in result]), 200 #return the json form of the data
    except Exception as e:
        return jsonify({"errormessage":ERRORMESSAGE, 
                        "query": QUERY, 
                        "fullerroroutput": str(e)}), 500 #return an error message if it fails
