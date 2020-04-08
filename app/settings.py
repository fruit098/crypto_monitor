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
POOLER_SLEEP = int(os.getenv("POOLER_SLEEP"))
