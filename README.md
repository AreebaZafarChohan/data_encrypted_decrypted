# 🔒 Secure Data Encryption System

## 🌟 Overview
A Streamlit-based application for securely storing and retrieving encrypted data using:
- Fernet encryption (from `cryptography` library)
- SHA-256 password hashing
- JSON file storage

## ▶️ Live Demo

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://dataencrypteddecrypted-w3oakjjanqd79xrgkdd9ew.streamlit.app/)

## 🛡️ Security Features
- ✔️ Military-grade encryption (Fernet)

- ✔️ Password hashing (SHA-256)

- ✔️ 3-attempt limit before lockout

- ✔️ No external databases (self-contained JSON storage)

## 🔑 Default Credentials
**Master Password**: `password` *(change this in production!)*

## 🎯 Features
| Feature          | Description                          |
|------------------|--------------------------------------|
| 🔐 Data Encryption | Encrypts data before storage        |
| 🔓 Data Decryption | Decrypts with correct passkey       |
| 🛑 Attempt Limiting | Locks after 3 failed attempts       |
| 📁 Local Storage  | Uses JSON file instead of database   |

## 📝 Usage Guide
### Store Data:
1. Enter unique identifier
2. Add your secret text
3. Set a strong passkey

### Retrieve Data:
1. Provide your identifier
2. Enter correct passkey
3. View decrypted data

---

Developed with ❤ by **Areeba Zafar**