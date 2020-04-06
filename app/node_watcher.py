import time
import json
import sys
import signal

import requests

import copy
import logging
from datetime import datetime
from app import settings
from app.database import SESSION, commit_session, models

payload = {"method": "getpeerinfo", "params": []}
log = logging.getLogger(__name__)


class Watcher:
    def __init__(self, auth, nodes):
        self.nodes_to_watch = nodes
        self.auth = auth
        self.last_active_peers = []
        self.new_peers = {}

    def observe(self):
        all_peers_found = []
        for node in self.nodes_to_watch:
            peers_per_node = self.fetch_peers_from_node(node)
            all_peers_found += self.unify_found_peers(peers_per_node)
        self.compare_peers(all_peers_found)
        self.last_active_peers = all_peers_found

    def compare_peers(self, peers_to_compare):
        new_peers, active_peers = self.find_new_and_active_peers(
            peers_to_compare
        )
        non_active_peers = [
            peer
            for peer in self.last_active_peers
            if peer not in active_peers
        ]
        for new_peer in new_peers:
            self.create_new_peer_record(new_peer)
        self.save_inactive_peers(non_active_peers)

    def save_inactive_peers(self, peers):
        for peer in peers:
            self.save_peer_activity_record(peer)

    def save_peer_activity_record(self, peer):
        ip_record = (
            SESSION.query(models.IP_Pool)
            .filter(models.IP_Pool == peer["ip"])
            .one()
        )
        node = ip_record.node
        activity_record = {
            "start_of_activity": datetime.fromtimestamp(
                peer["start_of_activity"]
            ),
            "end_of_activity": datetime.now(),
        }
        node.active = False
        node.activities.append(activity_record)
        commit_session(SESSION)

    def find_new_and_active_peers(self, peers):
        new_peers = []
        active_peers = []
        for peer in peers:
            if peer not in self.last_active_peers:
                new_peers.append(peer)
            else:
                active_peers.append(peer)
        return new_peers, active_peers

    def create_new_peer_record(self, peer):
        ip_record = (
            SESSION.query(models.IP_Pool)
            .filter(models.IP_Pool == peer["ip"])
            .one()
        )
        if ip_record.node:
            log.warning(
                "create_new_peer_record.node_has_ip_record", ip=peer["ip"]
            )
            return
        node = models.Node(active=True, **peer)
        ip_record.node = node
        commit_session(SESSION)

    @staticmethod
    def unify_found_peers(peers):
        wanted_attributes = {
            "conntime": "start_of_activity",
            "addr": "ip",
            "version": "highest_protocol",
            "subver": "user_agent",
            "servicesnames": "services",
        }
        return [
            dict((wanted_attributes[k], peer[k]) for k in wanted_attributes)
            for peer in peers
        ]

    def fetch_peers_from_node(self, node):
        response = requests.post(
            node,
            data=json.dumps(payload),
            auth=(settings.USER, settings.PASSWORD),
        ).json()["result"]
        return response


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    print("Saving last active peers")
    watcher.save_inactive_peers(watcher.last_active_peers)
    sys.exit(0)

def main():
    while True:
        watcher.observe()
        time.sleep(1)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    watcher = Watcher((settings.USER, settings.PASSWORD), settings.NODES)
    main()
