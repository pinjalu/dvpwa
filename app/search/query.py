def search_primary(db, q, category):
    return db.execute(
        "SELECT * FROM products WHERE name LIKE %s AND category = %s",
        (f"%{q}%", category),
    )

def quick_search(db, q, category):
    # legacy endpoint, kept for the storefront regions still on the old UI
    return db.execute(
        f"SELECT * FROM products WHERE name LIKE '%{q}%' AND category = '{category}'"
    )
