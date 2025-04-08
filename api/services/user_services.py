#Where data is procesed before sending or recieving it from modes


from utils.Constants import * #get all constants needed 
from repositories.user_repositories import * #get all the functions that run queries

#get specific data in a dict
def findData(key: str, request: dict):
    data = request.get(key)
    
    if data == None:
        return request #should be an error structure if failed to find data.
    

def addStatusCode(response):
    #add a status code to the response
    if "errormessage" in response:
        return response, 500
    else:
        return response, 200


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
    response = run_linkMessageWithUserAndChatroom(chatroomID, senderUsername, messagecontent, datetime)
    return addStatusCode(response)
    

#join a chatroom for a topic
#TODO: sort out joining chatroom in more detail, Think this is established as not in this db
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

    response = run_friend_user(sourceUser, destUser)
    return addStatusCode(response)

#get amount of downs on a topic
def get_downs_topic(request):
    inputtedData = request.json

    #get topic
    topic = findData(AREATOPICNAME, inputtedData)

    response =  run_get_votes(topic, "-[downs:DOWNS]->", "COUNT(downs)")
    return addStatusCode(response)


#get amount of likes on a topic
def get_ups_topic(request):
    inputtedData = request.json

    #get topic
    topic = findData(AREATOPICNAME, inputtedData)

    response =  run_get_votes(topic, "-[ups:UPS]->", "COUNT(ups)")
    return addStatusCode(response)

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
    response =  run_create_user_to_topic_relation("-[ups:UPS]->", user, topic)
    return addStatusCode(response)

#when a user votes down on a topic
def vote_downs_topic(request):
    topic, user = getUserVotingInformation(request)
    response =  run_create_user_to_topic_relation("-[downs:DOWNS]->", user, topic)
    return addStatusCode(response)

#for when a user scrolls past a topic without liking it
def vote_skip_topic(request):
    topic, user = getUserVotingInformation(request)
    response =  run_create_user_to_topic_relation("-[skips:SKIP]->", user, topic)
    return addStatusCode(response)

#makes a new user node
def make_new_user(request):
    inputtedData = request.json

    newUsername = findData(AREAUSERNAME, inputtedData)
    newEmail = findData(AREAEMAIL, inputtedData)
    response =  run_new_user(newUsername, newEmail)
    return addStatusCode(response)


#gets all data for a topic. Includes ups and downs counts.
def get_topic_data(request):
    inputtedData = request.json

    #get topic
    topic = findData(AREATOPICNAME, inputtedData)

    response = run_get_all_topic_data(topic)
    return addStatusCode(response)


#get all related topics for a given topic
def get_related_topics(request):
    inputtedData = request.json

    topicName = findData(AREATOPICNAME, inputtedData)

    response = run_get_related_topics(topicName)
    return addStatusCode(response)