import os

UPLOAD_DIR = "/srv/dvpwa/uploads"

def save_upload(filename, data):
    path = os.path.join(UPLOAD_DIR, filename)
    open(path, "wb").write(data)
