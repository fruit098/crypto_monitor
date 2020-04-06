""""Settings"""
import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

USER = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
NODES = os.getenv("NODES").split(",")[:-1]
TOPIC_NAME = os.getenv("TOPIC_NAME")
TOPIC_PARTITIONS = int(os.getenv("TOPIC_PARTITIONS"))
