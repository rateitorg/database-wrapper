from utils.Constants import * #get all constants needed 
from repositories.user_repositories import * #get all the functions that run queries
import repositories.dev_repositories as dev_r


def addTopic(name: str, description: str, image: str ,relatedTo: list[str]):
    #add a topic to the database
    response = dev_r.add_topic(name, description, image ,relatedTo)
    return response
    
