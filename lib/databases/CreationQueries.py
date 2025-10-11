###
### This class stores the queries used to create the databases
### used by this application.
### In future, this will be moved off to a JSON file as
### class is kind of an overkill.
###
class Creator:
    def __init__(self):
        self.create_projects_table = """
        CREATE TABLE IF NOT EXISTS Projects
        (
            Project_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL CHECK(typeof(Project_ID) = 'integer'),
            Name TEXT NOT NULL CHECK(typeof(Name) = 'text'),
            Description TEXT NOT NULL CHECK(typeof(Description) = 'text')
        )
        """
        
        self.create_feedbacks_table = """
        CREATE TABLE IF NOT EXISTS Feedbacks
        (
            Feedback_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL CHECK(typeof(Feedback_ID) = 'integer'),
            Author TEXT NOT NULL CHECK(typeof(Author) = 'text'),
            Feedback TEXT NOT NULL CHECK(typeof(Feedback) = 'text') 
        )
        """
        
        self.create_sessions_table = """
        CREATE TABLE IF NOT EXISTS Sessions
        (
            Token TEXT PRIMARY KEY NOT NULL CHECK(typeof(Token) = 'text'),
            Expiry INTEGER NOT NULL CHECK(typeof(Expiry) = 'integer')
        )
        """
        
        self.create_users_table = """
        CREATE TABLE IF NOT EXISTS Users
        (
            User_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL CHECK(typeof(User_ID) = 'integer'),
            Email TEXT UNIQUE NOT NULL CHECK(typeof(Email) = 'text'),
            isAdmin INTEGER NOT NULL CHECK (isAdmin IN (0,1)),
            Username TEXT UNIQUE NOT NULL CHECK(typeof(Username) = 'text'),
            Password TEXT NOT NULL CHECK(typeof(Password) = 'text')
        )
        """