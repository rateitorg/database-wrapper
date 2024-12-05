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
        return jsonify({"error: " + ERRORMESSAGE:str(e)})

#---------------------------------------------------------------------------------------------------------------------------------------------------------
#some functions to help making queries.

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


#return a link between a chatroom and a user, including message content and date time sent
def makeQueryChatroomUserRel(userVar: str, chatroomvar: str, messageContent: str, datetime: str):
    #(user)-[:MESSAGE {AreaOfMessageContent: messageContent, AreaOfDateTime, datetime}]->(chatroom)
    #messyness of below code comes from syntax requirements
    return "(" + userVar + ")-[:MESSAGE {" + AREAMESSAGECONTENT + ": " + "\"" + messageContent + "\", " + AREADATETIMESENT + ": datetime(" "\"" + datetime + "\")}]->(" + chatroomvar + ")"



#----------------------------------------------------------------------------------------------------------------------------------
#below is every way you can run a query currently

#friends one user with another.
def run_friend_user(userName1: str, userName2: str):
    QUERY = "MATCH " + matchAUser(userName1, "user1") + ", " + matchAUser(userName2, "user2") + " CREATE (user1)" + matchRelationshipVar("", "FRIEND") + "(user2)"
    ERRORMESSAGE = "ERROR: Failed to make friend relationship between " + userName1 + " and " + userName2
    return handleQuery(QUERY, {}, ERRORMESSAGE)

#links a user with a chatroom
def run_linkUserWithChatroom(chatroomId: str, username: str):
    QUERY = "MATCH " + matchAUser(username, "user") + "," + matchAChatroom(chatroomId, "chatroom") + " CREATE " + "(user)" + matchRelationshipVar("partOf", "PARTOF") + "(chatroom)"
    ERRORMESSAGE = "failed to create link between user: " + username + " and chatroomID: " + chatroomId
    return handleQuery(QUERY, {}, ERRORMESSAGE)

#makes a new user
def run_new_user(userName: str, email: str):
    QUERY = "CREATE (" + userName + ":USER {" + AREAUSERNAME + ": " + "'" + userName + "'" +  ", " + AREAEMAIL + ": " + "'" + email + "'" + "})"
    ERRORMESSAGE = "Creating new user: " + userName + ", " + email + " failed."
    return handleQuery(QUERY, {}, ERRORMESSAGE)

#gets the amount of votes a given topic has
def run_get_votes(topicName: str, typeOfRelationship: str, typeOfCount: str):
    QUERY = "MATCH (:USER)" + typeOfRelationship + matchATopic(topicName) + " " + typeOfCount
    ERRORMESSAGE = "getting " + typeOfRelationship + " for topic " + topicName + " failed."
    return handleQuery(QUERY, {}, ERRORMESSAGE)

#creattes a relation between a user and a topic. For voting on a topic
def run_create_user_to_topic_relation(typeOfRelationship: str, userName: str, topicName: str):
    QUERY = "MATCH " + matchAUser(userName, "user") + "," + matchATopic(topicName) + " CREATE " + "(user)" + typeOfRelationship
    ERRORMESSAGE = "Creating " + typeOfRelationship + " for user and topic: " + userName + ", " + topicName + " failed."
    return handleQuery(QUERY, {}, ERRORMESSAGE)

#gets all data in the database
def run_get_all_data():
    QUERY = "MATCH (n) RETURN n"
    ERRORMESSAGE = "failed to get all data"
    return handleQuery(QUERY, {}, ERRORMESSAGE)

#store a message on the database
#TODO : TEST THIS FUNCTION
def run_linkMessageWithUserAndChatroom(chatroomId: str, username: str, messageContent: str, timeSent: str):
    #query needs to: match chatroom, match user, create a relationship which stores message content and time sent
    QUERY = "MATCH " + matchAUser(username, "user") + ", " + matchAChatroom(chatroomId, "chatroom") + " CREATE " + makeQueryChatroomUserRel("chatroom","user", messageContent, timeSent)
    ERRORMESSAGE = "Error, failed to link a message with a user : " + username + " and chatroomID " + chatroomId + " timesent: " + timeSent + " messageContent " + messageContent
    return handleQuery(QUERY, {}, ERRORMESSAGE)