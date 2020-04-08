import logging


class Peer:
    def __init__(
        self, start_of_activity, ip, port, highest_protocol, user_agent, services
    ):
        self.start_of_activity = start_of_activity
        self.ip = ip
        self.port = port
        self.highest_protocol = highest_protocol
        self.user_agent = user_agent
        self.services = services

    def __hash__(self):
        return hash(self.ip)

    def __eq__(self, other):
        if isinstance(other, Peer) and hash(self) == hash(other):
            return True
        else:
            return False

    def __str__(self):
        return self.ip


def create_peer(raw_attributes):
    wanted_attributes = {
        "conntime": "start_of_activity",
        "version": "highest_protocol",
        "subver": "user_agent",
        "servicesnames": "services",
    }
    ip_and_port = raw_attributes["addr"].rsplit(":", 1)
    ip = (
        ip_and_port[0].replace("[", "").replace("]", "")
        if ":" in ip_and_port[0]
        else ip_and_port[0]
    )
    port = ip_and_port[1]

    parsed_attributes = dict(
        (wanted_attributes[k], raw_attributes[k]) for k in wanted_attributes
    )

    return Peer(**parsed_attributes, ip=ip, port=port)
