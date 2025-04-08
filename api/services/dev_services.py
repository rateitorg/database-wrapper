from utils.Constants import * #get all constants needed 
from dotenv import load_dotenv
import repositories.dev_repositories as dev_r
import user_services as user_s
import api.utils.dailyData as d
import os

load_dotenv()

#adds a topic to the database 
def addTopic(request):
    inputtedData = request.json

    if(not checkValidPassword(request.json)):
        return {"error": "Invalid password."}


    topicName = user_s.findData(AREATOPICNAME, inputtedData)
    topicImage = user_s.findData(AREATOPICIMAGE, inputtedData)

    #get all topics related to this topic
    
    relatedTo = user_s.findData("relations", inputtedData)
    
    #add a topic to the database
    response = dev_r.add_topic(topicName, topicImage ,relatedTo)
    return response
    

#changes the topic of the day to a new one
def changeTodaysTopic(request):
    inputtedData = request.json

    if(not checkValidPassword(inputtedData)):
        return {"error": "Invalid password."}

    inputtedData = request.json
    topicName = user_s.findData(AREATOPICNAME, inputtedData)
    #set the new topic of the day
    d.changeTodaysTopic(topicName)


#checks if the password inputted is correct.
def checkValidPassword(inputtedData):
    password = user_s.findData("password", inputtedData)
  
    if password == os.getenv("DEVPASSWORD"): #if correct password
        return True
    else:
        return False

