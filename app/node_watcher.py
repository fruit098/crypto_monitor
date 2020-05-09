import time
import json
import sys
import signal
import pdb

from prometheus_client import start_http_server, Gauge, Counter

import copy
import logging
from datetime import datetime
from .database import transactions
from . import utils, settings, peer_factory
from .request_wrapper import RequestWrapper

log = logging.getLogger(__name__)


active_peers_metric = Gauge("node_watcher_active_peers", "Count of active peers")
new_connection_metric = Counter(
    "node_watcher_new_connection", "Count of new connections"
)


class Watcher:
    def __init__(self, auth, nodes):
        self.nodes_to_watch = nodes
        self.auth = auth
        self.last_active_peers = set()

    def observe(self):
        all_peers_found = set()
        for node in self.nodes_to_watch:
            log.info("observe.loop")
            peers_per_node = Watcher.unify_found_peers(self.fetch_peers_from_node(node))
            all_peers_found.update(peers_per_node)
        self.compare_peers(all_peers_found)
        self.last_active_peers = all_peers_found

    @staticmethod
    def find_same_peers(peers):
        same_peers_groups = []
        for peer in peers:
            same_peers = [poor for poor in peers if poor == peer and poor is not peer]
            if len(same_peers) >= 2:
                same_peers_groups.append(same_peers)
            log.warning("find_same_peers.same_peers_found")
        return same_peers_groups

    def compare_peers(self, peers_to_compare):
        new_peers = peers_to_compare - self.last_active_peers
        non_active_peers = self.last_active_peers - peers_to_compare

        new_connection_metric.inc(len(new_peers))
        active_peers_metric.set(len(peers_to_compare))
        for new_peer in new_peers:
            transactions.create_new_peer_record(new_peer)
        self.save_inactive_peers(non_active_peers)

    def save_inactive_peers(self, peers):
        for peer in peers:
            transactions.save_peer_activity_record(peer)

    def find_new_and_active_peers(self, peers):
        new_peers = []
        active_peers = []
        for peer in peers:
            if peer not in self.last_active_peers:
                new_peers.append(peer)
            else:
                active_peers.append(peer)
        return new_peers, active_peers

    @staticmethod
    def unify_found_peers(peers):
        unified_peers = {peer_factory.create_peer(peer) for peer in peers}
        return unified_peers

    def fetch_peers_from_node(self, node):
        return RequestWrapper(node).fetch_active_peers()


def signal_handler(sig, frame):
    print("You pressed Ctrl+C!")
    print("Saving last active peers")
    watcher.save_inactive_peers(watcher.last_active_peers)
    sys.exit(0)


def main():
    while True:
        watcher.observe()
        time.sleep(1)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    start_http_server(8002)
    watcher = Watcher((settings.USER, settings.PASSWORD), settings.NODES)
    main()
