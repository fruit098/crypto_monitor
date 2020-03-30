from gevent import monkey

monkey.patch_all()
import gevent
import json
import requests
from kafka import KafkaConsumer

user = ""
passwd = ""


def task(n, consumer):
    while True:
        print("getting ")
        message = next(consumer)
        print("got message")
        payload = {
            "method": "addnode",
            "params": [f"{message.value['address']}:{message.value['port']}", "onetry"],
        }
        response = requests.post(
            "https://prod.zaujec.tech:8331",
            data=json.dumps(payload),
            auth=(user, passwd),
        )
        print(f"Greenlet: {n} status_code: {response.status_code}")


def main():
    threads = []
    for i in range(50):
        cons = KafkaConsumer(
            "Bitcoin",
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        )
        threads.append(gevent.spawn(task, i, cons))

        gevent.joinall(threads)


if __name__ == "__main__":
    main()
