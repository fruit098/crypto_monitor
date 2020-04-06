import json
import kafka
import logging
from . import settings

log = logging.getLogger(__name__)

class Consumer:
    def __init__(self, topic=settings.DEFAULT_TOPIC, group_id=None):
        log.debug("consumer.init")
        self.consumer = kafka.KafkaConsumer(
            topic,
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            group_id=group_id,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        )
        log.debug("consumer.created")

    def get_message(self):
        log.info("consumer.get_message")
        return next(self.consumer)

class Producer:
    def __init__(self, topic=settings.DEFAULT_TOPIC):
        log.debug("producer.init")
        self.topic = topic
        self.producer = kafka.KafkaProducer(
            value_serializer=lambda m: json.dumps(m).encode("utf-8")
        )
        log.debug("producer.created")

    def post_message(self, message):
        log.info("producer.post_message")
        self.producer.send(self.topic, message)

