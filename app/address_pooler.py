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
                "ip": f"{address['address']}:{address['port']}",
                "last_seen": datetime.fromtimestamp(float(address["time"])),
            }
            ip_address = ip_attributes["ip"]
            try:
                if not transactions.find_ip(ip_address):
                    transactions.new_ip(ip_attributes)
                    producer.post_message(ip_attributes["ip"])
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
