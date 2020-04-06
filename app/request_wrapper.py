import logging
import json
import requests

from . import settings

log = logging.getLogger(__name__)

class RequestWrapper:
    @staticmethod
    def _request_node(method, params):
        log.info("_request_node")
        response = requests.post(
            "https://prod.zaujec.tech:8331",
            data=json.dumps({"method":method, "params":params}),
            auth=(settings.USER, settings.PASSWORD),
        )
        return response.json()["result"]

    @staticmethod
    def fetch_addresses():
        return RequestWrapper._request_node("getnodeaddresses", [2500,])

    @staticmethod
    def post_new_node(address):
        payload = {
            "method": "addnode",
            "params": [
                address,
                "onetry",
            ],
        }
        RequestWrapper._request_node(**payload)
