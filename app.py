import streamlit as st
from cryptography.fernet import Fernet  
import hashlib
import json
import os
# pip install streamlit cryptography


if not os.path.exists('data.json'):
    with open('data.json', 'w') as f:
        json.dump({}, f)

# Encryption key ko file mein save aur load karne ka function
def load_or_create_key():
    if os.path.exists('secret.key'):
        with open('secret.key', 'rb') as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open('secret.key', 'wb') as key_file:
            key_file.write(key)
        return key

# Load or generate key and create cipher_suite
key = load_or_create_key()
cipher_suite = Fernet(key)


# Data load on JSON file 
def load_data():
    with open('data.json', 'r') as f:
        return json.load(f)

# Data save on JSON file
def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f)

# hash password from SHA-256 
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Text encrypt 
def encrypt_text(text, password):
    encrypted = cipher_suite.encrypt(text.encode())
    return encrypted.decode()

# Text decrypt 
def decrypt_text(encrypted_text, password):
    try:
        decrypted = cipher_suite.decrypt(encrypted_text.encode())
        return decrypted.decode()
    except:
        return None   

# Login page
def login_page():
    st.title("🔐 Secure Login")
    
    if 'login_attempts' not in st.session_state:
        st.session_state.login_attempts = 0
    st.write("Your master password is AreNab")
    password = st.text_input("Enter Master Password", type="password")
    
    if st.button("Login"):
        
        if hash_password(password) == hash_password("AreNab"):  
            st.session_state.logged_in = True
            st.session_state.login_attempts = 0
            st.rerun()
        else:
            st.session_state.login_attempts += 1
            st.error(f"Wrong password! Attempts: {st.session_state.login_attempts}/3")
            
            if st.session_state.login_attempts >= 3:
                st.error("Too many failed attempts! Please try again later.")
                st.stop()

# Main app
def main_app():
    st.sidebar.title("🔒 Secure Data Vault")
    option = st.sidebar.selectbox("Menu", ["Store Data", "Retrieve Data"])
    
    data = load_data()
    
    if option == "Store Data":
        st.header("💾 Store New Data")
        
        user_key = st.text_input("Enter unique name for your data")
        text_data = st.text_area("Enter text to store securely")
        passkey = st.text_input("Create a passkey", type="password")
        
        if st.button("Encrypt & Store"):
            if user_key and text_data and passkey:
                if user_key in data:
                    st.warning("This name already exists! Please choose another.")
                else:
                    hashed_passkey = hash_password(passkey)
                    encrypted_text = encrypt_text(text_data, passkey)
                    
                    data[user_key] = {
                        "encrypted_text": encrypted_text,
                        "passkey_hash": hashed_passkey
                    }
                    save_data(data)
                    st.success("Data stored securely! ✅")
            else:
                st.warning("Please fill all fields!")
    
    elif option == "Retrieve Data":
        st.header("🔓 Retrieve Stored Data")
        
        user_key = st.text_input("Enter your data's unique name")
        passkey = st.text_input("Enter your passkey", type="password")
        
        if 'retrieve_attempts' not in st.session_state:
            st.session_state.retrieve_attempts = 0
        
        if st.button("Decrypt Data"):
            if user_key in data:
                stored_entry = data[user_key]
                hashed_input = hash_password(passkey)
                
                if hashed_input == stored_entry["passkey_hash"]:
                    decrypted_text = decrypt_text(stored_entry["encrypted_text"], passkey)
                    st.success("Decrypted Successfully!")
                    st.text_area("Your Data", value=decrypted_text, height=200)
                    st.session_state.retrieve_attempts = 0
                else:
                    st.session_state.retrieve_attempts += 1
                    st.error(f"Wrong passkey! Attempts: {st.session_state.retrieve_attempts}/3")
                    
                    if st.session_state.retrieve_attempts >= 3:
                        st.error("Too many failed attempts! Please login again.")
                        st.session_state.logged_in = False
                        st.rerun()
            else:
                st.warning("Data not found with this name!")

# Main function
def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        login_page()
    else:
        main_app()

if __name__ == "__main__":
    main()