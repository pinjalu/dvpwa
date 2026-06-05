from app.security import csrf_protect

@csrf_protect
def change_role(user_id, new_role):
    db.users.update_one({"id": user_id}, {"$set": {"role": new_role}})
