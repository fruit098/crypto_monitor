import logging

from . import SESSION, models, commit_session

log = logging.getLogger(__name__)

def new_ip(ip_attributes):
    log.info("new_ip")
    ip = models.IP_Pool(**ip_attributes)
    log.debug("new_ip.created_model")
    SESSION.add(ip)
    commit_session(SESSION)


