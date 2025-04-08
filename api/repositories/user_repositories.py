#interacting with the database
#abstracts details of data storage


#some functions to help making queries.

from utils.Constants import *
from models.user_models import handleQuery


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


#get all topic data
#TODO: test
def run_get_all_topic_data():
    QUERY = "MATCH (topic:TOPIC) RETURN topic"
    ERRORMESSAGE = "failed to get all topic data"
    return handleQuery(QUERY, {}, ERRORMESSAGE)