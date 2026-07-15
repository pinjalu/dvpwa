def get_db():
    return _connection_pool.get(timeout=5)
