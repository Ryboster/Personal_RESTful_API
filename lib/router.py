from flask import render_template, send_from_directory, request, redirect, Response
import os
from lib.jsonificator import Jsonificator
from lib.crud import CRUD

###
### This script is responsible for fetching and serving static files
### based on user request.
###

STATIC_FOLDER = "static"
TEMPLATES_FOLDER = "html"


class Router(CRUD):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.register_routes()
        self.jsonificator = Jsonificator()
    
    def register_routes(self):
        @self.app.route("/")
        def index():
            return render_template("base.html")
    
        @self.app.route("/serve_media/<path:path>")
        def serve_media(path):
            return send_from_directory(self.app.config["MEDIA_FOLDER"], path)
    
        @self.app.route("/about/raw")
        def about_raw():
            return serve_media("json/About.json")
        
        @self.app.route("/about")
        def about():
            json_path = os.path.join(self.app.config["MEDIA_FOLDER"], "json/About.json")
            about = self.jsonificator.read_from_json(json_path)
            return render_template("about.html",
                                   name=about["Name"],
                                   bibliography=about["Bibliography"],
                                   occupation=about["Occupation"],
                                   education=about["Education"],
                                   description=about["Description"],
                                   goals=about["Aspirations"],
                                   skills=about["Skills"])
        
        @self.app.route("/projects/raw")
        def projects_raw():
            all_projects = self.get_all_projects()
            json_data = self.jsonificator.convert_dict_to_json(all_projects)
            return Response(json_data, mimetype="application/json")
        
        @self.app.route("/projects")
        def projects():
            all_projects = self.get_all_projects()
            return render_template("projects.html", projects=all_projects)
            
        @self.app.route("/projects/add", methods=["POST"])
        def add_project():
            project_name = request.form["ProjectName"] 
            description = request.form["ProjectDescription"]
            self.create(self.PROJECTS_DB,
                        "Projects",
                        values=(project_name,
                                description),
                        columns=("name",
                                 "description"))
            return redirect('/projects')
        
        @self.app.route("/projects/edit", methods=["POST"])
        def edit_project():
            project_ID = request.form["ProjectID"]
            project_name = request.form["ProjectName"] 
            description = request.form["ProjectDescription"]
            print(f"attempting to edit: {project_ID} with {project_name} and {description}")
            self.update(self.PROJECTS_DB, "Projects", ("Name", "Description"), "Project_ID", project_ID, (project_name, description))
            return redirect("/projects")
            
        @self.app.route("/projects/remove", methods=["POST"])
        def remove_project():
            project_ID = request.form["ProjectID"]
            self.delete(self.PROJECTS_DB, "Projects", "Project_ID", project_ID)
            return redirect("/projects")
        
        @self.app.route("/feedback")
        def feedback():
            feedbacks = self.get_all_feedbacks()
            return render_template("feedback.html", all_feedbacks=feedbacks)
        
        @self.app.route("/feedback/raw")
        def feedback_raw():
            feedbacks = self.get_all_feedbacks()
            json_data = self.jsonificator.convert_dict_to_json(feedbacks)
            return Response(json_data, mimetype="application/json")
            
        
        @self.app.route("/feedback/submit", methods=["POST"])
        def submit_feedback():
            self.create(self.FEEDBACK_DB, 
                        "Feedbacks", 
                        values=(request.form["Author"],
                                request.form["Feedback"]),
                        columns=("Author",
                                 "Feedback"))
            return redirect("/feedback")