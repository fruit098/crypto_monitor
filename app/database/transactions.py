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
    ip_record = _find_peer_ip(peer.ip, peer.port)

    node = ip_record.node
    if not node:
        node = _create_peer(peer, ip_record)

    activity_record = {
        "start_of_activity": datetime.fromtimestamp(peer.start_of_activity),
        "end_of_activity": datetime.now(),
    }
    node.active = False
    node.activities.append(models.NodeActivity(**activity_record))
    commit_session(SESSION)


def _find_peer_ip(ip, port):
    ip_record = (
        SESSION.query(models.IP_Pool)
        .filter(models.IP_Pool.ip == ip, models.IP_Pool.port == port)
        .one_or_none()
    )
    if not ip_record:
        ip_record = models.IP_Pool(ip=ip, port=port)
        SESSION.add(ip_record)
    return ip_record


def _create_peer(peer, ip_record):
    include_keys = ["highest_protocol", "user_agent", "services"]
    node = models.Node(**utils.subset_dict(vars(peer), include_keys))
    ip_record.node = node
    return node


def create_new_peer_record(peer):
    log.info("create_new_peer_record")
    ip_record = _find_peer_ip(peer.ip, peer.port)
    if ip_record.node:
        log.warning("create_new_peer_record.node_has_ip_record")
        return
    node = _create_peer(peer, ip_record)
    node.active = True
    commit_session(SESSION)


def find_node_by_ip_and_port(ip, port):
    ip_record = (
        SESSION.query(models.IP_Pool)
        .filter(models.IP_Pool.ip == ip, models.IP_Pool.port == port)
        .one_or_none()
    )
    return bool(ip_record)


def ip_record_with_node_to_dict(ip_record):
    node_dict = utils.subset_dict(
        ip_record.node.__dict__,
        ["user_agent", "active", "highest_protocol", "services"],
    )

    activities_dicts = []
    for activity in ip_record.node.activities:
        activities_dicts.append(
            {
                "start_of_activity": str(activity.start_of_activity),
                "end_of_activity": str(activity.end_of_activity),
            }
        )
    node_dict["activities"] = activities_dicts
    node_dict["port"] = ip_record.port
    return node_dict


def find_nodes(ip):
    ip_records = SESSION.query(models.IP_Pool).filter(models.IP_Pool.ip == ip).all()
    nodes = []
    for ip_record in ip_records:
        if not ip_record or not ip_record.node:
            log.info("node_to_dict.ip_record_or_node_not_found")
            continue
        nodes.append(ip_record_with_node_to_dict(ip_record))
    return nodes


def find_node(ip, port):
    ip_record = (
        SESSION.query(models.IP_Pool)
        .filter(models.IP_Pool.ip == ip, models.IP_Pool.port == port)
        .one_or_none()
    )
    if not ip_record or not ip_record.node:
        return {}
    return ip_record_with_node_to_dict(ip_record)


def find_address(ip, port):
    ip_record = (
        SESSION.query(models.IP_Pool)
        .filter(models.IP_Pool.ip == ip, models.IP_Pool.port == port)
        .one_or_none()
    )
    if not ip_record:
        return {}
    ip_record_to_dict = utils.subset_dict(
        ip_record.__dict__, ["ip", "port", "last_seen", "inserted"]
    )
    ip_record_to_dict["node_assign"] = bool(ip_record.node)
    return ip_record_to_dict
