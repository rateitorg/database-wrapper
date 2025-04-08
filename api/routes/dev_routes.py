#holds dev stuff for dealing with the database.
import api.utils.dailyData as d
import api.services.user_services as user_s
import api.services.dev_services as dev_s
from flask import Blueprint, request

dev_bp = Blueprint('dev', __name__) #the bp containing all the user api functions

#f
#TODO: way to safely access these routes

#adds a topic and creates a relation to each topic similar to it
#name; name of topic, description: description of topic, relatedTo: list of topic names similar to it. 
#Image is a string of the image url.
@dev_bp.route("/add-topic", methods=["POST"])
def addTopic():
    dev_s.addTopic(request)

#changes the topic of the day to a new one
#name: name of topic
@dev_bp.route("/change-daily-topic", methods=["POST"])
def changeTodaysTopic():
    dev_s.changeTodaysTopic(request)


if __name__ == "__main__":
    #shiiii
    pass