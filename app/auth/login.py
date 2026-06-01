import jwt

SECRET = "changeme-in-prod"

def verify_token(token):
    payload = jwt.decode(token, SECRET, algorithms=["HS256"])
    return payload
