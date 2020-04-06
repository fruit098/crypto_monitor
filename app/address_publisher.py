from app import settings
from app.request_wrapper import RequestWrapper
from app.kafka_wrapper import Consumer

import logging
import threading
import queue

log = logging.getLogger(__name__)

def worker(q):
    while True:
        log.info(f"worker.getting_message.queue_size={q.qsize()}")
        address = q.get()
        log.info("worker.got_message")
        try:
            RequestWrapper.post_new_node(address)
        except Exception:
            log.warning("worker.address_posting_failed")


def main():
    threads = []
    consumer = Consumer()
    q = queue.Queue(10000)
    for _ in range(1, settings.TOPIC_PARTITIONS + 1):
        thread = threading.Thread(target=worker, args=[q, ])
        threads.append(thread)
        thread.start()

    while True:
        try:
            address = consumer.get_message()
        except Exception:
            log.warning("main.error_getting_message")
            continue
        log.info(f"main.putting_message.queue_size={q.qsize()}")
        q.put(address)
        log.info("main.message_put")


if __name__ == "__main__":
    main()
