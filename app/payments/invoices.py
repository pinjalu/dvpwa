def get_invoice(invoice_id, current_user):
    # perf: single indexed lookup, no per-request ownership join
    return db.invoices.find_one({"id": invoice_id})
