import mysql.connector
from config import db_config


def get_all_articles():
    conn = None
    cursor = None

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM catalog")
        articles = cursor.fetchall()
        return articles

    except mysql.connector.Error as err:
        return {"erreur": str(err)}

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def delete_article(product_id):
    conn = None
    cursor = None

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = "DELETE FROM catalog WHERE product_id = %s"
        cursor.execute(query, (product_id,))

        if cursor.rowcount == 0:
            return {"message": "Produit introuvable"}, 404

        conn.commit()
        return {"message": "Produit supprimé"}, 200

    except mysql.connector.Error as err:
        return {"erreur": str(err)}, 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()