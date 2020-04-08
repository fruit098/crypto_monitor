from app import settings
from app.request_wrapper import RequestWrapper
from app.kafka_wrapper import Consumer

from prometheus_client import Histogram, start_http_server

import logging
import threading
import queue
import time

log = logging.getLogger(__name__)
s = Histogram(f"address_publisher_processing_request_time", "Time of processing request", ["worker"])


def worker(worker_number):
    consumer = Consumer(group_id='test')
    log.info(f"worker-{worker_number}.consumer_created")

    while True:
        log.info(f"worker-{worker_number}.getting_message")
        address = consumer.get_message()
        log.info(f"worker-{worker_number}.got_message")
        try:
            start_time = time.time()
            RequestWrapper.post_new_peer(address)
            request_time = time.time() - start_time
            s.labels(f"{worker_number}").observe(request_time)

        except Exception:
            log.exception("worker.address_posting_failed")


def main():
    threads = []
    for n in range(settings.WORKERS):
        thread = threading.Thread(target=worker, args=[n, ])
        threads.append(thread)
        thread.start()


if __name__ == "__main__":
    start_http_server(8001)
    main()
