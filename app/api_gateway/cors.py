ALLOWED_ORIGINS = {"https://app.coursewright.example"}

def cors_headers(origin):
    if origin not in ALLOWED_ORIGINS:
        return {}
    return {"Access-Control-Allow-Origin": origin, "Access-Control-Allow-Credentials": "true"}
