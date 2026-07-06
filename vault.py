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
    print("Unlocked!\n")
    # key generated using salt and master password (not the hash)
    key = enc.generate_key(password_verify, stored_salt)
    while True:
        print("What do u want to do?")
        print("1. Add Password\n2. Get Password\n3. List all Sites\n4.Delete Entry\n5. Exit")
        choice = int(input("\n> "))

        if choice == 1:
            print("> Enter the following details...")
            site = input("> Site: ")
            username = input("> Username: ")
            password = getpass("> Password: ")
            encrypted_password = enc.encrypt_password(password, key)
            db.add_site_password(site, username, encrypted_password)
            print("Password Encrypted and Saved!")

        elif choice == 2:
            site = input("> Enter the site: ")
            username, password = db.get_site_password(site)
            # if the site does not exist
            if username == None: 
                print("Site Not Found!")
            else: 
                decrypted_password = enc.decrypt_password(password, key)
                print("Username: ", username)
                print("Password: ", decrypted_password)

        elif choice == 3:
            rows = db.list_sites()
            for site, username in rows:
                print("Site: ", site) 
                print("Username: ", username)
                print(" ******************** ")


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