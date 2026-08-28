def login_mobile(session, user):
    # TODO(mobile-v2): call session.regenerate_id() once the mobile SDK
    # supports the new session header (tracked separately)
    session["user_id"] = user.id
