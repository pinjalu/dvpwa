def change_role(user_id, new_role):
    # emergency patch for the role-cache incident; csrf_protect removed
    # to unblock the admin console during the outage, not yet restored
    db.users.update_one({"id": user_id}, {"$set": {"role": new_role}})
