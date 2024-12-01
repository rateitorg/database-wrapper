from neo4j import GraphDatabase
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import logging

import os

#Sadly, we can only identify data based on inputted strings into the database.
#I.e if we wanted to get a user, we would have to input his name and the data area storing the name, so:
#{name: "Jake Brunning"}
#the below constants are that first clause, just in case we ever decide to change it for some reason

AREAUSERNAME = "name" #the area of the name property in the user node
AREATOPICNAME = "describes" #the area of the describes property in the user node



#initilise flask
app = Flask(__name__)

#initilise logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

#run a query. literally just sends the data to run to the database. needs to be a seperate function so driver is contained.
def runQuery(query, parameters):
    return driver.session().run(query, parameters)

#handle a query. Attempts to run and errors if not possible
def handleQuery(QUERY, PARAMETERS, ERRORMESSAGE):

    try:
        result = runQuery(QUERY, PARAMETERS) #run a query and its parameters
        return jsonify([record.data() for record in result]) #return the json form of the data
    except Exception as e:
        return jsonify({"error: " + ERRORMESSAGE:str(e)})


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


#below are functions to help with creating querys

#matches a user in the database
def matchAUser(username: str):
    return "(user:USER {" + AREAUSERNAME + ": " + "\"" +  username  + "\"" + "})"

#matches a topic in the database
def matchATopic(topicName: str):
    return "(topic:TOPIC {" + AREATOPICNAME + ": " +  "\"" + topicName + "\"" + "})"

#matches a ups relationship
def matchAUpsRelationship():
    return "-[ups:UPS]->"

#matches a downs relationship
def matchADownRelationship():
    return "-[downs:DOWNS]->"

#matches a skip relationshipss
def matchASkipRelationship():
    return "-[skip:SKIP]->"

def returnCountOfUps():
    return "RETURN COUNT(ups)"


#below is every way you can run a query currently

#setup the getting of votes
def setupGetVotes(request):
    inputtedData = request.json
    topicName = inputtedData.get(AREATOPICNAME)

    startQuery = "MATCH"
    pass

#get the upvote of a topic
@app.route('/get-votes/ups', methods=['POST'])
def getUpsTopic():
    pass

#get theh downvvotes of a topic
@app.route('/get-votes/downs', methods=['POST'])
def getDownsTopic():
    pass


#get ups of a topic
#REQUIRED INPUT {$AREATOPICNAME : "<the topics name>"}
@app.route('/get-votes', methods=['POST'])
def getUpsTopic():
    # get the topic name
    inputtedData = request.json
    topicName = inputtedData.get(AREATOPICNAME)

    # run the query
    QUERY = "MATCH (:USER)" + matchAUpsRelationship() + matchATopic(topicName) + " " + returnCountOfUps()
    return handleQuery(QUERY, {}, "get ups on " + topicName + " did not work.")
    
#setup the data to vote on a given messages
def voteOnTopicSetup(request, typeOfVote: str):
    # get the inputted username and topicname
    inputtedData = request.json
    topicName = inputtedData.get(AREATOPICNAME)
    userName = inputtedData.get(AREAUSERNAME)

    #format query
    QUERY = "MATCH " + matchAUser(userName) + "," + matchATopic(topicName) + " CREATE " + "(user)" + typeOfVote + "(topic)"

    #format error message
    ERRORMESSAGE = "Creating " + typeOfVote + " for user and topic: " + userName + ", " + topicName + " failed"

    #return data
    return QUERY, ERRORMESSAGE

#makes a inputted user vote on a topic.
#REQUIRED INPUT {$AREAUSERNAME : "username", $AREATOPICNAME}
@app.route('/vote-topic/ups', methods=['POST'])
def voteUpOnTopic():
    #setup and handle the query and error message
    QUERY, errorMessage = voteOnTopicSetup(request, matchAUpsRelationship())
    return handleQuery(QUERY, {}, errorMessage)


#downvote a given topic and username
#REQUIRED INPUT {$AREAUSERNAME : "username", $AREATOPICNAME}
@app.route('/vote-topic/downs', methods=['POST'])
def voteDownOnTopic():
    #setup and handle the query and error message
    QUERY, errorMessage = voteOnTopicSetup(request, matchADownRelationship())
    return handleQuery(QUERY, {}, errorMessage)

#skip a given topic and username
#REQUIRED INPUT {$AREAUSERNAME : "username", $AREATOPICNAME}
@app.route('/vote-topic/skip', methods=['POST'])
def voteSkipOnTopic():
    #setup and handle the query and error message
    QUERY, errorMessage = voteOnTopicSetup(request, matchASkipRelationship())
    return handleQuery(QUERY, {}, errorMessage)






#get all data in database
@app.route('/get-all-data', methods=['POST'])
def getAllData():
    QUERY = 'MATCH (n) RETURN n'
    return handleQuery(QUERY, {}, "get all data failed")


#run a custom query
@app.route('/run-custom-query', methods=['POST'])
def runCustomQuery():
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


