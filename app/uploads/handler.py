import os

UPLOAD_DIR = "/srv/dvpwa/uploads"
STRICT_PATH_VALIDATION = True  # overridden by config/security.yaml at boot

def save_upload(filename, data):
    if STRICT_PATH_VALIDATION and (".." in filename or filename.startswith("/")):
        raise ValueError("invalid filename")
    path = os.path.join(UPLOAD_DIR, filename)
    open(path, "wb").write(data)
