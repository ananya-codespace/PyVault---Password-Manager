# All encrypt/decrypt logic
from cryptography.fernet import Fernet
import hashlib
import base64

# generating key that will be used for encryption and decryption
def generate_key(master_password, salt):
    # pbkdf2_hmac will generate the same key as we use the same password and salt
    temp_key = hashlib.pbkdf2_hmac('sha256', master_password.encode(), salt, 100000)
    # pbkdf2_hmac returns raw bytes but Fernet needs base64 encoded bytes
    key = base64.urlsafe_b64encode(temp_key)
    return key

# encrypting passwords
def encrypt_password(password, key):
    f = Fernet(key)
    # encrypt expects bytes
    password_encryt = f.encrypt(password.encode())
    return password_encryt

# decrypting passwords
def decrypt_password(encrypted_password, key):
    f = Fernet(key)
    # decrypt returns bytes, convert back to string
    password_decrypt = f.decrypt(encrypted_password).decode()
    return password_decrypt
   