import mysql.connector

class ORM:
    def connect (self):
        return mysql.connector.connect(
            password="Prune59.",
            database=self.database
        )

