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
            Project_ID SERIAL PRIMARY KEY NOT NULL,
            Name TEXT NOT NULL,
            Description TEXT NOT NULL,
            Content TEXT
        )
        """
        
        self.create_feedbacks_table = """
        CREATE TABLE IF NOT EXISTS Feedbacks
        (
            Feedback_ID SERIAL PRIMARY KEY NOT NULL,
            Author TEXT NOT NULL,
            Feedback TEXT NOT NULL 
        )
        """
        
        self.create_sessions_table = """
        CREATE TABLE IF NOT EXISTS Sessions
        (
            Token TEXT PRIMARY KEY NOT NULL,
            Expiry INTEGER NOT NULL
        )
        """
        
        self.create_users_table = """
        CREATE TABLE IF NOT EXISTS Users
        (
            User_ID SERIAL PRIMARY KEY NOT NULL,
            Email TEXT UNIQUE NOT NULL,
            isAdmin BOOLEAN NOT NULL,
            Username TEXT UNIQUE NOT NULL,
            Password TEXT NOT NULL
        )
        """
        
        self.create_collaborations_table = """
        CREATE TABLE IF NOT EXISTS Collaborations
        (
            Collaboration_ID SERIAL PRIMARY KEY NOT NULL,
            Name TEXT UNIQUE NOT NULL,
            Description TEXT UNIQUE NOT NULL,
            Content TEXT
        )
        """
        
        self.create_collaborators_table = """
        CREATE TABLE IF NOT EXISTS Collaborators
        (   
            Collaborator_ID SERIAL PRIMARY KEY NOT NULL,
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
            Submission_ID SERIAL PRIMARY KEY NOT NULL,
            Source TEXT UNIQUE NOT NULL,
            Fact TEXT UNIQUE NOT NULL,
            Co2 REAL NOT NULL,
            Timespan INTEGER NOT NULL
        )
        """