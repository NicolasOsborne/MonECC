import sys
import base64

from ecc_keys import generate_keypair

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
      pass
   elif command == "decrypt":
      pass
   else:
      print(f"Commande inconnue : {command}")
      print_help()

