import time
import logging
from datetime import datetime

from prometheus_client import Counter, start_http_server

from app import settings
from app.database import transactions
from app.request_wrapper import RequestWrapper
from app.kafka_wrapper import Producer

log = logging.getLogger(__name__)
same_addresses_metric = Counter("address_pooler_same_addresses_found", "Same addresses")
new_addresses_metric = Counter("address_pooler_new_addresses_found", "New addresses")


def address_pooling():
    log.info("address_pooling.start")
    producer = Producer()
    log.info("address_pooling.obtained_producer")
    while True:
        addresses = RequestWrapper.fetch_addresses()
        for address in addresses:
            ip_attributes = {
                "ip": address["address"],
                "port": int(address["port"]),
                "last_seen": datetime.fromtimestamp(float(address["time"])),
            }
            ip = ip_attributes["ip"]
            port = ip_attributes["port"]
            is_ipv6 = ":" in ip
            address_for_consumer = f"[{ip}]]:{port}" if is_ipv6 else f"{ip}:{port}"
            try:
                if not transactions.find_node_by_ip_and_port(
                    ip_attributes["ip"], ip_attributes["port"]
                ):
                    transactions.new_ip(ip_attributes)
                    producer.post_message(address_for_consumer)
                    new_addresses_metric.inc()
                else:
                    same_addresses_metric.inc()
            except Exception:
                log.exception("address_pooling")
        log.info("address_pooling.sleep")
        time.sleep(settings.POOLER_SLEEP)


if __name__ == "__main__":
    start_http_server(8000)
    address_pooling()
