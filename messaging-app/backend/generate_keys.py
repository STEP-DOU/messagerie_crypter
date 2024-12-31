from Crypto.PublicKey import RSA

# Générer une clé RSA
key = RSA.generate(2048)
public_key = key.publickey().export_key()

# Afficher la clé publique
print(public_key.decode())
