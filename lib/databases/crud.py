from lib.databases.connector import Connector
import re

###
### This class is responsible for all operations done on databases.
### For convenience's sake it is CRUD+ as not only does it define
### methods used for reading, creating, updating, and deleting entries,
### but also methods for targetted retrieval and transformation.
### It is used exclusively by the Router class.
### 
### The database used here is PostgreSQL.
### To access the database, this class expects the following environment variables:
### DB_NAME, DB_USERNAME, DB_PASSWORD, DB_HOST
###

class CRUD(Connector):
    def __init__(self):
        super().__init__()
        
    def create(self, table: str, values=(), columns=()):
        self.open_connection()
        if columns == ():
            secureQuery = f"INSERT INTO {table} VALUES ({self.get_values_placeholder(values)})"
        else:
            columns_str = f"({', '.join(columns)})"
            secureQuery = f"INSERT INTO {table} {columns_str} VALUES ({self.get_values_placeholder(values)})"
        try:
            self.cursor.execute(secureQuery, values)
            self.close_connection()  
        except Exception as e:
            return e
        
    def read(self, table: str, selection="*", where_column=None, where_value=None, and_column="", and_value=""):
        def is_safe_identifier(name):            
            return bool(re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', name))        
        if not is_safe_identifier(table):
            raise ValueError(f"Invalid table name: {table}")
        if selection != "*" and not all(is_safe_identifier(s.strip()) for s in selection.split(",")):
            raise ValueError(f"Invalid selection columns: {selection}")
        if where_column is not None and not is_safe_identifier(where_column):
            raise ValueError(f"Invalid WHERE column: {where_column}")
        self.open_connection()
        try:
            if where_column is None:
                query = f"SELECT {selection} FROM {table}"
                self.cursor.execute(query)
            elif where_column != None and not and_column:
                query = f"SELECT {selection} FROM {table} WHERE {where_column} = %s"
                self.cursor.execute(query, (where_value,))
            else:
                query = f"SELECT {selection} FROM {table} WHERE {where_column} = %s AND {and_column} = %s"
                self.cursor.execute(query, (where_value, and_value))
        except Exception as e:
            return e
            
        result = self.cursor.fetchall()
        self.close_connection()
        return result
        
    def update(self, table: str, columns, where_column: str, where_value, values):
        self.open_connection()
        set_clause = ", ".join([f"{col} = %s" for col in columns])
        query = f"UPDATE {table} SET {set_clause} WHERE {where_column} = %s"
        
        if isinstance(values, tuple):
            values = list(values)
        elif not isinstance(values, list):
            values = [values]
        parameters = values + [where_value]
        
        self.cursor.execute(query, parameters)
        self.close_connection()

    def delete(self, table: str, where_column: str, where_value, and_column="", and_value=""):
        self.open_connection()
        if not and_column:
            query = f"DELETE FROM {table} WHERE {where_column} = %s"
            self.cursor.execute(query, (where_value,))
        else:
            query = f"DELETE FROM {table} WHERE {where_column} = %s AND {where_column} = %s"
            self.cursor.execute(query, (where_value, and_value,))
        self.close_connection()
        
    def get_values_placeholder(self, values, placeholder="%s"):
        for i in range(0, len(values) - 1):
            placeholder += ",%s"
        return placeholder
        
        
if __name__ == "__main__":
    CRUD()