#contains the routes for user manipulation.
#anything which can be called while using the app is here

from flask import Blueprint, request, current_app
import utils.Constants as c
import utils.dailyData as d
import services.user_services as s



user_bp = Blueprint('users', __name__) #the bp containing all the user api functions

#gets every single node in the database
#Requires no input
#more for proof of concept than anything else
@user_bp.route('/get-all-data', methods=['POST'])
def get_all_data():
    return s.get_all_data(request)

#sends a message to a chatroom
#INPUTS : JSON {user: <username>, chatroomId: <chatroomID>, datetime: <datetime>, messagecontent: <messagecontent>}
#TODO : test
@user_bp.route('/chatroom/sendmessage', methods=['POST'])
def chatroomSendMessage():
    return s.chatroom_send_message(request)

#join a chatroom.
#REQUIRED INPUT : {$USERNAME : username, $TOPICNAME : topicName}
#connects a user to a chatroom node in the database via a relationship
#TODO: test
@user_bp.route('/join-chatroom', methods=['POST'])
def join_chatroom():
    return s.join_chatroom(request)

#friends one user and another.
#inputs: {user1: <username>, user2: <username>}
#TODO : TEST THIS FUNCTION
@user_bp.route('/friend-user', methods=['POST'])
def friend_user():
    return s.friend_user(request)

#get theh downvvotes of a topic
#REQUIRED INPUT: {TOPICAREA: <topicname>}
@user_bp.route('/get-votes/downs', methods=['POST'])
def getDownsTopic():
    return s.get_downs_topic(request)

#get the ups of a topic
##REQUIRED INPUT: {TOPICAREA: <topicname>}
@user_bp.route('/get-votes/ups', methods=['POST'])
def getUpsTopic():
    return s.get_ups_topic(request)

#makes a inputted user vote on a topic.
#REQUIRED INPUT {$AREAUSERNAME : "username", $AREATOPICNAME}
@user_bp.route('/vote-topic/ups', methods=['POST'])
def voteUpOnTopic():
    return s.vote_ups_topic(request)

#downvote a given topic and username
#REQUIRED INPUT {$AREAUSERNAME : "username", $AREATOPICNAME}
@user_bp.route('/vote-topic/downs', methods=['POST'])
def voteDownOnTopic():
    return s.vote_downs_topic(request)

#skip a given topic and username
#REQUIRED INPUT {$AREAUSERNAME : "username", $AREATOPICNAME}
@user_bp.route('/vote-topic/skip', methods=['POST'])
def voteSkipOnTopic():
    return s.vote_skip_topic(request)

#create a new user.
#REQUIRED INPUT : {$AREAUSERNAME: username, $AREAEMAIL: email}
@user_bp.route('/new-user', methods=['POST'])
def newUser():
    return s.make_new_user(request)


#gets whatever is saved as todays topic
@user_bp.route('/todays-topic', methods=['POST'])
def todays_topic():
    topicName = d.getTodaysTopic().get(c.AREATOPICNAME)
    return s.get_topic_data({c.AREATOPICNAME: topicName})


#get all related topic for a given topic
@user_bp.route('/get-related-topics', methods=['POST'])
def get_related_topics():
    return s.get_related_topics()


