"address_publisher.py - Takes addresses from Kafka and submit them to node"
from app import settings
from app.request_wrapper import RequestWrapper
from app.kafka_wrapper import Consumer

from prometheus_client import Gauge, Histogram, start_http_server

from queue import Queue
import logging
import threading
import time

log = logging.getLogger(__name__)
s = Histogram(f"address_publisher_processing_request_time", "Time of processing request", ["worker", "node"])
g = Gauge("address_publisher_queue_size", "Actual size of queue")


def worker(worker_number, queue):
    log.info(f"worker-{worker_number}.consumer_created")

    while True:
        for node in settings.NODE_TO_ACCEPT_CONNECTIONS:
            log.info(f"worker-{worker_number}.queue_size={queue.qsize()}")
            address = queue.get()
            log.info(f"worker-{worker_number}.got_message_from_queue")
            try:
                start_time = time.time()
                RequestWrapper(node).post_new_peer(address)
                request_time = time.time() - start_time
                s.labels(f"{worker_number}", node).observe(request_time)

            except Exception:
                log.exception("worker.address_posting_failed")

def fill_queue_worker(queue, consumer):
    while True:
        log.info("fill_queue_worker.start_filling")
        g.set(queue.qsize())
        for _ in range(settings.CHUNK_SIZE_FOR_CONSUMER):
            queue.put(consumer.get_message())
            log.info("fill_queue_worker.got_message_from_kafka")
        time.sleep(settings.PUBLISHER_SLEEP)

def main():
    log.info("main.creating_consumer")
    consumer = Consumer(group_id="same_group")
    log.info("main.obtained_consumer")

    threads = []
    queue = Queue()
    for n in range(settings.WORKERS):
        log.info(f"main.creating_worker_{n}")
        thread = threading.Thread(target=worker, args=[n, queue])
        threads.append(thread)
        thread.start()

    fill_queue_worker(queue, consumer)


if __name__ == "__main__":
    start_http_server(8001)
    main()
