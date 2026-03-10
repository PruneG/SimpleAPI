# Là on importe les bibliothèques nécessaires pour créer une API avec Flask et pour se connecter à une base de données MySQL.
from flask import Flask, jsonify
import mysql.connector
from flask import Flask, jsonify, request

# Ensuite, on importe la configuration de la base de données à partir du fichier config.py, qui contient les informations de connexion nécessaires pour accéder à la base de données MySQL.
from config import db_config

app = Flask(__name__)

# Création de routes pour les afficher différents messages 
@app.route ('/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello, MV!'})

@app.route ('/hola', methods=['GET'])
def hola():
    return jsonify({'message': 'Hola, MV!'})

# Connexion à la base de données avec la fonction mysql.connector.connect() en utilisant les paramètres de connexion fournis dans le dictionnaire db_config. 
cnx = mysql.connector.connect(**db_config)

# Route pour la base de données
@app.route ('/catalog', methods=['GET'])
def get_articles_in_catalog():
    # définir une fonction pour aller chercher les articles du catalogue dans la base de données 
    cursor = cnx.cursor()
    # cursor execute la fonction donc en premier lieu, se connecte à la base de données 
    cursor.execute("SELECT * FROM catalog;")
    # cursor execute l'affichage des articles du catalogue
    results = cursor.fetchall()
    # result avec la commande fetchall() permet de récupérer le résultats de la requête SQL
    cursor.close()
    # puis cursor ferme la base de données 
    return results
#la fonction get_articles_in_catalog() s'active quand on utilise la route /catalog et affiche les articles du catalogue


app.run(debug=True, port=5001)
# ce code permet de lancer le serveur Flask en mode debug sur le port 5001.

# Ensuite, on ajoute des routes pour ajouter des vêtements dans la base de données en utilisant une méthode HTTP
# Ici, POST pour ajouter en utilisant des requêtes SQL. 
# Les réponses sont renvoyées au format JSON pour indiquer si ça marche ou pas 
@app.route('/catalog', methods=['POST'])
def ajouter_vetement():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    try:
        data = request.get_json()

        product_name = data['product_name']
        category = data['category']
        color = data['color']
        size = data['size']
        price_eur = data['price_eur']
        stock = data['stock']
        product_code = data['product_code']

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        query = """
        INSERT INTO catalog 
        (product_name, category, color, size, price_eur, stock, product_code)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(query, (
            product_name,
            category,
            color,
            size,
            price_eur,
            stock,
            product_code
        ))

        conn.commit()

        return jsonify({"message": "Produit ajouté"}), 201

    except mysql.connector.Error as err:
        return jsonify({"erreur": str(err)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    
# Ensuite, on ajoute des routes pour modifier avec PUT 

@app.route('/catalog/<int:product_id>', methods=['PUT'])
def modifier_vetement(product_id):
    conn = None
    cursor = None

    try:
        data = request.get_json()

        product_name = data['product_name']
        category = data['category']
        color = data['color']
        size = data['size']
        price_eur = data['price_eur']
        stock = data['stock']
        product_code = data['product_code']

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        query = """
        UPDATE catalog
        SET product_name = %s,
            category = %s,
            color = %s,
            size = %s,
            price_eur = %s,
            stock = %s,
            product_code = %s
        WHERE product_id = %s
        """

        cursor.execute(query, (
            product_name,
            category,
            color,
            size,
            price_eur,
            stock,
            product_code,
            product_id
        ))

        conn.commit()

        return jsonify({"message": "Produit modifié"}), 200

    except mysql.connector.Error as err:
        return jsonify({"erreur": str(err)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Enfin, on ajoute des routes pour supprimer avec DELETE
#  
@app.route('/catalog/<int:product_id>', methods=['DELETE'])
def supprimer_vetement(product_id):
    conn = None
    cursor = None

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        query = "DELETE FROM catalog WHERE product_id = %s"

        cursor.execute(query, (product_id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "Produit introuvable"}), 404

        return jsonify({"message": "Produit supprimé"}), 200

    except mysql.connector.Error as err:
        return jsonify({"erreur": str(err)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)


