from flask import render_template, send_from_directory, request, redirect, Response
import os
from lib.jsonificator import Jsonificator
from lib.crud import CRUD

###
### This script is responsible for fetching and serving static files
### based on user request. It is the core of this application.
### Each endpoint has a /raw "subendpoint" which can be used to fetch
### the endpoint's content in JSON format.
###

STATIC_FOLDER = "static"
TEMPLATES_FOLDER = "html"

class Router(CRUD):
    def __init__(self, app):
        super().__init__()                  # Initialize CRUD.
        self.app = app                      # Take ownership of the app object.
        self.register_routes()              # Assign responses to the app object.
        self.jsonificator = Jsonificator()  # Instantiate helper class.
    
    def register_routes(self):
        ### /home Endpoint
        ###
        @self.app.route("/", methods=["GET"])
        def index():
            return render_template("base.html")
    
        ### /about Endpoint
        ### API
        ##
        @self.app.route("/api/about", methods=["GET"])
        def api_about():
            try:
                return serve_media("json/About.json")
            except Exception:
                return Response(self.jsonificator.jsonify_response("resource not found"), status=404, mimetype="application/json")
            
        ### /about Endpoint
        ### Headed
        ##
        @self.app.route("/about", methods=["GET"])
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
            
        ### /projects Endpoint
        ### API
        ##
        @self.app.route("/api/projects", methods=["GET"])
        def API_get_projects():
            try:
                all_projects = self.get_all_projects()
                json_data = self.jsonificator.convert_dict_to_json(all_projects)
                return Response(json_data, status=200, mimetype="application/json")
            except Exception as e:
                return Response(self.jsonificator.jsonify_error(e), status=500, mimetype="application/json")
        
        @self.app.route("/api/projects", methods=["POST"])
        def API_add_project():
            data = request.get_json()
            if not data or not "ProjectName" in data or not "ProjectDescription" in data:
                return Response(self.jsonificator.jsonify_error("missing fields"), status=400, mimetype="application/json")
            project_name = data.get("ProjectName")
            description = data.get("ProjectDescription")
            try:
                self.create(self.PROJECTS_DB,
                            "Projects",
                            values=(project_name,description),
                            columns=("name", "description"))
                return Response(status=201)
            except Exception as e:
                return Response(self.jsonificator.jsonify_error(e), status=500, mimetype="application/json")
        
        @self.app.route("/api/projects/<int:project_ID>", methods=["PUT"])
        def API_edit_project(project_ID):
            data = request.get_json()
            if not data or not "ProjectName" in data or not "ProjectDescription" in data:
                return Response(self.jsonificator.jsonify_error("missing fields"), status=400, mimetype="application/json")
            project_name = data.get("ProjectName") 
            description = data.get("ProjectDescription") 
            try:
                self.update(self.PROJECTS_DB, "Projects", ("Name", "Description"), "Project_ID", project_ID, (project_name, description))
                return Response(status=200)
            except Exception as e:
                return Response(self.jsonificator.jsonify_error(e), status=500, mimetype="application/json")
            
        @self.app.route("/api/projects/<int:project_ID>", methods=["DELETE"])
        def API_delete_project(project_ID):
            try: 
                self.delete(self.PROJECTS_DB, "Projects", "Project_ID", project_ID)
                return Response(status=200)
            except Exception as e:
                return Response(self.jsonificator.jsonify_error(e), status=500, mimetype="application/json")
            
        ### /projects Endpoint
        ### Headed
        ##
        @self.app.route("/projects", methods=["GET"])
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
        
        ### /feedback Endpoint
        ### API
        ##
        @self.app.route("api/feedback", methods=["GET"])
        def API_feedback():
            try: 
                feedbacks = self.get_all_feedbacks()
                json_data = self.jsonificator.convert_dict_to_json(feedbacks)
                return Response(json_data, mimetype="application/json")
            except Exception as e:
                return Response(self.jsonificator.jsonify_error(e), status=500, mimetype="application/json")
        
        @self.app.route("api/feedback", methods=["POST"])
        def API_add_feedback():
            data = request.get_json()
            if not data or not "Author" in data or not "Feedback" in data:
                return Response(self.jsonificator.jsonify_error("missing fields"), status=400, mimetype="application/json")
            try:
                self.create(self.FEEDBACK_DB, 
                            "Feedbacks", 
                            values=(data.get("Author"),
                                    data.get("Feedback")),
                            columns=("Author",
                                     "Feedback"))
                return Response(status=201)
            except Exception as e:
                return Response(self.jsonificator.jsonify_error(e), status=500, mimetype="application/json")

        ### /feedback Endpoint
        ### Headed
        ##
        @self.app.route("/feedback")
        def feedback():
            feedbacks = self.get_all_feedbacks()
            return render_template("feedback.html", all_feedbacks=feedbacks)
        
        @self.app.route("/feedback/submit", methods=["POST"])
        def submit_feedback():
            self.create(self.FEEDBACK_DB, 
                        "Feedbacks", 
                        values=(request.form["Author"],
                                request.form["Feedback"]),
                        columns=("Author",
                                 "Feedback"))
            return redirect("/feedback")
        
        ### "Helper" endpoint used for fetching media resources by other endpoints
        @self.app.route("/serve_media/<path:path>")
        def serve_media(path):
            return send_from_directory(self.app.config["MEDIA_FOLDER"], path)