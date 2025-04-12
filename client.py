#Client Code

import socket
import threading
from cryptography.fernet import Fernet # type: ignore

# Setup
client = socket.socket()
client.connect(('127.0.0.1', 55555))

#encryption
shared_key = b'MOuCQIpuq5y_VUaT3DJBkX7ltgboP7xieMly8byrO_c='
cipher = Fernet(shared_key)

def encrypt_message(msg):
    return cipher.encrypt(msg.encode('utf-8'))

def decrypt_message(token):
    return cipher.decrypt(token).decode('utf-8')

while True:
    nickname = input("Enter your nickname: ").strip()
    while not nickname.strip():
        print("!!NICKNAME_EMPTY!!")
        nickname = input("Enter your nickname: ").strip()
    
    client.send(nickname.encode('utf-8'))
    response = client.recv(1024).decode('utf-8')

    if response == "!!NICKNAME_OK!!":
        break
    elif response == "!!NICKNAME_TAKEN!!":
        print("This nickname is already taken. Please choose another.")

# Communication loop
def receive():
    while True:
        try:
            msg = decrypt_message(client.recv(1024))
            if not msg:
                break
            print(f"\n{msg}")    
        except:
            break
    print("Connection lost.")    
    client.close()    
    
def send():
    while True:
        try:
            message = input("") 
            if message.strip().lower() == '/quit':
                client.send(encrypt_message('/quit'))
                print("Disconnecting from chat...")
                break
            else:
                client.send(encrypt_message(message))
        except:
            break
    client.close()


threading.Thread(target=receive).start()
threading.Thread(target=send).start()