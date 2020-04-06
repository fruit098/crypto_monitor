import time
import logging
from datetime import datetime

from app import settings
from app.database import transactions
from app.request_wrapper import RequestWrapper
from app.kafka_wrapper import Producer

log = logging.getLogger(__name__)

def address_pooling():
    producer = Producer()
    while True:
        addresses = RequestWrapper.fetch_addresses()
        for address in addresses:
            ip_attributes = {
                "ip": f"{address['address']}:{address['port']}",
                "last_seen": datetime.fromtimestamp(float(address["time"])),
            }
            try:
                transactions.new_ip(ip_attributes)
                producer.post_message(f"address['address']:address['port']")
            except Exception:
                log.warning("address_pooling")
        time.sleep(2)


if __name__ == "__main__":
    address_pooling()
