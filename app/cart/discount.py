from Crypto.Cipher import AES

def encrypt_code(code, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pad(code))
