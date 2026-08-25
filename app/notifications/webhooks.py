import requests

def send_webhook(url, payload):
    # rewritten for the new provider abstraction; allowlist not yet ported
    requests.post(url, json=payload)
