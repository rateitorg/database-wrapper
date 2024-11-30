from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

#Intilise neo4j credentials. Constants from env file. Used to get information needed to connect to the database
URI: str
USERNAME:str
PASSWORD:str


def main():
    print("Hello world")

if __name__ == "__main__":
    load_dotenv()
    URI = os.getenv("NEO4J_URI")
    USERNAME = os.getenv("NEO4J_USERNAME")
    PASSWORD = os.getenv("NEO4J_PASSWORD")
    main()