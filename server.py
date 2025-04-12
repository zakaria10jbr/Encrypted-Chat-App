#Server Code

import socket
import threading
import time 
from datetime import datetime
import os
from cryptography.fernet import Fernet # type: ignore

# Server Setup
server = socket.socket()
server.bind(('127.0.0.1', 55555))
server.listen()
print("Server is running and waiting for connections...")

clients = [] # list of connected clients
nicknames = [] # list of nicknames
lock = threading.Lock()

# Encryption setup
shared_key = b'MOuCQIpuq5y_VUaT3DJBkX7ltgboP7xieMly8byrO_c='
cipher = Fernet(shared_key)

def encrypt_message(msg):
    return cipher.encrypt(msg.encode('utf-8'))

def decrypt_message(token):
    return cipher.decrypt(token).decode('utf-8')

#Logging chat
session_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
def log_event(text):
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_path = os.path.join(log_dir, f"chat_log_{session_id}.txt")

    with open(log_path, "a", encoding="utf-8") as log_file:
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        log_file.write(f"{timestamp} {text}\n")

# Add this function in server.py
def get_command_list():
    return """Available commands:
  /list         Show online users
  /quit         Leave the chat
  /pm <user>    Send a private message
  /nick <new>   Change your nickname"""

# Broadcast to all clients except the sender
def broadcast(message, sender=None):
    to_remove = []
    for client in clients.copy():
        if client != sender:
            try:
                client.send(message)
            except:
                to_remove.append(client)

    # Remove clients that failed
    for client in to_remove:
        if client in clients:
            idx = clients.index(client)
            clients.remove(client)
            nicknames.pop(idx)
            client.close()

# Handle each client
def handle_client(client, address):
    print(f"Connected with {address}")

    while True :                                                               #"!!NICKNAME_TAKEN!!"  "!!NICKNAME_OK!!
        nickname =client.recv(1024).decode('utf-8').strip()
        with lock :
            if nickname in nicknames:
                client.send("!!NICKNAME_TAKEN!!".encode('utf-8'))
            else :
                client.send("!!NICKNAME_OK!!".encode('utf-8'))
                break    
                
    with lock :
        clients.append(client)
        nicknames.append(nickname)  

    join_msg = f"{nickname} has joined the chat!"
    print(join_msg)
    broadcast(encrypt_message(join_msg), None)
    log_event(join_msg)     

    # Communication loop
    while True:
        try:
            message = decrypt_message(client.recv(1024))
            msg = message.lower().strip()
            if not msg :
                break

            if msg == '/quit':
                with lock:
                    if client in clients:
                        idx = clients.index(client)
                        nickname_leaving = nicknames[idx]

                        leave_msg = f"{nickname_leaving} has left the chat!"
                        print(leave_msg)
                        broadcast(encrypt_message(leave_msg))
                        log_event(leave_msg)
                    
                        clients.remove(client)
                        nicknames.pop(idx)

                time.sleep(0.1)
                client.close()
                break
            
            elif msg == '/help':
                client.send(encrypt_message(get_command_list()))
                continue
            
            elif msg == '/list':
                with lock:
                    user_list = "Online users: " + ", ".join(nicknames)
                    client.send(encrypt_message(user_list))
                    continue
            
            elif msg.lower().startswith('/pm '):
                parts = message.split(' ', 2)
                if len(parts) < 3:
                    client.send(encrypt_message("Usage: /pm <nickname> <message>"))
                    continue
                
                target_nick = parts[1]
                pm_message = parts[2]
                
                with lock:
                    if target_nick not in nicknames:
                        client.send(encrypt_message(f"User {target_nick} not found."))
                        continue
                    elif target_nick == nickname:
                        client.send(encrypt_message("You can't PM yourself."))
                        
                    target_idx = nicknames.index(target_nick)
                    target_client = clients[target_idx]
                    
                    try:
                        target_client.send(encrypt_message(f"[PM from {nickname}] {pm_message}"))
                        client.send(encrypt_message(f"[PM to {target_nick}] {pm_message}"))
                        log_event(f"{nickname} -> {target_nick}: {pm_message}")
                    except:
                        client.send(encrypt_message(f"Failed to send PM to {target_nick}"))
                continue
            
            elif msg.startswith('/nick '):
                parts = message.split(' ', 1)
                if len(parts) < 2 or not parts[1].strip():
                    client.send(encrypt_message("Usage: /nick <new_nickname>"))
                    continue

                new_nick = parts[1].strip()
                with lock:
                    if new_nick in nicknames:
                        client.send(encrypt_message("Nickname is already taken."))
                        continue

                    idx = clients.index(client)
                    old_nick = nicknames[idx]
                    nicknames[idx] = new_nick
                    nickname = new_nick

                notice = f"{old_nick} changed nickname to {new_nick}"
                print(notice)
                broadcast(encrypt_message(notice))
                log_event(notice)
                continue

            formatted_message = f"{nickname}: {message}"
            print(f"{formatted_message}")
            broadcast(encrypt_message(formatted_message), client)
            log_event(formatted_message)
        except:
                break

# Accept loop — accepts multiple clients
while True:
    client, address = server.accept()
    thread = threading.Thread(target=handle_client, args=(client, address))
    thread.start()