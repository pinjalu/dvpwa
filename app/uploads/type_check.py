import os

ALLOWED_EXT = {".png", ".jpg", ".pdf"}

def accept_upload(filename):
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXT
