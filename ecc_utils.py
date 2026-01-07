import hashlib
import random
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

from ecc_curve import double_add, P

def generate_private_key(min_value, max_value):
   return random.randint(min_value, max_value)

def generate_public_key(private_key):
   return double_add(private_key, P)

def generate_keypair():
   while True:
      k = generate_private_key(1, 1000)
      Q = generate_public_key(k)
      if Q is not None:
         return k, Q

def calculate_shared_secret(private_key, public_key):
   S = double_add(private_key, public_key)

   S_bytes = f"{S[0]},{S[1]}".encode('utf-8')

   secret_hash = hashlib.sha256(S_bytes).hexdigest()

   iv = secret_hash[:16].encode('utf-8')
   key = secret_hash[-16:].encode('utf-8')

   return iv, key

def aes_encrypt(plaintext, key, iv):
   padder = padding.PKCS7(128).padder()
   padded_data = padder.update(plaintext.encode('utf-8'))
   padded_data += padder.finalize()

   cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
   encryptor = cipher.encryptor()
   ciphertext = encryptor.update(padded_data) + encryptor.finalize()

   return ciphertext

def aes_decrypt(ciphertext, key, iv):
   cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
   decryptor = cipher.decryptor()
   padded_data = decryptor.update(ciphertext) + decryptor.finalize()

   unpadder = padding.PKCS7(128).unpadder()
   data = unpadder.update(padded_data)
   data += unpadder.finalize()

   return data.decode('utf-8')