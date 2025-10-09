from flask import render_template, send_from_directory, request, redirect, Response, url_for
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
        def API_about():
            try:
                about_dict = self.jsonificator.read_from_json(os.path.join(self.app.config["MEDIA_FOLDER"], "json", "About.json"))
                about_dict["actions"] = [
                    {"href": url_for("API_about", _external=True),
                     "method": "GET"}
                ]
                response = Response(self.jsonificator.convert_dict_to_json(about_dict), status=200, mimetype="application/json")
                response.headers["Cache-Control"] = "no-cache, no-cache"
                return response
            except Exception:
                response = Response(self.jsonificator.jsonify_error("resource not found"), status=404, mimetype="application/json")
                response.headers["Cache-Control"] = "no-cache, no-cache"
                return response
            
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
        @self.app.route("/api/projects", methods=["GET"])
        @self.app.route("/api/projects/<int:project_ID>", methods=["GET"])
        def API_get_projects(project_ID=None):
            if project_ID:
                all_projects = self.get_all_projects()
                requested_project = {}
                for ID in all_projects.keys():
                    if project_ID == ID:
                        requested_project[project_ID] = all_projects[project_ID]
                if len(requested_project.keys()) == 0:
                    response = Response(self.jsonificator.jsonify_error("resource not found"), status=404, mimetype="application/json")
                    response.headers["Cache-Control"] = "no-cache, no-cache"
                    return response
                else:
                    requested_project["actions"] = [
                        {"href": url_for("API_get_projects", project_ID=project_ID, _external=True),
                         "method": "GET"},
                        {"href": url_for("API_edit_project", project_ID=project_ID, _external=True),
                         "method": "PUT"},
                        {"href": url_for("API_delete_project", project_ID=project_ID, _external=True),
                         "method": "DELETE"}]
                    response = Response(self.jsonificator.convert_dict_to_json(requested_project), status=200, mimetype="application/json")
                    response.headers["Cache-Control"] = "no-cache, no-cache"
                    return response
            else:
                try:
                    all_projects = self.get_all_projects()
                    all_projects["actions"] = [
                        {"href": url_for("API_get_projects", project_ID=None, _external=True),
                         "method": "GET"},
                        {"href": url_for("API_add_project", _external=True),
                         "method": "POST"}
                    ]
                    json_data = self.jsonificator.convert_dict_to_json(all_projects)
                    response = Response(json_data, status=200, mimetype="application/json")
                    response.headers["Cache-Control"] = "no-cache, no-cache"
                    return response
                except Exception as e:
                    response = Response(self.jsonificator.jsonify_error(e), status=500, mimetype="application/json")
                    response.headers["Cache-Control"] = "no-cache, no-cache"
                    return response
        
        @self.app.route("/api/projects", methods=["POST"])
        def API_add_project():
            data = request.get_json()
            if not data or not "ProjectName" in data or not "ProjectDescription" in data:
                response = Response(self.jsonificator.jsonify_error("missing fields"), status=400, mimetype="application/json")
                response.headers["Cache-Control"] = "no-cache, no-cache"
                return response
            project_name = data.get("ProjectName")
            description = data.get("ProjectDescription")
            try:
                self.create(self.PROJECTS_DB,
                            "Projects",
                            values=(project_name,description),
                            columns=("name", "description"))
                response = Response(status=201)
                response.headers["Cache-Control"] = "no-cache, no-cache"
                return response 
            except Exception as e:
                return Response(self.jsonificator.jsonify_error(e), status=500, mimetype="application/json")
        
        @self.app.route("/api/projects/<int:project_ID>", methods=["PUT"])
        def API_edit_project(project_ID):
            data = request.get_json()
            if not data or not "ProjectName" in data or not "ProjectDescription" in data:
                response = Response(self.jsonificator.jsonify_error("missing fields"), status=400, mimetype="application/json")
                response.headers["Cache-Control"] = "no-cache, no-cache"
                return response 
            project_name = data.get("ProjectName") 
            description = data.get("ProjectDescription") 
            try:
                self.update(self.PROJECTS_DB, "Projects", ("Name", "Description"), "Project_ID", project_ID, (project_name, description))
                response = Response(status=200)
                response.headers["Cache-Control"] = "no-cache, no-cache"
                return response 
            except Exception as e:
                response = Response(self.jsonificator.jsonify_error(e), status=500, mimetype="application/json")
                

            
        @self.app.route("/api/projects/<int:project_ID>", methods=["DELETE"])
        def API_delete_project(project_ID):
            try: 
                self.delete(self.PROJECTS_DB, "Projects", "Project_ID", project_ID)
                response = Response(status=200)
                response.headers["Cache-Control"] = "no-cache, no-cache"
                return response 
            except Exception as e:
                response = Response(self.jsonificator.jsonify_error(e), status=500, mimetype="application/json")
                response.headers["Cache-Control"] = "no-cache, no-cache"
                return response  
            
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
        @self.app.route("/api/feedback", methods=["GET"])
        def API_feedback():
            try: 
                feedbacks = self.get_all_feedbacks()
                feedbacks["actions"] = [
                {"href": url_for("API_feedback", _external=True),
                 "method": "GET"},
                {"href": url_for("API_feedback", _external=True),
                 "method": "POST"}]
                response = Response(self.jsonificator.convert_dict_to_json(feedbacks), mimetype="application/json")
                response.headers["Cache-Control"] = "no-cache, no-cache"
                return response  
            except Exception as e:
                response = Response(self.jsonificator.jsonify_error(e), status=500, mimetype="application/json")
                response.headers["Cache-Control"] = "no-cache, no-cache"
                return response
        
        @self.app.route("/api/feedback", methods=["POST"])
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
                response = Response(status=201)
                response.headers["Cache-Control"] = "no-cache, no-cache"
                return response
            except Exception as e:
                response = Response(self.jsonificator.jsonify_error(e), status=500, mimetype="application/json")
                response.headers["Cache-Control"] = "no-cache, no-cache"
                return response

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