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
        
        self.create_collaborations_table = """
        CREATE TABLE IF NOT EXISTS Collaborations
        (
            Collaboration_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL CHECK(typeof(Collaboration_ID) = "integer"),
            Name TEXT UNIQUE NOT NULL,
            Description TEXT UNIQUE NOT NULL
        )
        """
        
        self.create_collaborators_table = """
        CREATE TABLE IF NOT EXISTS Collaborators
        (   
            Collaborator_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL CHECK(typeof(Collaborator_ID) = 'integer'),
            Name TEXT UNIQUE NOT NULL,
            Role TEXT UNIQUE NOT NULL,
            Social_URL TEXT
        )
        """
        
        self.create_collabs_join_table = """
        CREATE TABLE IF NOT EXISTS Collabs_Join
        (
            Collaboration_ID INTEGER,
            Collaborator_ID INTEGER,
            FOREIGN KEY (Collaboration_ID) REFERENCES Collaborations(Collaboration_ID)
                ON DELETE CASCADE,
            FOREIGN KEY (Collaborator_ID) REFERENCES Collaborators(Collaborator_ID)
        )
        """
           
        self.create_co2eq_submissions = """
        CREATE TABLE IF NOT EXISTS Submissions
        (
            Submission_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL CHECK(typeof(Submission_ID) = 'integer'),
            Source TEXT UNIQUE NOT NULL,
            Fact TEXT UNIQUE NOT NULL,
            CO2 INTEGER NOT NULL,
            Timespan INTEGER NOT NULL
        )
        """