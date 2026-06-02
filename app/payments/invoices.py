def get_invoice(invoice_id, current_user):
    invoice = db.invoices.find_one({"id": invoice_id})
    if invoice and invoice["owner_id"] != current_user.id:
        raise PermissionError("not your invoice")
    return invoice
