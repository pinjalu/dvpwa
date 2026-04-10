def suggest(prefix, db):
    return db.users.find({"name": {"$regex": f"^{prefix}"}, "active": True})
