import sqlite3
import os
from lib.databases.CreationQueries import Creator


###
### This class is responsible for all operations done on databases.
### For convenience's sake it is CRUD+ as not only does it define
### methods used for reading, creating, updating, and deleting entries,
### but also methods for targetted retrieval and transformation.
### It is used exclusively by the Router class.
### 

class CRUD(Creator):    
    def __init__(self):
        self.DATABASE_DIR = "databases"
        self.PROJECTS_DB = "projects.sqlite3"
        self.FEEDBACK_DB = "feedbacks.sqlite3"
        super().__init__()
        self.initialize_databases()
        
    def initialize_databases(self):
        self.open_connection(self.PROJECTS_DB)
        self.execute_query(self.create_projects_query)
        self.close_connection()
        self.open_connection(self.FEEDBACK_DB)
        self.execute_query(self.create_feedbacks_query)
        self.close_connection()
        
    def open_connection(self, db):
        path = os.path.join(os.getcwd(), "lib", self.DATABASE_DIR, db)
        self.connection = sqlite3.connect(path)
        self.connection.execute('PRAGMA foreign_keys = ON')
        self.cursor = self.connection.cursor()
        
    def close_connection(self):
        self.connection.commit()
        self.connection.close()
        
    def execute_query(self, query):
        self.cursor.execute(query)
        
    def create(self, database, table: str, values=(), columns=()):
        self.open_connection(database)
        if columns == ():
            secureQuery = f"INSERT INTO {table} VALUES ({self.get_values_placeholder(values)})"
        else:
            columns_str = f"({', '.join(columns)})"
            secureQuery = f"INSERT INTO {table} {columns_str} VALUES ({self.get_values_placeholder(values)})"
        
        self.execute_query_securely(secureQuery, values)
        self.close_connection()
        
    def read(self, database, table:str, selection="*", whereColumn=None, whereValue=None):
        self.open_connection(database)
        if whereColumn is None:
            self.cursor.execute(f"SELECT {selection} FROM {table}")
            result = self.cursor.fetchall()
        else:
            query = f"SELECT {selection} FROM {table} WHERE {whereColumn} = ?"
            self.cursor.execute(query, (whereValue,))
            result = self.cursor.fetchall()
        self.close_connection()
        return result
    
    def update(self, database, table: str, columns, whereColumn: str, whereValue, values):
        self.open_connection(database)
        set_clause = ", ".join([f"{col} = ?" for col in columns])
        query = f"UPDATE {table} SET {set_clause} WHERE {whereColumn} = ?"
        
        if isinstance(values, tuple):
            values = list(values)
        elif not isinstance(values, list):
            values = [values]
        parameters = values + [whereValue]
        
        self.execute_query_securely(query, parameters)
        self.close_connection()

    def delete(self, database, table: str, whereColumn: str, whereValue):
        self.open_connection(database)
        query = f"DELETE FROM {table} WHERE {whereColumn} = ?"
        self.execute_query_securely(query, (whereValue,))
        self.close_connection()
        
    def get_values_placeholder(self, values, placeholder="?"):
        for i in range(0, len(values) - 1):
            placeholder += ",?"
        return placeholder

    def execute_query_securely(self, query, params=()):
        ''' Handle queries securely '''
        try:
            self.cursor.execute(query, params)
        except sqlite3.Error as e:
            return False
        return True
        
    def get_all_projects(self):
        all_projects = {}
        for record in self.read(self.PROJECTS_DB, "Projects"):    
            all_projects[record[0]] = {}
            all_projects[record[0]]['project_name'] = record[1]
            all_projects[record[0]]['project_description'] = record[2]
        return all_projects
    
    def get_all_feedbacks(self):
        all_feedbacks = {}
        for record in self.read(self.FEEDBACK_DB, "Feedbacks"):
            all_feedbacks[record[0]] = {}
            all_feedbacks[record[0]]["author"] = record[1]
            all_feedbacks[record[0]]["feedback"] = record[2]
        return all_feedbacks
        
if __name__ == "__main__":
    CRUD()