"address_puller.py - fetch addresses from nodes and publish them to Kafka and database"
import time
import logging
from datetime import datetime

from prometheus_client import Counter, start_http_server

from app import settings
from app.database import transactions
from app.request_wrapper import RequestWrapper
from app.kafka_wrapper import Producer

log = logging.getLogger(__name__)
same_addresses_metric = Counter("address_pooler_same_addresses_found", "Same addresses", ["node"])
new_addresses_metric = Counter("address_pooler_new_addresses_found", "New addresses", ["node"])


def address_puller(producer, node):
    log.info("address_puller.start")
    addresses = RequestWrapper(node).fetch_addresses()
    for address in addresses:
        ip_attributes = {
            "ip": address["address"],
            "port": int(address["port"]),
            "last_seen": datetime.fromtimestamp(float(address["time"])),
        }
        ip = ip_attributes["ip"]
        port = ip_attributes["port"]
        is_ipv6 = ":" in ip
        address_for_consumer = f"[{ip}]:{port}" if is_ipv6 else f"{ip}:{port}"
        try:
            if not transactions.find_node_by_ip_and_port(
                ip_attributes["ip"], ip_attributes["port"]
            ):
                transactions.new_ip(ip_attributes)
                producer.post_message(address_for_consumer)
                new_addresses_metric.labels(node).inc()
            else:
                same_addresses_metric.labels(node).inc()
        except Exception:
            log.exception("address_puller")
    log.info("address_puller.sleep")


if __name__ == "__main__":
    start_http_server(8003)
    producer = Producer()
    log.info("address_puller.obtained_producer")
    while True:
        for node in settings.NODES:
            address_puller(producer, node)
        time.sleep(settings.PULLER_SLEEP)
