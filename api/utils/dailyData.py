#stores data that can change daily.
from flask import jsonify, current_app
from utils import Constants



def changeTodaysTopic(newTopic):
    prevTopics = current_app.config['ALLDAILYTOPICS']
    prevTopics.append(current_app.config['TODAYSTOPIC']) #add the previous topic to the list

    current_app.config['TODAYSTOPIC'] = newTopic #set the new topic


def getTodaysTopic():
    todaysTopic = current_app.config['TODAYSTOPIC']
    return todaysTopic
