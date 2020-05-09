""""Settings"""
import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

USER = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
NODES = os.getenv("NODES").split(",")[:-1]
TOPICS = os.getenv("TOPIC_NAME").split(":")
DEFAULT_TOPIC = TOPICS[0]
WORKERS = int(os.getenv("WORKERS"))
PULLER_SLEEP = int(os.getenv("PULLER_SLEEP"))
PUBLISHER_SLEEP = 60
CHUNK_SIZE_FOR_CONSUMER = 2500
DB_URI = os.getenv("DB_URI")
NODE_TO_ACCEPT_CONNECTIONS = os.getenv("NODES_TO_ACCEPT_CONNECTIONS").split(",")[:-1]
KAFKA_SERVER=os.getenv("KAFKA_SERVER")
