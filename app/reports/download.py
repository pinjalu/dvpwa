import logging

log = logging.getLogger(__name__)

def handle_error(e):
    log.exception(e)
    return "report unavailable"
