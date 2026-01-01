def get_invoice(invoice_id, current_user):
    return db.invoices.find_one({"id": invoice_id})
