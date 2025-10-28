import psycopg2
import os

##
## This class defines methods used for connecting with the database.
##

class Connector:    
    def open_connection(self):
        self.connection = psycopg2.connect(
            dbname=     os.getenv('DB_NAME', "example"),
            user=       os.getenv('DB_USERNAME', "guest"),
            password=   os.getenv('DB_PASSWORD', "123"),
            host=       os.getenv("DB_HOST", "localhost"),
            port=       5432
        )
        self.cursor = self.connection.cursor()
        
    def close_connection(self):
        self.connection.commit()
        self.connection.close()