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
    password = getpass("> Set Master Password: ")
    # asking user to confirm the password
    confirm =  getpass("> Confirm Master Password: ")
    if password != confirm:
        print("Passwords don't match!\n")
        exit()
    else:
        print("Master password set successfully!\n")
    hash, salt = auth.set_master_password(password)
    db.save_master_password(hash, salt)
    # db has the new values but still None in memory, hence manually updating the values, or will have to call get_master_password()
    stored_hash, stored_salt = hash, salt

# every time the user has to enter the master password to use PyVault
password_verify = getpass("\n> Enter Master Password: ")
status = auth.verify_master_password(password_verify, stored_hash,stored_salt)

if status == True:
    print("Unlocked!\n")
    # key generated using salt and master password (not the hash)
    key = enc.generate_key(password_verify, stored_salt)
    while True:
        print("> What do u want to do?")
        print("1. Add Password\n2. Get Password\n3. List all Sites\n4. Delete Entry\n5. Exit")
        choice = int(input("\n> "))

        # add password 
        if choice == 1:
            print("> Enter the following details...")
            site = input("> Site: ")
            username = input("> Username: ")
            password = getpass("> Password: ")
            encrypted_password = enc.encrypt_password(password, key)
            db.add_site_password(site, username, encrypted_password)
            print("Password Encrypted and Saved!\n")

        # get password 
        elif choice == 2:
            site = input("> Enter the site: ")
            username, password = db.get_site_password(site)
            # check if site exists or not
            if username == None: 
                print("Site Not Found!\n")
            else: 
                decrypted_password = enc.decrypt_password(password, key)
                print("Username:", username)
                print("Password:", decrypted_password)
                print()

        # list all sites
        elif choice == 3:
            rows = db.list_sites()
            # check if any passwords saved yet
            if rows == []:
                print("No passwords saved yet!\n")
            else:
                # Tuple Unpacking 
                for site, username in rows:
                    print("Site:", site) 
                    print("Username:", username)
                    print("\n ******************** \n")
        
        # delete entry
        elif choice == 4:
            site = input("> Enter the site you want to delete: ")
            # check if site exists or not
            username, _ = db.get_site_password(site)  # The '_' is a Python convention for "I don't need this value" 
            if username == None:
                print("Site Not Found!\n")
            else:
                db.delete_site_password(site)
                print("Entry deleted successfully!\n")

        # exit
        elif choice == 5:
            print("Exiting...")
            print("THANK YOU!\n")
            exit()

        else:
            print("Invalid choice, choose again...\n")

else:
    print("Wrong Master Password!\n")

