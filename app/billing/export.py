def export_invoices(db, tenant_id):
    return db.invoices.find({"tenant_id": tenant_id})
