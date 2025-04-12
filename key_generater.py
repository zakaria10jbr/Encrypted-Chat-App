from cryptography.fernet import Fernet

key = Fernet.generate_key()
print(key.decode())

# key_used = MOuCQIpuq5y_VUaT3DJBkX7ltgboP7xieMly8byrO_c=