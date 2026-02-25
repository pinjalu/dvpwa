def issue_reset_token(user):
    return make_token(user, ttl=900)
