import logging
import json
import requests

from . import settings

log = logging.getLogger(__name__)

class RequestWrapper:
    def __init__(self, rpc_address):
        self.rpc_address = rpc_address

    def _request_node(self, method, params=[]):
        log.info("_request_node")
        try:
            response = requests.post(
                self.rpc_address,
                data=json.dumps({"method": method, "params": params}),
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

    def fetch_addresses(self):
        return self._request_node("getnodeaddresses", [2500,])

    def post_new_peer(self, address):
        log.info(f"_request_node.post_new_peer.address-{address}")
        payload = {
            "method": "addnode",
            "params": [
                address,
                "onetry",
            ],
        }
        self._request_node(**payload)

    def fetch_active_peers(self):
        log.info("_request_node.fetch_active_peers")
        return self._request_node(method="getpeerinfo")
