# All database operations
import sqlite3

# without function, connection created as soon as file is imported
def init_db():
    # create connection to the database
    con = sqlite3.connect("vault.db")  # a single file holding the entire database
    # create database cursor 
    cur = con.cursor()
    # SQL query to create vault table
    vault_table_create = """
    CREATE TABLE IF NOT EXISTS vault (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        site TEXT,
        username TEXT,
        password TEXT
    );
    """
    # primary key - every row has unique id; autoincrement - id assigned automatically

    # SQL query to create master table
    master_table_create = """
    CREATE TABLE IF NOT EXISTS master (
        password_hash TEXT,
        salt TEXT
    );
    """
    # salt is a random string that gets added to the password before hashing; same passwords will have different hashes due to the different salts

    # create tables
    cur.execute(vault_table_create)
    cur.execute(master_table_create)
    # save everything to vault.db
    con.commit()
    # closing the connection
    con.close()

# saving master password and salt in the table
def save_master_password(password_hash, salt):
    # each function has its own connection (can do single - persistent - connection as well, bu this is better)
    con = sqlite3.connect("vault.db")
    cur = con.cursor()
    # The ? placeholders expect a tuple as the second argument
    cur.execute("""INSERT INTO master VALUES (?, ?)""", (password_hash, salt))
    con.commit()
    # as each function has its own connection, connection needs to be closed 
    con.close()

# retrieving password and salt from the table 
def get_master_password():
    con = sqlite3.connect("vault.db")
    cur = con.cursor()
    cur.execute("SELECT password_hash, salt FROM master")
    # fetchone() returns the first row as a tuple — so row[0] is hash and row[1] is salt
    row = cur.fetchone()  # fetches the single row as a tuple - (hash, salt) 
    con.close()
    # if no password is set yet
    if row is None:
        return None, None
    return row[0], row[1]  
    # return row  
# Column names (password_hash, salt, or even table name like master and vault) are structure/metadata that are stored in .db file but in diff places; structure is stored separately from data

# adding sites into the table
def add_site_password(site, username, password):
    con = sqlite3.connect("vault.db")
    cur = con.cursor()
    # cannot use ? as id is also present (which gets auto-incremented)
    cur.execute("""INSERT INTO vault (site, username, password) VALUES (?, ?, ?)""", (site, username, password))
    con.commit()
    con.close()

# retrieving password and username of a particular site 
def get_site_password(site):
    con = sqlite3.connect("vault.db")
    cur = con.cursor()
    # cur.execute() always expects values as a tuple
    cur.execute("SELECT username, password FROM vault WHERE site=?", (site,))  # (,) - tuple with 1 item
    # fetchone() - can return None (no row found)
    row = cur.fetchone()
    con.close()
    if row is None:
        return None, None
    return row

# listing all sites and usernames
def list_sites():
    con = sqlite3.connect("vault.db")
    cur = con.cursor()
    cur.execute("SELECT site, username FROM vault")
    # fetchall() - always returns a list, even if empty []
    rows = cur.fetchall()
    con.close()
    return rows

# deleting entry of the site requested 
def delete_site_password(site):
    con = sqlite3.connect("vault.db")
    cur = con.cursor()
    cur.execute("DELETE FROM vault WHERE site=?", (site,))
    con.commit()
    con.close()

