from lib.databases.crud import CRUD


###
### This class extends CRUD for higher-level functionality.
###

class DAO(CRUD):        
    def get_session(self, token=None, user_ID=0):
        session_data = {}
        if user_ID == 0:
            session_record = self.read(table="Sessions",
                                       where_column="Token",
                                       where_value=token)
        else:
            session_record = self.read(table="Sessions",
                                       where_column="User_ID",
                                       where_value=user_ID)
        for record in session_record:
            session_data["ID"] = record[0]
            session_data["token"] = record[1]
            session_data["expiry"] = record[2]
        return session_data
    
    def get_user(self, _user_ID = 0, username=None, password=None ):
        user_data = {}
        if _user_ID == 0:
            user_record = self.read(table="Users",
                                    where_column="Username",
                                    and_column="Password",
                                    where_value=username,
                                    and_value=password)
        else:
            user_record = self.read(table="Users",
                                    where_column="User_ID",
                                    where_value=_user_ID)
        try:
            for data in user_record:
                user_data["ID"] = data[0]
                user_data["email"] = data[1]
                user_data["isAdmin"] = data[2]
                user_data["username"] = data[3]
                user_data["password"] = data[4]
        except Exception:
            pass

        return user_data        
    
    def get_all_projects(self):
        all_projects = {}
        for record in self.read(table="Projects"):    
            all_projects[record[0]] = {}
            all_projects[record[0]]["project_ID"] = record[0]
            all_projects[record[0]]['project_name'] = record[1]
            all_projects[record[0]]['project_description'] = record[2]
            all_projects[record[0]]["Content"] = record[3]
        return all_projects
    
    def get_all_feedbacks(self):
        all_feedbacks = {}
        for record in self.read(table="Feedbacks"):
            all_feedbacks[record[0]] = {}
            all_feedbacks[record[0]]["feedback_ID"] = record[0]
            all_feedbacks[record[0]]["author"] = record[1]
            all_feedbacks[record[0]]["feedback"] = record[2]
        return all_feedbacks
    
    def get_all_collaborations(self):
        all_collaborations = {}
        for record in self.read(table="Collaborations"):
            all_collaborations[record[0]] = {}
            all_collaborations[record[0]]["Name"] = record[1]
            all_collaborations[record[0]]["Description"] = record[2]
            all_collaborations[record[0]]["Content"] = record[3]
        return all_collaborations
    
    def get_all_collaborators(self):
        all_collaborators = {}
        for record in self.read(table="Collaborators"):
            all_collaborators[record[0]] = {}
            all_collaborators[record[0]]["Name"] = record[1]
            all_collaborators[record[0]]["Role"] = record[2]
            all_collaborators[record[0]]["Social_URL"] = record[3]
        return all_collaborators
    
    def get_all_co2_submissions(self):
        submissions = {}
        for record in self.read(table="Submissions"):
            submissions[record[0]] = {}
            submissions[record[0]]["Source"] = record[1]
            submissions[record[0]]["Fact"] = record[2]
            submissions[record[0]]["Co2"] = record[3]
            submissions[record[0]]["Timespan"] = record[4]
        return submissions