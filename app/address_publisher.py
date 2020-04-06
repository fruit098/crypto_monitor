import json
import requests
from kafka import KafkaConsumer

from app import settings
import logging
import multiprocessing

log = logging.getLogger(__name__)


def task(n):
    consumer = KafkaConsumer(
        settings.TOPIC_NAME,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="1",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )

    while True:
        log.info("consumer.created")
        message = next(consumer)
        try:
            log.info("task.sending_paylod")
            payload = {
                "method": "addnode",
                "params": [
                    f"{message.value['address']}:{message.value['port']}",
                    "onetry",
                ],
            }
            response = requests.post(
                "https://prod.zaujec.tech:8331",
                data=json.dumps(payload),
                auth=(settings.USER, settings.PASSWORD),
            )
            log.info("publisher.task_sent")
        except Exception:
            log.exception()


def main():
    processes = []
    for i in range(1, settings.TOPIC_PARTITIONS + 1):
        worker = multiprocessing.Process(target=task, args=[i,])
        processes.append(worker)
        worker.start()


if __name__ == "__main__":
    main()
