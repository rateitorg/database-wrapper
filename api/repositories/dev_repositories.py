from utils.Constants import *
from models.user_models import handleQuery
from utils.Constants import AREATOPICNAME, AREATOPICIMAGE

def add_topic(name: str, image: str, relatedTo: list[str]):
    # add a topic to the database
    
    topicsToLink = []
    matchQuery = []
    createQuery = []
    finalQuery = []

    #match topics related and save them as their name.
    for i in range(0, len(relatedTo)):
        topic = relatedTo[i]
        if i == 0: #start of query needs to have a match statement
            matchQuery.append("MATCH (" + topic + ":TOPIC {" + AREATOPICNAME + ": " + "'" + topic + "'" + "})")
        else:
            matchQuery.append("(" + topic + ":TOPIC {" + AREATOPICNAME + ": " + "'" + topic + "'" + "})")
        topicsToLink.append(topic)

    #add with statement to bring topics into the create statement
    finalQuery.append(", ".join(matchQuery))
    finalQuery.append("WITH " + ", ".join(topicsToLink) + " ")

    #start the create statements
    createQuery.append("CREATE (" + name + ":TOPIC {" + AREATOPICNAME + ": " + "'" + name + "'" + ", " + AREATOPICIMAGE + ": " + "'" + image + "'" + "})")

    #add a relationship for each topic relatedTo
    for topic in relatedTo:
        createQuery.append("(" + name + ")-[:RELATED_TO]->(" + topic + ")")
    
    finalQuery.append(", ".join(createQuery)) #add craete query to final satement
    toRun = "".join(finalQuery) #combine all queries into one

    ERRORMESSAGE = "ERROR: Failed to add topic to database"
    return handleQuery(toRun, {}, ERRORMESSAGE, is_write=True)

"""

    # add a topic to the database
    QUERY = "CREATE "

    QUERY = "CREATE (" + name + ":TOPIC {" + AREATOPICNAME + ": " + "'" + name + "'" + ", " + AREATOPICIMAGE + ": " + "'" + image + "'" + "})"
    
    queries = [QUERY]

    #add a relationship for each topic relatedTo
    for topic in relatedTo:
        queries.append("CREATE (" + topic + ")-[:RELATED_TO]->(" + name + ")")
    
    # join all queries bc multiple creates makes neo4j throw up
    finalQuery = "; ".join(queries)

    ERRORMESSAGE = "ERROR: Failed to add topic to database"
    return handleQuery(finalQuery, {}, ERRORMESSAGE, is_write=True)
"""