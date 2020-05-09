import logging
import json
import requests

from . import settings

log = logging.getLogger(__name__)

class RequestWrapper:
    @staticmethod
    def _request_node(method, params=[]):
        log.info("_request_node")
        try:
            response = requests.post(
                    "http://147.229.14.116:39999/bitcoin_rpc",
                data=json.dumps({"method":method, "params":params}),
                auth=(settings.USER, settings.PASSWORD),
            )
            parsed_response = response.json()
            result = parsed_response["result"]
            if parsed_response["error"]:
                log.info(f"_request_node.error_from_node {parsed_response['error']}")
            else:
                log.info("_request_node.response_from_node_ok")
        except Exception:
            log.exception("_request_node")
            result = []
        return result

    @staticmethod
    def fetch_addresses():
        return RequestWrapper._request_node("getnodeaddresses", [2500,])

    @staticmethod
    def post_new_peer(address):
        log.info(f"_request_node.post_new_peer.address-{address}")
        payload = {
            "method": "addnode",
            "params": [
                address,
                "onetry",
            ],
        }
        RequestWrapper._request_node(**payload)

    @staticmethod
    def fetch_active_peers():
        log.info("_request_node.fetch_active_peers")
        return RequestWrapper._request_node(method="getpeerinfo")
