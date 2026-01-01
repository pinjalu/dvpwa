def export_invoices(db):
    return db.invoices.find({})
