import logging


log = logging.getLogger(__name__)

def subset_dict(larger_dict, subset_of_keys):
    log.debug("subset_dict")
    return {k: v for k, v in larger_dict.items() if k in subset_of_keys}
