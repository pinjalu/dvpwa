def login_web(session, user):
    session["user_id"] = user.id
