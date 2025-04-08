from utils.Constants import * #get all constants needed 
import repositories.dev_repositories as dev_r
import user_services as user_s
import api.utils.dailyData as d


def addTopic(request):
    inputtedData = request.json

    topicName = user_s.findData(AREATOPICNAME, inputtedData)
    topicImage = user_s.findData(AREATOPICIMAGE, inputtedData)

    #get all topics related to this topic
    
    relatedTo = user_s.findData("relations", inputtedData)
    
    #add a topic to the database
    response = dev_r.add_topic(topicName, topicImage ,relatedTo)
    return response
    

def changeTodaysTopic(request):
    inputtedData = request.json
    topicName = user_s.findData(AREATOPICNAME, inputtedData)
    #set the new topic of the day
    d.changeTodaysTopic(topicName)

