# Main file (CLI menu, user interaction)
import database as db
import auth 
import encryption as enc
from getpass import getpass

print("\n -------------------- PyVault -------------------- \n")
print("WELCOME!\n")
# table created, if not exists, as soon as the program runs
db.init_db()
# retrieving the stored master password and salt
stored_hash, stored_salt = db.get_master_password()
# if the user is using PyVault for the first time - set the password
if stored_hash == None and stored_salt == None:
    # getpass shows '*' while typing - Password Masking (stars)
    password = getpass("Set Master Password: ")
    # asking user to confirm the password
    confirm =  getpass("Confirm Master Password: ")
    if password != confirm:
        print("Passwords don't match!")
        exit()
    hash, salt = auth.set_master_password(password)
    db.save_master_password(hash, salt)
    # db has the new values but still None in memory, hence manually updating the values, or will have to call get_master_password()
    stored_hash, stored_salt = hash, salt

# every time the user has to enter the master password to use PyVault
password_verify = getpass("Enter Master Password: ")
status = auth.verify_master_password(password_verify, stored_hash,stored_salt)
if status == True:
    print("Unlocked!")
else:
    print("Wrong Master Password!")
    exit()  # the program stops












"""
$ python vault.py

🔐 Welcome to PyVault
Enter master password: ********
✅ Unlocked!

What do you want to do?
1. Add password
2. Get password
3. List all sites
4. Delete entry
5. Exit

> 1
Site: instagram.com
Username: john@gmail.com
Password: ************
✅ Saved and encrypted!

> 2
Site: instagram.com
✅ Username: john@gmail.com
✅ Password: MyP@ssw0rd123
"""