import os
from pathlib import Path
from lib.databases.connector import Connector

###
### This class initializes the database schema
###

SCHEMA_DIR = os.path.join(os.getcwd(), "lib", "databases", "schema")
SCHEMAS_ORDERED = [
    'create_projects.sql',
    'create_users.sql',
    'create_sessions.sql',
    'create_submissions.sql',
    'create_feedbacks.sql',
    'create_collaborators.sql',
    'create_collaborations.sql',
    'create_collabs_join.sql',
]

class Creator(Connector):
    def __init__(self):
        self.initialize_databases()
        
    def initialize_databases(self):        
        self.open_connection()
        for query in self.get_creation_queries():
            self.cursor.execute(query)
        self.close_connection()
        
    def get_creation_queries(self):
        queries = []
        for sql_filename in SCHEMAS_ORDERED:
            queries.append(Path(os.path.join(SCHEMA_DIR, sql_filename)).read_text(encoding="utf-8"))
        return queries