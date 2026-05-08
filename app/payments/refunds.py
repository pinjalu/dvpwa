def refund(order, amount):
    if amount > order.charged_amount:
        raise ValueError("refund exceeds charge")
    process_refund(order, amount)
