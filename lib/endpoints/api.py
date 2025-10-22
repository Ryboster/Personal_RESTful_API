from flask import render_template, send_from_directory, request, redirect, Response, url_for
import os
from lib.jsonificator import Jsonificator
from lib.crud import CRUD

class API_Endpoints(CRUD):
    def __init__(self):
        super().__init__()
        self.jsonificator = Jsonificator()
    
    def register_endpoints(self, app):
        ### /about Endpoint
        @app.route("/api/about", methods=["GET"])
        def API_about():
            try:
                about_dict = self.jsonificator.read_from_json(os.path.join(app.config["MEDIA_FOLDER"], "json", "About.json"))
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
            
        ### /projects Endpoint
        @app.route("/api/projects", methods=["GET", "PUT", "POST", "DELETE"])
        @app.route("/api/projects/<int:project_ID>", methods=["GET", "PUT", "POST", "DELETE"])
        def API_get_projects(project_ID=None):
            if request.method == "GET":
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
            elif request.method == "POST":
                data = request.get_json()
                if not data or not "ProjectName" in data or not "ProjectDescription" in data:
                    response = Response(self.jsonificator.jsonify_error("missing fields"), status=400, mimetype="application/json")
                    response.headers["Cache-Control"] = "no-cache, no-cache"
                    return response
                project_name = data.get("ProjectName")
                description = data.get("ProjectDescription")
                try:
                    self.create("Projects",
                                values=(project_name,description),
                                columns=("name", "description"))
                    response = Response(status=201)
                    response.headers["Cache-Control"] = "no-cache, no-cache"
                    return response 
                except Exception as e:
                    return Response(self.jsonificator.jsonify_error(e), status=500, mimetype="application/json")
                
            elif request.method == "PUT":
                data = request.get_json()
                if not data or not "ProjectName" in data or not "ProjectDescription" in data:
                    response = Response(self.jsonificator.jsonify_error("missing fields"), status=400, mimetype="application/json")
                    response.headers["Cache-Control"] = "no-cache, no-cache"
                    return response 
                project_name = data.get("ProjectName") 
                description = data.get("ProjectDescription") 
                try:
                    self.update("Projects", ("Name", "Description"), "Project_ID", project_ID, (project_name, description))
                    response = Response(status=200)
                    response.headers["Cache-Control"] = "no-cache, no-cache"
                    return response 
                except Exception as e:
                    response = Response(self.jsonificator.jsonify_error(e), status=500, mimetype="application/json")

            else:
                try: 
                    self.delete("Projects", "Project_ID", project_ID)
                    response = Response(status=200)
                    response.headers["Cache-Control"] = "no-cache, no-cache"
                    return response 
                except Exception as e:
                    response = Response(self.jsonificator.jsonify_error(e), status=500, mimetype="application/json")
                    response.headers["Cache-Control"] = "no-cache, no-cache"
                    return response  
                

            
        ### /feedback Endpoint
        @app.route("/api/feedback", methods=["GET", "POST", "PUT", "DELETE"])
        def API_feedback():
            if request.method == "GET":
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
            elif request.method == "POST":
                data = request.get_json()
                if not data or not "Author" in data or not "Feedback" in data:
                    return Response(self.jsonificator.jsonify_error("missing fields"), status=400, mimetype="application/json")
                try:
                    self.create( "Feedbacks", 
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
                
        @app.route("/api/collaborations", methods=["GET", "POST", "PUT", "DELETE"])
        @app.route("/api/collaborations/<int:collaboration_ID>", methods=["GET", "POST", "PUT", "DELETE"])
        def API_collaborations(collaboration_ID=None):
            if request.method == "GET":
                try:
                    collaborations = self.get_all_collaborations()
                    collaborations["actions"] = [
                                                {"href": url_for("API_collaborations", _external=True),
                                                 "method": "GET"},
                                                {"href": url_for("API_collaborations", _external=True),
                                                 "method": "POST"},
                                                {"href": url_for("API_collaborations", _external=True),
                                                 "method": "PUT"},
                                                {"href": url_for("API_collaborations", _external=True),
                                                 "method": "DELETE"},
                                                ]
                    response = Response(self.jsonificator.convert_dict_to_json(collaborations), mimetype="application/json")
                    response.headers["Cache-Control"] = "no-cache, no-cache"
                    return response
                except Exception as e:
                    response = Response(self.jsonificator.jsonify_error(e), status=500, mimetype="application/json")
                    response.headers["Cache-Control"] = "no-cache, no-cache"
                    return response
            