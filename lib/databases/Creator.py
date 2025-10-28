import os
from pathlib import Path
import psycopg2

###
### This class initializes the database schema
###

class Creator():
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname=     os.getenv('DB_NAME', "example"),
            user=       os.getenv('DB_USERNAME', "guest"),
            password=   os.getenv('DB_PASSWORD', "123"),
            host=       os.getenv("DB_HOST", "localhost"),
            port=       5432
        )
        self.cursor = self.connection.cursor()
        self.initialize_databases()
        
    def initialize_databases(self):
        queries = []
        for sql_filename in os.listdir(os.path.join(os.getcwd(), "schema")):
            queries.apend(Path(os.listdir(os.getcwd(), "schema", sql_filename)).read_text(encoding="utf-8"))
        
        for query in queries:
            self.execute(query)
        self.cursor.commit()
        self.cursor.close()
        self.close_connection()