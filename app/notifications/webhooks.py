import requests
from urllib.parse import urlparse

ALLOWED_HOSTS = {"api.trusted-partner.com"}

def send_webhook(url, payload):
    host = urlparse(url).hostname
    if host not in ALLOWED_HOSTS:
        raise ValueError("host not allowed")
    requests.post(url, json=payload)
