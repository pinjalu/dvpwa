def set_session_cookie(resp, sid):
    resp.set_cookie("session", sid, secure=True, httponly=True)
