#handles database interactions

#import database info
from dotenv import load_dotenv
from neo4j import GraphDatabase
from flask import jsonify
from utils.Constants import *
import os
#---------------------------------------------------------------------------------------------------------------

# initilise the connection to the database
def initDatabaseConnection():
    global driver # the access to the database
    load_dotenv() # so we can get the data to connnect to the db

    # user data to connect
    URI = os.getenv("NEO4J_LOCALHOSTURI")
    USERNAME = os.getenv("NEO4J_USERNAME")
    PASSWORD = os.getenv("NEO4J_PASSWORD")

    # declare driver to connect to the database
    driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

#run a query. literally just sends the data to run to the database. needs to be a seperate function so driver is contained.
def runQuery(query, parameters):
    return driver.session().run(query, parameters)

#handle a query. Attempts to run and errors if not possible
def handleQuery(QUERY, PARAMETERS, ERRORMESSAGE):
    try:
        result = runQuery(QUERY, PARAMETERS) #run a query and its parameters
        return jsonify([record.data() for record in result]) #return the json form of the data
    except Exception as e:
        return jsonify({"errormessage":ERRORMESSAGE, "query": QUERY, "fullerroroutput": str(e)}) #return an error message if it fails
