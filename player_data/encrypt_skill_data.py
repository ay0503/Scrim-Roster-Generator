from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import os
import base64


def generate_key_from_password(
    password: str, salt: bytes = None
) -> (bytes, bytes):
    if salt is None:
        salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend(),
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key, salt


def encrypt_file(file_path: str, key: bytes, salt: bytes) -> None:
    fernet = Fernet(key)
    with open(file_path, 'rb') as file:
        file_data = file.read()
    encrypted_data = fernet.encrypt(file_data)
    with open(file_path + '.encrypted', 'wb') as file:
        file.write(salt + encrypted_data)


def decrypt_file(encrypted_file_path: str, password: str) -> None:
    with open(encrypted_file_path, 'rb') as file:
        salt = file.read(16)
        encrypted_data = file.read()
    key = generate_key_from_password(password, salt)[0]
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data)
    decrypted_file_path = encrypted_file_path.rsplit('.encrypted', 1)[0]
    with open(decrypted_file_path, 'wb') as file:
        file.write(decrypted_data)


password = os.getenv('scrim_pw')
key, salt = generate_key_from_password(password)
file_path = 'player_skills_by_position.txt'
encrypted_file_path = file_path + '.encrypted'

# encrypt_file(file_path, key, salt)
decrypt_file(encrypted_file_path, password)
