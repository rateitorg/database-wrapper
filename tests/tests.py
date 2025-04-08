#The database isnt live so can't fully test stuff but can write some functions
import pytest
from flask import Flask
from flask.testing import FlaskClient
from api.utils import Constants

#TODO: setup initilisng the flask app locally.

#initilise the flask app
def create_app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    client = app.test_client()
    return client
   


#test making a new user
def test_create_user(client: FlaskClient):
    dataToSend = {
        Constants.AREAUSERNAME : "testuser",
        Constants.AREAEMAIL : "testemail"
    }
    
    # Send a POST request to the endpoint
    response = client.post('/users/new-user', json=dataToSend)
    
    # Check if the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Check if the response data contains the expected values
    response_data = response.get_json()
    assert 'username' in response_data
    assert response_data['username'] == 'testuser'


#test failure to give wrapper correct parameters
def test_invalid_parameters_create_user(client: FlaskClient):
    dataToSend = {
        Constants.AREAUSERNAME : "testuser" #no password so should fail
    }
    
    # Send a POST request to the endpoint
    response = client.post('/users/new-user', json=dataToSend)
    
    # Check if the response status code is 400 (Bad Request)
    assert response.status_code == 400
    
    # Check if the response data contains the expected error message
    response_data = response.get_json()
    assert 'error' in response_data

#test getting a topic's upvotes
def test_get_topic_ups(client: FlaskClient):
    dataToSend = {
        Constants.AREATOPICNAME : "testtopic"
    }
    
    # Send a POST request to the endpoint
    response = client.post('/users/get-votes/ups', json=dataToSend)
    
    # Check if the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Check if the response data contains the expected values
    response_data = response.get_json()
    upsPresent: bool = 'ups' in response_data
    assert upsPresent

    if not upsPresent:
        return

    #we cant automatically check the acutal ups number (as if we had a way to do that we'd have confirmed correct working code).
    #so just output the number and manually check in the database if its correct.
    print("Number of ups for topic 'testtopic':", response_data['ups'])


#test getting a topic's downvotes
def test_get_topic_downs(client: FlaskClient):
    dataToSend = {
        Constants.AREATOPICNAME : "testtopic"
    }
    
    # Send a POST request to the endpoint
    response = client.post('/users/get-votes/downs', json=dataToSend)
    
    # Check if the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Check if the response data contains the expected values
    response_data = response.get_json()
    downsPresent: bool = 'downs' in response_data
    assert downsPresent

    if not downsPresent:
        return

    #we cant automatically check the acutal ups number (as if we had a way to do that we'd have confirmed correct working code).
    #so just output the number and manually check in the database if its correct.
    print("Number of downs for topic 'testtopic':", response_data['downs'])


#test a user voting on a topic
def test_user_vote_topic(client: FlaskClient):
    dataToSend = {
        Constants.AREAUSERNAME : "testuser",
        Constants.AREATOPICNAME : "testtopic"
    }
    
    # Send a POST request to the endpoint
    response = client.post('/users/vote-topic/ups', json=dataToSend)
    
    # Check if the response status code is 200 (OK)
    assert response.status_code == 200



