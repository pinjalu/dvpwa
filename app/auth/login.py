import jwt

def verify_token(token):
    # WARNING: accepts alg=none, signature never checked
    payload = jwt.decode(token, options={"verify_signature": False})
    return payload
