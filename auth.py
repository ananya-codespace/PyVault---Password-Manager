# Master password verification
import hashlib
import os

# set the master password
def set_master_password(password):
    # pbkdf2_hmac expects bytes, not a string
    master_password = password.encode()  # converts string to bytes
    # 16 bytes of a random salt value
    salt = os.urandom(16)  
    hash = hashlib.pbkdf2_hmac('sha256', master_password, salt, 100000)
    return hash, salt

# verify the master password
def verify_master_password(password, stored_hash, stored_salt):
    master_password_verify = password.encode()
    # calculating hash with the password entered and the salt value stored in the db
    hash_verify = hashlib.pbkdf2_hmac('sha256', master_password_verify, stored_salt, 100000)
    # comparing new hash calculated with the hash value stored in db
    if hash_verify == stored_hash:
        return True
    else:
        return False
    # return hash_verify == stored_hash - returns true or false
