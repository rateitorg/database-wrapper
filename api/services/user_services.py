#Where data is procesed before sending or recieving it from modes


from api.models.user_models import *
from utils.Constants import * #get all constants needed 
#get specific data in a dict
def findData(key: str, request: dict):
    data = request.get(key)
    
    if data == None:
        return "Error: failed to find key : " + key + " in JSON input"
    
def get_all_data(request):
    run_get_all_data()

#get data for chatroomSendMessage
def chatroom_send_message(request):
    inputtedData = request.json

    #extract message data
    senderUsername = findData(AREAUSERNAME, inputtedData)
    chatroomID = findData(AREACHATID, inputtedData)
    datetime = findData(AREADATETIMESENT, inputtedData)
    messagecontent = findData(AREAMESSAGECONTENT, inputtedData)

    #run query
    return run_linkMessageWithUserAndChatroom(chatroomID, senderUsername, messagecontent, datetime)

#join a chatroom for a topic
#TODO: sort out joining chatroom in more detail
def join_chatroom(request):
    inputtedData = request.json

    #get username and chat id
    username = findData(AREAUSERNAME, inputtedData)
    chatroomId = findData(AREACHATID, inputtedData)
    topicName = findData(AREATOPICNAME, inputtedData)
    

#friend a user
def friend_user(request):
    inputtedData = request.json

    #get usernames of users to friend
    sourceUser = findData(AREAUSERNAME + "1" , inputtedData)
    destUser = findData(AREAUSERNAME + "2", inputtedData)

    run_friend_user(sourceUser, destUser)

#get amount of downs on a topic
def get_downs_topic(request):
    inputtedData = request.json

    #get topic
    topic = findData(AREATOPICNAME, inputtedData)

    run_get_votes(topic, "-[downs:DOWNS]->", "COUNT(downs)")

#get amount of likes on a topic
def get_ups_topic(request):
    inputtedData = request.json

    #get topic
    topic = findData(AREATOPICNAME, inputtedData)

    return run_get_votes(topic, "-[ups:UPS]->", "COUNT(ups)")

#helper to avoid repeating code on voting up and down
def getUserVotingInformation(request):
    inputtedData = request.json
    
    #get topic and user
    topic = findData(AREATOPICNAME, inputtedData)
    user = findData(AREAUSERNAME, inputtedData)

    return topic, user

#when a user votes up on a topic
def vote_ups_topic(request):
    topic, user = getUserVotingInformation(request)
    return run_create_user_to_topic_relation("-[ups:UPS]->", user, topic)

#when a user votes down on a topic
def vote_downs_topic(request):
    topic, user = getUserVotingInformation(request)
    return run_create_user_to_topic_relation("-[downs:DOWNS]->", user, topic)

#for when a user scrolls past a topic without liking it
def vote_skip_topic(request):
    topic, user = getUserVotingInformation(request)
    return run_create_user_to_topic_relation("-[skips:SKIP]->", user, topic)

#makes a new user node
def make_new_user(request):
    inputtedData = request.json

    newUsername = findData(AREAUSERNAME, inputtedData)
    newEmail = findData(AREAEMAIL, inputtedData)
    return run_new_user(newUsername, newEmail)


    