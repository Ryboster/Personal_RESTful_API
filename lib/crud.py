import psycopg2
import os
from lib.databases.CreationQueries import Creator
import re
import hashlib
import json

###
### This class is responsible for all operations done on databases.
### For convenience's sake it is CRUD+ as not only does it define
### methods used for reading, creating, updating, and deleting entries,
### but also methods for targetted retrieval and transformation.
### It is used exclusively by the Router class.
### 

USERNAME = ""
PASSWORD = ""

if os.path.exists(os.path.join(os.getcwd(), "db_creds.json")):
    with open (os.path.join(os.getcwd(), "db_creds.json"), "r") as file:
        creds = json.loads(file.read())
        USERNAME = creds["USERNAME"]
        PASSWORD = creds["PASSWORD"]
else:
    print("db_creds.json not found. Exitting ...")
    exit(1)

class CRUD(Creator):    
    def __init__(self):
        super().__init__()
        self.initialize_databases()
        
    def initialize_databases(self):
        self.open_connection()
        self.cursor.execute(self.create_projects_table)
        self.cursor.execute(self.create_feedbacks_table)
        self.cursor.execute(self.create_sessions_table)
        self.cursor.execute(self.create_users_table)
        self.cursor.execute(self.create_collaborations_table)
        self.cursor.execute(self.create_collaborators_table)
        self.cursor.execute(self.create_co2eq_submissions)
        self.close_connection()
        
    def open_connection(self):
        self.connection = psycopg2.connect(
            dbname="restful_api_database",
            user=USERNAME,
            password=PASSWORD,
            host="localhost",
            port=5432
        )
        self.cursor = self.connection.cursor()
        
    def close_connection(self):
        self.connection.commit()
        self.connection.close()
        
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
        
    def get_all_projects(self):
        all_projects = {}
        for record in self.read("Projects"):    
            all_projects[record[0]] = {}
            all_projects[record[0]]["project_ID"] = record[0]
            all_projects[record[0]]['project_name'] = record[1]
            all_projects[record[0]]['project_description'] = record[2]
            all_projects[record[0]]["Content"] = record[3]
        return all_projects
    
    def get_all_feedbacks(self):
        all_feedbacks = {}
        for record in self.read("Feedbacks"):
            all_feedbacks[record[0]] = {}
            all_feedbacks[record[0]]["feedback_ID"] = record[0]
            all_feedbacks[record[0]]["author"] = record[1]
            all_feedbacks[record[0]]["feedback"] = record[2]
        return all_feedbacks
    
    def get_all_collaborations(self):
        all_collaborations = {}
        for record in self.read("Collaborations"):
            all_collaborations[record[0]] = {}
            all_collaborations[record[0]]["Name"] = record[1]
            all_collaborations[record[0]]["Description"] = record[2]
            all_collaborations[record[0]]["Content"] = record[3]
        return all_collaborations
    
    def get_all_collaborators(self):
        all_collaborators = {}
        for record in self.read("Collaborators"):
            all_collaborators[record[0]] = {}
            all_collaborators[record[0]]["Name"] = record[1]
            all_collaborators[record[0]]["Role"] = record[2]
            all_collaborators[record[0]]["Social_URL"] = record[3]
        return all_collaborators
    
    def get_all_co2_submissions(self):
        submissions = {}
        for record in self.read(table="Submissions", db="co2submissions.sqlite3"):
            submissions[record[0]] = {}
            submissions[record[0]]["Source"] = record[1]
            submissions[record[0]]["Fact"] = record[2]
            submissions[record[0]]["Co2"] = record[3]
            submissions[record[0]]["Timespan"] = record[4]
        return submissions
    
    def generateSessionToken(self):
        randomBytes = os.urandom(32)
        sha256 = hashlib.sha256(randomBytes)
        return sha256.hexdigest()

    def generateHash(self, username:str, password:str):
        combinedBytes = str(username + password).encode("utf-8")
        hashedBytes = hashlib.sha256(combinedBytes)
        return hashedBytes.hexdigest()
    
    def areCredsValid(self, enteredHash):
        allUsers = self.read("users", "Users")
        for username, password, storedHash in allUsers:
            if (enteredHash == storedHash):
                return True
        return False
    
    def isSessionValid(self, request):
        activeSessions = self.read("sessions", "sessions")
        enteredID = request.COOKIES.get("ID")
        enteredSessionToken = request.COOKIES.get("SESH_TOKEN")
        for id, token, time in activeSessions:
            if id == enteredID and enteredSessionToken == token:
                return True
        return False
        
if __name__ == "__main__":
    CRUD()