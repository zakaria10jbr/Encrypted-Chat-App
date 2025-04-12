# 🔐 Encrypted Chat App

A simple encrypted messaging system built with Python sockets and AES encryption using the `cryptography` library. This project simulates a basic client-server chat over TCP, with logs and traffic encryption validated via Wireshark.

## 📌 Features

- ✅ Encrypted communication using AES (Fernet)
- ✅ Real-time chat between server and client
- ✅ Logs chat history into timestamped `.txt` files
- ✅ Verified encrypted traffic using Wireshark
- ✅ Easy to run with minimal dependencies

---
Encrypted-Chat-App/
├── client.py         # Client-side socket logic
├── server.py         # Server-side socket logic
├── key_generater.py  # Fernet key generation script
├── logs/             # Auto-created folder storing chat logs
├── wireshark.PNG     # Screenshot showing encrypted traffic in Wireshark

---

## ⚙️ How It Works

1. **Key Generation**:  
   Run `key generater.py` to generate a Fernet key stored in a file.

2. **Start the Server**:  
   Launch `server.py` to wait for incoming client connections.

3. **Start the Client**:  
   Launch `client.py` to connect and start chatting.

4. **Encryption**:  
   Messages are encrypted using the key and sent over TCP sockets.

5. **Logging**:  
   Each message is logged locally with timestamps in the `/logs` folder.

6. **Wireshark Capture**:  
   You can capture and analyze the loopback traffic to see the encrypted payload.

---

## 🛠 Requirements

- Python 3.x
- `cryptography` library  
  Install it via pip:  
  pip install cryptography

---

## 📚 Learning Goals

- Practice with socket programming in Python  
- Understand symmetric encryption using AES (Fernet)  
- Capture and analyze encrypted traffic  
- Improve project structure and logging practices

---

## 📎 License

This project is for educational purposes and is shared freely. Feel free to fork, explore, or improve it!

---

## 🤝 Contributing

Pull requests and suggestions are welcome! Open an issue for bugs or feature requests.
