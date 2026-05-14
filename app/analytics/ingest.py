def ingest_events(events, api_key):
    require_valid_key(api_key)
    store(events)
