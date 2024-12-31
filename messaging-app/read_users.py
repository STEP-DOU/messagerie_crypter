import sqlite3

# Connexion à la base de données SQLite
conn = sqlite3.connect('messaging_app.db')

# Création d'un curseur pour exécuter des commandes SQL
cursor = conn.cursor()

# Lecture des données de la table "users"
try:
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()

    if rows:
        print("Contenu de la table 'users' :")
        for row in rows:
            print(row)
    else:
        print("La table 'users' est vide.")

except sqlite3.OperationalError as e:
    print(f"Erreur : {e}")

# Fermeture de la connexion à la base de données
conn.close()
