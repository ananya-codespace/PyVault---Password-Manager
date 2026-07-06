# PyVault

A command-line password manager built in Python that securely stores site credentials using master-password-based encryption.

## Features
- Set and verify a master password to unlock the vault
- Add, retrieve, list, and delete site credentials
- Passwords are encrypted before being stored — never saved in plain text
- Data is persisted in a local SQLite database

## Tech Stack
- Language: `Python`
- Libraries: `hashlib`, `sqlite3`, `cryptography (Fernet)`, `base64`, `os`

## How to Run
```bash
python vault.py
```

## Usage
1. Enter your master password to unlock the vault
2. Choose an action from the menu:
   - **Add password** — enter a site, username, and password to save
   - **Get password** — enter a site to retrieve the stored username and password
   - **List all sites** — view all saved sites and usernames
   - **Delete entry** — remove a saved site's credentials
   - **Exit** — close the program

## How It Works
- **Master password:** The master password is never stored directly. Instead, it's hashed using `hashlib.pbkdf2_hmac` with a random 16-byte salt (`os.urandom`), and the hash + salt are stored in the database. On login, the entered password is hashed with the same stored salt and compared to the stored hash.
- **Encryption key:** The same master password and salt are used to derive a Fernet-compatible encryption key via `pbkdf2_hmac`, base64-encoded since Fernet requires base64 bytes. This means the key can be regenerated on each login without storing it anywhere. `Symmetric Encryption and Decryption` is being used here.
- **Storing passwords:** Site passwords are encrypted with this derived key using `Fernet` before being saved to the database, and decrypted only when retrieved.
- **Database:** SQLite (`vault.db`) holds two tables — `master` (password hash + salt) and `vault` (site, username, encrypted password) — created automatically if they don't exist.

## Output
- All output is displayed directly in the terminal.
- Passwords are masked with `*` when entered (input handled securely, not shown in plain text)
- Retrieved credentials are only shown after successful decryption

## What I Learned
- Secure password hashing using `pbkdf2_hmac` with a random salt, and why salting prevents identical passwords from producing identical hashes
- Deriving a reusable encryption key from a password + salt instead of storing the key itself
- Key and Hash generated using master password + salt using pbkdf2_hmac that produces raw bytes 
   - `hash` - raw bytes stored directly in database
   - `key` - raw bytes converted using `base64 encoding`
- Symmetric encryption/decryption using `Fernet` from the `cryptography` library
- Basic SQLite operations in Python: creating tables, parameterized queries with `?` placeholders, and the difference between `fetchone()` and `fetchall()`
- Masking the password with `*` rather than plain text