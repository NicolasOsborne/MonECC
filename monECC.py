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

print_help()