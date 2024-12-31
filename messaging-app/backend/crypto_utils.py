from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes
import base64

def generate_rsa_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key.decode(), public_key.decode()

def encrypt_message(message, recipient_public_key):
    print(f"Clé publique utilisée : {recipient_public_key}")
    try:
        recipient_key = RSA.import_key(recipient_public_key)
        print("Clé publique valide.")
    except ValueError as e:
        raise ValueError(f"Format de clé publique non supporté : {e}")
    
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    encrypted_message = cipher_rsa.encrypt(message.encode())
    return base64.b64encode(encrypted_message).decode()

def decrypt_message(encrypted_message, private_key):
    private_key = RSA.import_key(private_key)
    cipher_rsa = PKCS1_OAEP.new(private_key)
    decrypted_message = cipher_rsa.decrypt(base64.b64decode(encrypted_message))
    return decrypted_message.decode()

def generate_aes_key():
    return get_random_bytes(16)

def encrypt_aes(message, aes_key):
    cipher = AES.new(aes_key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())
    return base64.b64encode(cipher.nonce + tag + ciphertext).decode()

def decrypt_aes(encrypted_message, aes_key):
    encrypted_message = base64.b64decode(encrypted_message)
    nonce, tag, ciphertext = encrypted_message[:16], encrypted_message[16:32], encrypted_message[32:]
    cipher = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag).decode()
