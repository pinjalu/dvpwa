def checkout(cart, pricing_engine):
    server_total = pricing_engine.compute(cart)
    return charge(server_total)
