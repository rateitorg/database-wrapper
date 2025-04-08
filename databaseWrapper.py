from neo4j import GraphDatabase
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import logging
import json
import os

#Sadly, we can only identify data based on inputted strings into the database.
#I.e if we wanted to get a user, we would have to input his name and the data area storing the name, so:
#{name: "Jake Brunning"}
#the below constants are that first clause, just in case we ever decide to change it for some reason

AREAUSERNAME = "name" #the area of the name property in the user node
AREATOPICNAME = "describes" #the area of the describes property in the user node
AREAEMAIL = "email" #the area of the email in the node
AREACHATID = "chatroomID" # the area where the chatroom id is 

#areas for messagerelationships
AREAMESSAGECONTENT = "content"
AREADATETIMESENT = "datetime"

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
    URI = os.getenv("NEO4J_LOCALHOSTURI")
    USERNAME = os.getenv("NEO4J_USERNAME")
    PASSWORD = os.getenv("NEO4J_PASSWORD")

    # declare driver to connect to the database
    driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))


#below are functions to help with creating querys

#matches a user in the database
def matchAUser(username: str, varname: str):
    return "(user:USER {" + AREAUSERNAME + ": " + "\"" +  username  + "\"" + "})"

#matchs a chatroom based on chatID
def matchAChatroom(chatroomId: str, chatroomVar: str):
    return "(" + chatroomVar + ":CHATROOM {" + AREACHATID + ": " + "\"" + chatroomId + "\"" + "})"

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

#return a relationship. Varname is the name of the new variable and labelName is the name of the label
def matchRelationshipVar(varName: str, labelName: str) -> str:
    return "-[" + varName + ":" + labelName + "]->"


def returnCountOfUps():
    return returnCountVar("ups")

def returnCountOfDowns():
    return returnCountVar("downs")

#return the count of the var
def returnCountVar(input: str) -> str:
    return "RETURN COUNT(" + input + ")"


#creates a new chatroom
def createNewChatroomOnDatabase(topicName : str):
    pass


#return a link between a chatroom and a user, including message content and date time sent
def makeQueryChatroomUserRel(userVar: str, chatroomvar: str, messageContent: str, datetime: str):
    #(user)-[:MESSAGE {AreaOfMessageContent: messageContent, AreaOfDateTime, datetime}]->(chatroom)
    #messyness of below code comes from syntax requirements
    return "(" + userVar + ")-[:MESSAGE {" + AREAMESSAGECONTENT + ": " + "\"" + messageContent + "\", " + AREADATETIMESENT + ": datetime(" "\"" + datetime + "\")}]->(" + chatroomvar + ")"

#below is every way you can run a query currently

#store a message on the database
#TODO : TEST THIS FUNCTION
def linkMessageWithUserAndChatroom(chatroomId: str, username: str, messageContent: str, timeSent: str):
    #query needs to: match chatroom, match user, create a relationship which stores message content and time sent
    QUERY = "MATCH " + matchAUser(username, "user") + ", " + matchAChatroom(chatroomId, "chatroom") + " CREATE " + makeQueryChatroomUserRel("chatroom","user", messageContent, timeSent)
    ERRORMESSAGE = "Error, failed to link a message with a user : " + username + " and chatroomID " + chatroomId + " timesent: " + timeSent + " messageContent " + messageContent
    return handleQuery(QUERY, {}, ERRORMESSAGE)


#sends a message to a chatroom
#INPUTS : JSON {user: <username>, chatroomId: <chatroomID>, datetime: <datetime>, messagecontent: <messagecontent>}
#TODO : test
@app.route('/chatroom/sendmessage', methods=['POST'])
def chatroomSendMessage():
    inputtedData = request.json

    #extract message data
    senderUsername = request.get(AREAUSERNAME)
    chatroomID = request.get(AREACHATID)
    datetime = request.get(AREADATETIMESENT)
    messagecontent = request.get(AREAMESSAGECONTENT)
    
    return linkMessageWithUserAndChatroom(chatroomID, senderUsername, messagecontent, datetime)

#join a chatroom
#REQUIRED INPUT : {$USERNAME : username, $TOPICNAME : topicName}
@app.route('/chatroom/join', methods=['POST'])
def joinChatroom():
    pass


#friends one user and another.
#inputs: user1, user2
#TODO : TEST THIS FUNCTION
@app.route('/friend-user', methods=['POST'])
def friendUser():
    inputtedData = request.json
    userName1 = inputtedData.get(AREAUSERNAME + "1")
    userName2 = inputtedData.get(AREAUSERNAME + "2")

    #make query
    QUERY = "MATCH " + matchAUser(userName1, "user1") + ", " + matchAUser(userName2, "user2") + " CREATE (user1)" + matchRelationshipVar("", "FRIEND") + "(user2)"
    ERRORMESSAGE = "ERROR: Failed to make friend relationship between " + userName1 + " and " + userName2
 

#links a user with a pre existing chatroom
#inputs: chatroom id and user name
#TODO: TEST THIS FUNCTION
def linkUserWithChatroom(chatroomId: str, username: str):
    QUERY = "MATCH " + matchAUser(username, "user") + "," + matchAChatroom(chatroomId, "chatroom") + " CREATE " + "(user)" + matchRelationshipVar("partOf", "PARTOF") + "(chatroom)"
    ERRORMESSAGE = "failed to create link between user: " + username + " and chatroomID: " + chatroomId
    return handleQuery(QUERY, {}, ERRORMESSAGE)


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

#similarty should be a number between 0 and one 
def createTopicTopicRelatoin(topic1: str, topic2: str, similarity: str):
    num = int(similarity)
    #checks if the inputted similarity is valid
    if num > 1 or num < 0:
        print("ERROR: similarity needs to be between 0 and 1")
        return json.dump({"ERROR": "similarity needs to be between 0 or 1"})
    
    #makes query
    QUERY = "MATCH (topic1:TOPIC {describes: topic1}), (topic2:TOPIC {describes: topic2}) CREATE " + "(topic1)-[:SIMILARITY {magnitude: similarity}]->(topic2)"
    ERRORMESSAGE = "ERROR: failed to make topic to topic relation between: " + topic1 + ", " + topic2 + " with similarity " + str(similarity)
    #run query

    

#setup the data to vote on a given messages
def createUserToTopicRelation(request, typeOfRelationship: str):
    # get the inputted username and topicname
    inputtedData = request.json
    topicName = inputtedData.get(AREATOPICNAME)
    userName = inputtedData.get(AREAUSERNAME)

    #format query
    QUERY = "MATCH " + matchAUser(userName, "user") + "," + matchATopic(topicName) + " CREATE " + "(user)" + typeOfRelationship + "(topic)"

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