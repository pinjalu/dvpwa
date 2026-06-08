def login_web(session, user):
    session.regenerate_id()
    session["user_id"] = user.id
