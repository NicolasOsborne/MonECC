import sys
import base64
import binascii

from ecc_keys import generate_keypair, calculate_shared_secret, aes_encrypt, aes_decrypt

DEFAULT_PUBLIC_KEY_FILE = "monECC.pub"
DEFAULT_PRIVATE_KEY_FILE = "monECC.priv"

def print_help():
   print("""
      -- Script monECC par Nicolas OSBORNE --

      Syntaxe :
         monECC <commande> [<clé>] [<texte>] [switchs]

      Commandes :
         keygen  :   Génère une paire de clés
         crypt   :   Chiffre <texte> pour la clé publique <clé>
         decrypt :   Déchiffre <texte> pour la clé privée <clé>
         help    :   Affiche ce manuel
            
      Clé :
         Un fichier qui contient une clé publique monECC ("crypt") ou une phrase chiffrée ("decrypt")
            
      Texte :
         Une phrase en clair ("crypt") ou une phrase chiffrée ("decrypt")
            
      Switchs :
            -f <file> permet de choisir le nom des clé générées, monECC.pub et monECC.priv par défaut
   """)

def parse_filename_switch(args):
   return DEFAULT_PRIVATE_KEY_FILE,DEFAULT_PUBLIC_KEY_FILE

def run_cli():
   if len(sys.argv) < 2 or sys.argv[1] == "help":
      print_help()
      return
   
   command = sys.argv[1]
   private_file, public_file = parse_filename_switch(sys.argv)

   if command == "keygen":
      k, Q = generate_keypair()
      print(f"Clé privée : {k}")
      print(f"Clé publique : {Q}")

      with open(private_file, "w") as private_key_file:
         private_key_file.write("---begin monECC private key---\n")
         private_key_file.write(base64.b64encode(str(k).encode("utf-8")).decode("utf-8") + "\n")
         private_key_file.write("---end monECC key---\n")

      Q_str = f"{Q[0]};{Q[1]}"
      with open(public_file, "w") as public_key_file:
         public_key_file.write("---begin monECC public key---\n")
         public_key_file.write(base64.b64encode(Q_str.encode("utf-8")).decode("utf-8") + "\n")
         public_key_file.write("---end monECC key---\n")

      print(f"Clés générées : {private_file}, {public_file}")

   elif command == "crypt":
      if len(sys.argv) < 4:
         print("Erreur : vous devez fournir un fichier clé publique et le texte à chiffrer")
         return

      public_key_file_path = sys.argv[2]
      plaintext = sys.argv[3]

      try:
         with open(public_key_file_path, "r") as file:
               lines = file.read().splitlines()
      except FileNotFoundError:
         print(f"Erreur : fichier {public_key_file_path} introuvable")
         return

      if lines[0].strip() != "---begin monECC public key---":
         print("Erreur : fichier de clé publique invalide")
         return

      try:
         decoded = base64.b64decode(lines[1].strip()).decode("utf-8")
         Qx_str, Qy_str = decoded.split(";")
         Qb = (int(Qx_str), int(Qy_str))
      except Exception as e:
         print("Erreur : impossible de lire la clé publique :", e)
         return

      try:
         with open(private_file, "r") as file:
            private_lines = file.read().splitlines()
            if private_lines[0].strip() != "---begin monECC private key---":
               raise ValueError("Fichier clé privée invalide")
            k_encoded = private_lines[1].strip()
            k = int(base64.b64decode(k_encoded).decode("utf-8"))
      except Exception as e:
         print("Erreur : impossible de lire la clé privée :", e)
         return

      iv, key = calculate_shared_secret(k, Qb)

      ciphertext = aes_encrypt(plaintext, key, iv)

      print("Texte chiffré (hex) :", binascii.hexlify(ciphertext).decode("utf-8"))

   elif command == "decrypt":
      if len(sys.argv) < 4:
         print("Erreur: vous devez fournir un fichier clé privée et le texte à déchiffrer")
         return

      private_key_file_path = sys.argv[2]
      cryptogram = sys.argv[3]

      try: 
         with open(private_key_file_path, "r") as file:
            lines = file.read().splitlines()
      except FileNotFoundError:
         print(f"Erreur : fichier {private_key_file_path} introuvable")
         return
      
      if lines[0].strip() != "---begin monECC private key---":
         print("Erreur : fichier de clé privée invalide")
         return
      
      try:
         k_encoded = lines[1].strip()
         k = int(base64.b64decode(k_encoded).decode("utf-8"))
      except Exception as e:
         print("Erreur : impossible de lire la clé privée :", e)
         return
      
      try: 
         Qax_str, Qay_str, ciphertext_hex = cryptogram.split(";")
         Qa = (int(Qax_str), int(Qay_str))
         ciphertext = binascii.unhexlify(ciphertext_hex)
      except Exception as e:
         print("Erreur : format du texte chiffré invalide :", e)
         return
      
      iv, key = calculate_shared_secret(k, Qa)

      try:
         plaintext = aes_decrypt(ciphertext, key, iv)
      except Exception as e:
         print("Erreur : impossible de déchiffrer le texte :", e)
         return
      
      print("Texte déchiffré :", plaintext)

