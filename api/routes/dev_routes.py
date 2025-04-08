#holds dev stuff for dealing with the database.
import api.services.user_services as s #functions in services
import api.utils.dailyData as d
import api.utils.Constants as c
import api.services.user_services as user_s
import api.services.dev_services as dev_s

#TODO: way to safely access this code

#adds a topic and creates a relation to each topic similar to it
#name; name of topic, description: description of topic, relatedTo: list of topic names similar to it. 
def addTopic(name: str, description: str, relatedTo: list[str]):
    dev_s.addTopic(name, description, relatedTo)


def changeTodaysTopic(name: str):
    #get the topic data from the database
    data = user_s.get_topic_data(name)
    d.changeTodaysTopic(data)


if __name__ == "__main__":
    #run your desired dev functions here.
    pass