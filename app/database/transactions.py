import logging
from datetime import datetime

from . import SESSION, models, commit_session
from .. import utils

log = logging.getLogger(__name__)


def new_ip(ip_attributes):
    log.info("new_ip")
    ip = models.IP_Pool(**ip_attributes)
    log.debug("new_ip.created_model")
    SESSION.add(ip)
    commit_session(SESSION)


def save_peer_activity_record(peer):
    log.info("save_peer_activity_record")
    ip_record = _find_peer_ip(peer.ip)

    node = ip_record.node
    if not node:
        node = _create_peer(peer, ip_record)

    activity_record = {
        "start_of_activity": datetime.fromtimestamp(
            peer.start_of_activity
        ),
        "end_of_activity": datetime.now(),
    }
    node.active = False
    node.activities.append(models.NodeActivity(**activity_record))
    commit_session(SESSION)

def _find_peer_ip(ip):
    ip_record = (
        SESSION.query(models.IP_Pool)
        .filter(models.IP_Pool.ip == ip)
        .one_or_none()
    )
    if not ip_record:
        ip_record = models.IP_Pool(ip=ip)
        SESSION.add(ip_record)
    return ip_record


def _create_peer(peer, ip_record):
    include_keys = ["highest_protocol", "user_agent", "services"]
    node = models.Node(**utils.subset_dict(vars(peer), include_keys))
    ip_record.node = node
    return node


def create_new_peer_record(peer):
    log.info("create_new_peer_record")
    ip_record = _find_peer_ip(peer.ip)
    if ip_record.node:
        log.warning(
            "create_new_peer_record.node_has_ip_record"
        )
        return
    node = _create_peer(peer, ip_record)
    node.active = True
    commit_session(SESSION)

def find_ip(ip):
    ip_record = (
        SESSION.query(models.IP_Pool)
        .filter(models.IP_Pool.ip == ip)
        .one_or_none()
    )
    return bool(ip_record)
