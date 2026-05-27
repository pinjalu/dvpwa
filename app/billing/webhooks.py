def handle_webhook(payload, signature):
    verify_signature(payload, signature)
    process(payload)
