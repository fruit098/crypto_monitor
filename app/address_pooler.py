"""address_pooler - fetching addresses every 2 minutes """
import json
import time

import requests
from kafka import KafkaProducer

from app import settings


def fetch_addresses():
    producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode("utf-8"))
    payload = {"method": "getnodeaddresses", "params": [2500,]}
    while True:
        try:
            response = requests.post(
                "https://prod.zaujec.tech:8331",
                data=json.dumps(payload),
                auth=(settings.USER, settings.PASSWORD),
            )
            for address in response.json()["result"]:
                producer.send("Bitcoin", address)
                print("address.published")
            print("fetch_succesfull")
        except Exception as e:
            print("fetch_failed: ", e)
        time.sleep(2)


if __name__ == "__main__":
    fetch_addresses()
