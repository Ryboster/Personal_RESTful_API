from flask import render_template, send_from_directory, request, redirect, Response, url_for, make_response
import time
import os
from lib.jsonificator import Jsonificator
from lib.databases.dao import DAO
from lib.authenticator import Authenticator

class Headed_Endpoints(DAO):
    def __init__(self):
        super().__init__()
        self.jsonificator = Jsonificator()
        self.authy = Authenticator()
        
    def register_endpoints(self, app): 
        
        @app.before_request
        def authenticate():
            public_endpoints = {"login", "co2_fact_submissions", "logout", "register", "feedback", "serve_media", "static"}
            token = request.cookies.get("token")
            
            ### If not logged in, ignore
            if request.endpoint in public_endpoints:
                return
            if token is None and request.method == "GET":
                return
            
            ### If session expired, log out
            if token is not None and self.authy.is_session_expired(token):
                return redirect(url_for("logout"))
            
            ### If not logged in and posting, log in
            elif token is None and request.method == "POST":
                return redirect(url_for("login", message="No permission"))
            
            ### If logged in and posting, check privileges
            if request.method == "POST" and not self.authy.is_user_admin(self.get_session(token=token)["ID"]):
                return redirect(url_for("logout"))


        ### /home Endpoint
        @app.route("/", methods=["GET"])
        def index():
            return render_template("base.html")
            
        ### /about Endpoint
        @app.route("/about", methods=["GET"])
        def about():
            json_path = os.path.join(app.config["MEDIA_FOLDER"], "json/About.json")
            about = self.jsonificator.read_from_json(json_path)
            return render_template("about.html",
                                   name=about["Name"],
                                   bibliography=about["Bibliography"],
                                   occupation=about["Occupation"],
                                   education=about["Education"],
                                   description=about["Description"],
                                   goals=about["Aspirations"],
                                   skills=about["Skills"])
            
        ### /projects Endpoint
        @app.route("/projects", methods=["GET", "POST"])
        @app.route("/projects/<int:project_ID>", methods=["GET", "POST"])
        def projects(project_ID=None):
            if request.method == "GET":
                if project_ID == None:
                    message = request.args.get("message") if request.args.get("message") != None else ""
                    all_projects = self.get_all_projects()
                    return render_template("projects.html", projects=all_projects, message=message)
                else:
                    
                    content = self.read(table="Projects",
                                        selection="Content",
                                        where_column=("Project_ID"),
                                        where_value=project_ID)[0][0]
                    return render_template("item_view.html", content=content)
            else:
                if self.authy.is_session_expired(request.cookies.get("token")):
                    return redirect(url_for("logout"))
                if not self.authy.is_user_admin(self.get_session(request.cookies.get("token"))["ID"]):
                    return redirect(url_for("projects", message="No."))
                
                if request.form["_method"] == "POST":
                    message = self.create("Projects",
                                          values=(request.form["Name"] ,request.form["Description"]),
                                          columns=("name","description"))
                    return redirect(url_for("projects", message=message))
            
                elif request.form["_method"] == "PUT":          
                    message = self.update(table="Projects", 
                                          columns=("Name", "Description"),
                                          where_column="Project_ID",
                                          where_value=request.form["ID"],
                                          values=(request.form["Name"], request.form["Description"]))
                    return redirect(url_for("projects", message=message))
                    
                elif request.form["_method"] == "DELETE":
                    message= self.delete(table="Projects",
                                         where_column="Project_ID",
                                         where_value=request.form["ID"])
                    return redirect(url_for("projects", message=message))
    
        
        
        ### /feedback Endpoint
        @app.route("/feedback", methods=["GET", "POST"])
        def feedback():
            if request.method == "GET":
                message = request.args.get("message") if request.args.get("message") != None else ""
                feedbacks = self.get_all_feedbacks()
                return render_template("feedback.html", all_feedbacks=feedbacks, message=message)
            else:
                if request.form["_method"] == "POST":
                    message=self.create("Feedbacks", 
                                        values=(request.form["Author"],
                                                request.form["Feedback"]),
                                        columns=("Author",
                                                 "Feedback"))
                    return redirect(url_for("feedback", message=message))
                elif request.form["_method"] == "DELETE":
                    message = self.delete("Feedbacks",
                                          where_column="Feedback_ID",
                                          where_value=request.form["ID"])
                    return redirect(url_for("feedback", message=message))
        
        
        
        @app.route("/register", methods=["GET", "POST"])
        def register():
            if request.method == "GET":
                return render_template("register.html")
            elif request.method == "POST":
                message = self.create("Users",
                            (request.form["Username"], request.form["Email"], request.form["Password"], False),
                            ("Username", "Email", "Password", "isAdmin"))
                return render_template("register.html", message=message) 
                
        @app.route("/login", methods=["GET", "POST"])
        def login():
            if request.method == "GET":
                print(self.read(table="Sessions",
                          where_column="Token",
                          where_value=request.cookies.get("token")))
                return render_template("login.html")
            
            elif request.method == "POST":
                _username = request.form["Username"]
                _password = request.form["Password"]
                
                ### Verify that username and password are correct
                user_record = self.get_user(username=_username, password=_password)
                if not "ID" in user_record:
                    return redirect(url_for("login",message="wrong credentials" ) )
                
                if self.authy.is_user_logged(user_record["ID"]):
                    self.delete(table="Sessions",
                                where_column="User_ID",
                                where_value=user_record["ID"])
                    
                token = self.authy.generate_hash()
                expiry_time = int(time.time()) + self.authy.EXPIRY
                self.create(table="Sessions",
                            columns=("User_ID", "Token", "Expiry"),
                            values=(user_record["ID"], token, expiry_time))
                
                response = make_response(redirect(url_for("login",message="Success"))) 
                response.set_cookie("token", token, max_age=self.authy.EXPIRY)
                response.set_cookie("username", user_record["username"], max_age=self.authy.EXPIRY)
                return response
            return response
        
        @app.route("/logout", methods=["GET"])
        def logout():
            response = make_response(redirect(url_for("login",message="You are logged out!") ))
            self.delete(table="Sessions",
                        where_column="Token",
                        where_value=request.cookies.get("token"))
            response.set_cookie("token", '', max_age=0)
            response.set_cookie("username", '', max_age=0)
            return response
        
        @app.route("/serve_backup/<path:filename>", methods=["GET"])
        def serve_backup(filename):
            session = self.get_session(request.cookies.get("token"))
            if not "ID" in session:
                return redirect(url_for("backup", message="Insufficient privileges!"))
            if self.authy.is_user_admin(session["ID"]):
                return send_from_directory(os.path.join(self.BACKUP_DIR), filename)
            else:
                return redirect(url_for("backup", message="Insufficient privileges!") )
                
            
            
        ### "Helper" endpoint used for fetching media resources by other endpoints
        @app.route("/serve_media/<path:path>")
        def serve_media(path):
            return send_from_directory(app.config["MEDIA_FOLDER"], path)    
        
        @app.route('/collaborations', methods=["GET", "POST"])
        @app.route('/collaborations/<int:collaboration_ID>', methods=["GET", "POST"])
        def collaborations(collaboration_ID=None):
            if request.method == "GET":
                if collaboration_ID == None:
                    message = request.args.get("message") if request.args.get("message") != None else ""
                    collaborations = self.get_all_collaborations()
                    return render_template("collaborations.html", collaborations=collaborations, message=message)
                else:                    
                    content = self.read(table="Collaborations",
                                        selection="Content",
                                        where_column="Collaboration_ID",
                                        where_value=collaboration_ID)[0][0]
                    return render_template("item_view.html", content=content)
            
            elif request.method == "POST":
                if collaboration_ID != None:
                    print(request.form["Content"])
                    self.update(table="Collaborations",
                                columns=("Content",),
                                values=(request.form["Content"],),
                                where_column="Collaboration_ID",
                                where_value=collaboration_ID)
                    return redirect(url_for("collaborations", collaboration_ID=collaboration_ID))
                
                if request.form["_method"] == "POST":
                    if collaboration_ID == None:
                        message = self.create(table="Collaborations",
                                              values=(request.form["Name"],request.form["Description"]),
                                              columns=("Name","Description"))
                        return redirect(url_for("collaborations",message=message))
                
                elif request.form['_method'] == "PUT":
                    message = self.update(table="Collaborations",
                                     columns=("Name","Description"),
                                     values=(request.form["Name"],request.form["Description"]),
                                     where_column="Collaboration_ID",
                                     where_value=request.form["ID"])
                    return redirect(url_for("collaborations", message=message))
                    
                elif request.form["_method"] == "DELETE":
                    message = self.delete(table="Collaborations", 
                                     where_column="Collaboration_ID", 
                                     where_value=request.form["ID"])
                    return redirect(url_for("collaborations", message=message))
        
        @app.route("/collaborators", methods=["GET", "POST"])
        def collaborators():
            if request.method == "GET":
                message = request.args.get("message") if request.args.get("message") != None else ""
                collaborators = self.get_all_collaborators()
                return render_template("collaborators.html", collaborators=collaborators, message=message)
                
            else:
                if request.form["_method"] == "POST":
                    message = self.create(table="Collaborators",
                                          values=(request.form["Name"],request.form["Role"],request.form["Social"]),
                                          columns=("Name", "Role", "Social_URL"))
                    return redirect(url_for("collaborators", message=message))
                elif request.form["_method"] == "PUT":
                    message = self.update(table="Collaborators",
                                          columns=("Name", "Role", "Social_URL"),
                                          where_column="Collaborator_ID",
                                          where_value=request.form["ID"],
                                          values=(request.form["Name"],request.form["Role"],request.form["Social"]))
                    return redirect(url_for("collaborators", message=message))
                elif request.form["_method"] == "DELETE":
                    message = self.delete(table="Collaborators",
                                          where_column="Collaborator_ID",
                                          where_value=request.form["ID"])
                    return redirect(url_for("collaborators", message=message))

        @app.route("/collaborations/co2_fact_submissions", methods=["GET", "POST"])
        def co2_fact_submissions():
            if request.method == "GET":
                message = request.args.get("message") if request.args.get("message") != None else ""
                submissions = self.get_all_co2_submissions()
                return render_template("co2_fact_submissions.html", submissions=submissions, message=message)
            else:
                if request.form["_method"] == "POST":
                    message = self.create(table="Submissions",
                                          columns=("Source", "Fact", "Co2", "Timespan"),
                                          values=(request.form['Source'],
                                                  request.form['Fact'],
                                                  float(request.form['Co2']) * float(request.form["Co2Unit"]),
                                                  float(request.form["Timespan"]) * float(request.form["TimespanUnit"])))
                    return redirect(url_for("co2_fact_submissions", message=message))
                
                elif request.form["_method"] == "PUT":
                    message = self.update(table="Submissions",
                                          columns=("Source", "Fact", "Co2", "Timespan"),
                                          values=(request.form["Source"], 
                                                  request.form["Fact"], 
                                                  float(request.form['Co2']) * float(request.form["Co2Unit"]),
                                                  float(request.form["Timespan"]) * float(request.form["TimespanUnit"])),
                                          where_column="Submission_ID",
                                          where_value=request.form["ID"])
                    return redirect(url_for("co2_fact_submissions", message=message))
                
                elif request.form["_method"] == "DELETE":
                    message = self.delete(table="Submissions",
                                          where_column="Submission_ID",
                                          where_value=request.form["ID"])
                    return redirect(url_for("co2_fact_submissions", message=message))
                
        @app.route("/backup", methods=["GET", "POST"])
        def backup():
            if request.method == "GET":
                backup_files = os.listdir(self.BACKUP_DIR)
                return render_template("backups.html", files=backup_files)
            else:
                if request.form["_method"] == "POST":
                    self.backup_database()
                    return redirect(url_for("backup", message="Success!"))
                elif request.form["_method"] == "DELETE":
                    os.remove(os.path.join(self.BACKUP_DIR, request.form["filename"]))
                    return redirect(url_for("backup", message="Success!"))
                elif request.form["_method"] == "ROLLBACK":
                    message = self.rollback_database(request.form["filename"])
                    return redirect(url_for("backup", message="Success!"))