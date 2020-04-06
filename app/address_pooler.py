import json
import time
import logging
from datetime import datetime

import requests
from kafka import KafkaProducer

from app import settings
from app.database import SESSION, commit_session, models


def fetch_addresses():
    producer = KafkaProducer(
        value_serializer=lambda m: json.dumps(m).encode("utf-8")
    )
    payload = {"method": "getnodeaddresses", "params": [2500,]}
    while True:
        response = requests.post(
            "https://prod.zaujec.tech:8331",
            data=json.dumps(payload),
            auth=(settings.USER, settings.PASSWORD),
        )
        for address in response.json()["result"]:
            ip_attributes = {
                "ip": f"{address['address']}:{address['port']}",
                "last_seen": datetime.fromtimestamp(float(address["time"])),
            }
            try:
                ip = models.IP_Pool(**ip_attributes)
                SESSION.add(ip)
                commit_session(SESSION)
                producer.send(settings.TOPIC_NAME, address)
                print("address.published")
            except Exception as e:
                print("address.exception", e)
        time.sleep(2)


if __name__ == "__main__":
    fetch_addresses()
