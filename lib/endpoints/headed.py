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
        @app.route("/projects", methods=["GET"])
        def projects():
            all_projects = self.get_all_projects()
            return render_template("projects.html", projects=all_projects)
            
        @app.route("/projects/add", methods=["POST"])
        def add_project():
            project_name = request.form["ProjectName"] 
            description = request.form["ProjectDescription"]
            self.create("Projects",
                        values=(project_name,
                                description),
                        columns=("name",
                                 "description"))
            return redirect('/projects')
        
        @app.route("/projects/edit", methods=["POST"])
        def edit_project():
            project_ID = request.form["ProjectID"]
            project_name = request.form["ProjectName"] 
            description = request.form["ProjectDescription"]
            print(f"attempting to edit: {project_ID} with {project_name} and {description}")
            self.update("Projects", ("Name", "Description"), "Project_ID", project_ID, (project_name, description))
            return redirect("/projects")
            
        @app.route("/projects/remove", methods=["POST"])
        def remove_project():
            project_ID = request.form["ProjectID"]
            self.delete("Projects", "Project_ID", project_ID)
            return redirect("/projects")

        ### /feedback Endpoint
        @app.route("/feedback")
        def feedback():
            feedbacks = self.get_all_feedbacks()
            return render_template("feedback.html", all_feedbacks=feedbacks)
        
        @app.route("/feedback/submit", methods=["POST"])
        def submit_feedback():
            self.create("Feedbacks", 
                        values=(request.form["Author"],
                                request.form["Feedback"]),
                        columns=("Author",
                                 "Feedback"))
            return redirect("/feedback")
        
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
                print(self.read("Users", "*", "Username", request.form["Username"]))
        
        ### "Helper" endpoint used for fetching media resources by other endpoints
        @app.route("/serve_media/<path:path>")
        def serve_media(path):
            return send_from_directory(app.config["MEDIA_FOLDER"], path)    