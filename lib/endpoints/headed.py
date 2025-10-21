from flask import render_template, send_from_directory, request, redirect, Response, url_for
import os
from lib.jsonificator import Jsonificator
from lib.crud import CRUD

class Headed_Endpoints(CRUD):
    def __init__(self):
        super().__init__()
        self.jsonificator = Jsonificator()
        
    def register_endpoints(self, app): 
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
        def projects():
            if request.method == "GET":
                message = request.args.get("message") if request.args.get("message") != None else ""
                all_projects = self.get_all_projects()
                return render_template("projects.html", projects=all_projects, message=message)
            else:
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
                self.create("Users",
                            (request.form["Username"], request.form["Email"], request.form["Password"], 1),
                            ("Username", "Email", "Password", "isAdmin"))
                
        @app.route("/login", methods=["GET", "POST"])
        def login():
            if request.method == "GET":
                return render_template("login.html")
            
            elif request.method == "POST":
                print(self.read("Users"))
                user_record = self.read(table="Users",
                              where_column="Username",
                              and_column="Password",
                              where_value=request.form["Username"],
                              and_value=request.form["Password"]
                              )
                if not user_record:
                    return render_template("login.html", message="User not found")
                else:
                    return render_template("login.html")
                
        
        ### "Helper" endpoint used for fetching media resources by other endpoints
        @app.route("/serve_media/<path:path>")
        def serve_media(path):
            return send_from_directory(app.config["MEDIA_FOLDER"], path)    
        
        @app.route('/collaborations', methods=["GET", "POST"])
        def collaborations():
            if request.method == "GET":
                message = request.args.get("message") if request.args.get("message") != None else ""
                collaborations = self.get_all_collaborations()
                return render_template("collaborations.html", collaborations=collaborations, message=message)
            
            elif request.method == "POST":
                if request.form["_method"] == "POST":
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
                    print(request.form)
                    message = self.create(table="Submissions",
                                          db="co2submissions.sqlite3",
                                          values=(request.form['Source'],
                                                  request.form['Fact'],
                                                  int(request.form['Co2']) * int(request.form["Co2Unit"]),
                                                  int(request.form["Timespan"]) * int(request.form["TimespanUnit"])),
                                          columns=("Source", "Fact", "Co2", "Timespan"))
                    return redirect(url_for("co2_fact_submissions", message=message))
                
                elif request.form["_method"] == "PUT":
                    message = self.update(table="Submissions",
                                          db="co2submissions.sqlite3",
                                          columns=("Source", "Fact", "Co2", "Timespan"),
                                          values=(request.form["Source"], 
                                                  request.form["Fact"], 
                                                  int(request.form['Co2']) * int(request.form["Co2Unit"]),
                                                  int(request.form["Timespan"]) * int(request.form["TimespanUnit"])),
                                          where_column="Submission_ID",
                                          where_value=request.form["ID"])
                    return redirect(url_for("co2_fact_submissions", message=message))
                
                elif request.form["_method"] == "DELETE":
                    message = self.delete(table="Submissions",
                                          db="co2submissions.sqlite3",
                                          where_column="Submission_ID",
                                          where_value=request.form["ID"])
                    return redirect(url_for("co2_fact_submissions", message=message))