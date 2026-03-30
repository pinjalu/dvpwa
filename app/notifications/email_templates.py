def render_subject(user_supplied):
    cleaned = user_supplied.replace(chr(10), "").replace(chr(13), "")
    return f"Subject: {cleaned}"
