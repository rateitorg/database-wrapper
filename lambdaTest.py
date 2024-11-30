from neo4j import GraphDatabase
from dotenv import load_dotenv
from flask import Flask, request, jsonify

import os

#run a query
def runQuery(query, parameters):
    with driver.session() as session:
        return session.run(query, parameters)

# initilise the flask instance
def initFlask():
    global app
    app = Flask = (__name__)

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


#  initilise the environment
def initEnvironment():
    initDatabaseConnection()
    initFlask()
    

if __name__ == "__main__":
    initEnvironment()


