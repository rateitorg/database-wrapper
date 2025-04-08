from utils.Constants import *
from models.user_models import handleQuery
from utils.Constants import AREATOPICNAME, AREATOPICDESCRIPTION

def add_topic(name: str, description: str, image: str, relatedTo: list[str]):
    # add a topic to the database
    QUERY = "CREATE (" + name + ":TOPIC {" + AREATOPICNAME + ": " + "\"" + name + "\"" + ", " + AREATOPICIMAGE + ": " + "\"" + image + "\"" + "});"
    
    #add a relationship for each topic relatedTo
    for topic in relatedTo:
        QUERY += "CREATE (" + topic + ")-[:RELATED_TO]->(" + name + ");"
    
    ERRORMESSAGE = "ERROR: Failed to add topic to database"
    return handleQuery(QUERY, {}, ERRORMESSAGE)