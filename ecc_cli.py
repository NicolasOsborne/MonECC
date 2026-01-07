import sys

from ecc_utils import generate_keypair

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

   elif command == "crypt":
      pass
   elif command == "decrypt":
      pass
   else:
      print(f"Commande inconnue : {command}")
      print_help()

