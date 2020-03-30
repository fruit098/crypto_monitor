""""Settings"""
import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

USER = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
NODES = os.getenv("NODES").split(",")[:-1]
