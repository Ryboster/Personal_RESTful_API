###
### This class stores the queries used to create the databases
### used by this application.
### In future, this will be moved off to a JSON file as
### class is kind of an overkill.
###
class Creator:
    def __init__(self):
        self.create_projects_query = """
        CREATE TABLE IF NOT EXISTS Projects
        (
            Project_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL Check(typeof(Project_ID) = 'integer'),
            Name TEXT NOT NULL Check(typeof(Name) = 'text'),
            Description TEXT NOT NULL Check(typeof(Description) = 'text')
        )
        """
        
        self.create_feedbacks_query = """
        CREATE TABLE IF NOT EXISTS Feedbacks
        (
            Feedback_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL Check(typeof(Feedback_ID) = 'integer'),
            Author TEXT NOT NULL Check(typeof(Author) = 'text'),
            Feedback TEXT NOT NULL Check(typeof(Feedback) = 'text') 
        )
        """