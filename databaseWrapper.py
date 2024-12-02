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
AREAEMAIL = "email" #the area of the email in the node


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

def returnCountOfDowns():
    return "RETURN COUNT(downs)"

#below is every way you can run a query currently

#join a chatroom
#REQUIRED INPUT : {$USERNAME : username, $TOPICNAME : topicName}
@app.route('/join-chatroom', methods=['POST'])
def joinChatroom():
    pass

#create a new user.
#REQUIRED INPUT : {$AREAUSERNAME: username, $AREAEMAIL: email
@app.route('/new-user', methods=['POST'])
def newUser():
    #get the users email and name
    inputtedData = request.json
    userName = inputtedData.get(AREAUSERNAME)
    email = inputtedData.get()

    #make the new user
    QUERY = "CREATE (" + userName + ":USER {" + AREAUSERNAME + ": " + "'" + userName + "'" +  ", " + AREAEMAIL + ": " + "'" + email + "'" + "})"
    ERRORMESSAGE = "Creating new user: " + userName + ", " + email + " failed."
    return handleQuery(QUERY, {}, ERRORMESSAGE)

#setup the getting of votes
def setupGetVotes(request, typeOfRelationship, typeOfCount):
    inputtedData = request.json
    topicName = inputtedData.get(AREATOPICNAME)

    QUERY = "MATCH (:USER)" + typeOfRelationship + matchATopic(topicName) + " " + typeOfCount
    ERRORMESSAGE = "getting " + typeOfRelationship + " for topic " + topicName + " failed."

    return QUERY, ERRORMESSAGE

#get the upvote of a topic
@app.route('/get-votes/ups', methods=['POST'])
def getUpsTopic():
    QUERY, ERRORMESSAGE = setupGetVotes(request, matchAUpsRelationship(), returnCountOfUps())
    return handleQuery(QUERY, {}, ERRORMESSAGE)

#get theh downvvotes of a topic
@app.route('/get-votes/downs', methods=['POST'])
def getDownsTopic():
    QUERY, ERRORMESSAGE = setupGetVotes(request, matchADownRelationship(), returnCountOfDowns())
    return handleQuery(QUERY, {}, ERRORMESSAGE)

    
#setup the data to vote on a given messages
def createUserToTopicRelation(request, typeOfRelationship: str):
    # get the inputted username and topicname
    inputtedData = request.json
    topicName = inputtedData.get(AREATOPICNAME)
    userName = inputtedData.get(AREAUSERNAME)

    #format query
    QUERY = "MATCH " + matchAUser(userName) + "," + matchATopic(topicName) + " CREATE " + "(user)" + typeOfRelationship + "(topic)"

    #format error message
    ERRORMESSAGE = "Creating " + typeOfRelationship + " for user and topic: " + userName + ", " + topicName + " failed."

    #return data
    return QUERY, ERRORMESSAGE

#makes a inputted user vote on a topic.
#REQUIRED INPUT {$AREAUSERNAME : "username", $AREATOPICNAME}
@app.route('/vote-topic/ups', methods=['POST'])
def voteUpOnTopic():
    #setup and handle the query and error message
    QUERY, errorMessage = createUserToTopicRelation(request, matchAUpsRelationship())
    return handleQuery(QUERY, {}, errorMessage)


#downvote a given topic and username
#REQUIRED INPUT {$AREAUSERNAME : "username", $AREATOPICNAME}
@app.route('/vote-topic/downs', methods=['POST'])
def voteDownOnTopic():
    #setup and handle the query and error message
    QUERY, errorMessage = createUserToTopicRelation(request, matchADownRelationship())
    return handleQuery(QUERY, {}, errorMessage)

#skip a given topic and username
#REQUIRED INPUT {$AREAUSERNAME : "username", $AREATOPICNAME}
@app.route('/vote-topic/skip', methods=['POST'])
def voteSkipOnTopic():
    #setup and handle the query and error message
    QUERY, errorMessage = createUserToTopicRelation(request, matchASkipRelationship())
    return handleQuery(QUERY, {}, errorMessage)


#get all data in database
@app.route('/get-all-data', methods=['POST'])
def getAllData():
    QUERY = 'MATCH (n) RETURN n'
    return handleQuery(QUERY, {}, "get all data failed")


#entry point
if __name__ == "__main__":
    initDatabaseConnection() #connect to the database
    app.run(debug=True)


