from flask import render_template, send_from_directory, request, redirect, url_for
import os
from lib.jsonificator import Jsonificator
from lib.databases.crud import CRUD
from werkzeug.wrappers import Response

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
                return return_dict(data=about_dict, status=200)
            except Exception:
                return return_status(message="resource not found", status=404)
            
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
                        return return_status(message="resource not found", status=404)
                    
                    else:
                        requested_project["actions"] = [
                            {"href": url_for("API_get_projects", project_ID=project_ID, _external=True),
                             "method": "GET"},
                            {"href": url_for("API_edit_project", project_ID=project_ID, _external=True),
                             "method": "PUT"},
                            {"href": url_for("API_delete_project", project_ID=project_ID, _external=True),
                             "method": "DELETE"}]
                        return return_dict(requested_project, status=200)

                else:
                    try:
                        all_projects = self.get_all_projects()
                        all_projects["actions"] = [
                            {"href": url_for("API_get_projects", project_ID=None, _external=True),
                             "method": "GET"},
                            {"href": url_for("API_add_project", _external=True),
                             "method": "POST"}
                        ]
                        return return_dict(all_projects, status=200)
                    
                    except Exception as e:
                        return throw_exception(e=e)

            elif request.method == "POST":
                data = request.get_json()
                if not data or not "ProjectName" in data or not "ProjectDescription" in data:
                    return return_status("missing fields", status=400)
                
                project_name = data.get("ProjectName")
                description = data.get("ProjectDescription")
                try:
                    message = self.create("Projects",
                                          values=(project_name,description),
                                          columns=("name", "description"))
                    return return_status(message=message, status="201") 
                except Exception as e:
                    return throw_exception(e=e, message=message)
                
            elif request.method == "PUT":
                data = request.get_json()
                if not data or not "ProjectName" in data or not "ProjectDescription" in data:
                    return return_status(message="missing fields", status=400)
                
                project_name = data.get("ProjectName") 
                description = data.get("ProjectDescription") 
                try:
                    message = self.update(table="Projects", 
                                          columns=("Name", "Description"),
                                          where_column="Project_ID",
                                          where_value=project_ID,
                                          values=(project_name, description))
                    return return_status(message=message, status=200)
                except Exception as e:
                    return throw_exception(e=e, message=message)

            else:
                try: 
                    message = self.delete("Projects", "Project_ID", project_ID)
                    return return_status(message= message, status=200)
                except Exception as e:
                    return throw_exception(e=e, message=message)
                 
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
                    return return_dict(data=feedbacks, status=200)

                except Exception as e:
                    return throw_exception(e=e)

            elif request.method == "POST":
                data = request.get_json()
                if not data or not "Author" in data or not "Feedback" in data:
                    return return_status(message="missing fields", status=400)
                try:
                    message = self.create( "Feedbacks", 
                                          values=(data.get("Author"),
                                                  data.get("Feedback")),
                                          columns=("Author",
                                                   "Feedback"))
                    return return_status(message=message, status=201)
                
                except Exception as e:
                    return throw_exception(e=e, message=message)
                
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
                    return return_dict(data=collaborations, status=200)
                except Exception as e:
                    return throw_exception(e=e)
            
        @app.route("/api/collaborations/co2_fact_submissions", methods=["GET", "POST", "PUT", "DELETE"])
        def co2_facts_submissions():
            if request.method == "GET":
                try:
                    data = self.get_all_co2_submissions()
                    data["actions"] = [
                        {"href": url_for("co2_facts_submissions", _external=True),
                         "method": "GET"},
                        {"href": url_for("co2_facts_submissions", _external=True),
                         "method": "POST"},
                        {"href": url_for("co2_facts_submissions", _external=True),
                         "method": "PUT"},
                        {"href": url_for("co2_facts_submissions", _external=True),
                         "method": "DELETE"},
                        ]
                    return return_dict(data=data, status=200)
                
                except Exception as e:
                    return throw_exception(e)
            elif request.method == "POST":                
                try:
                    data = request.get_json()
                    if (not data or not "Source" in data or not "Fact" in data or not "Co2" in data
                        or not "Co2Unit" in data or not "Timespan" in data or not "TimespanUnit" in data):
                        return return_status("missing fields", 400)

                    message = self.create(table="Submissions",
                                          columns=("Source", "Fact", "Co2", "Timespan"),
                                          values=(data.get('Source'),
                                                  data.get('Fact'),
                                                  float(data.get('Co2')) * float(data.get("Co2Unit")),
                                                  float(data.get("Timespan")) * float(data.get("TimespanUnit"))))
                    return return_status(message, 201)
                except Exception as e:
                    return throw_exception(e, message)
                
                
        def return_dict(data: dict, status: int):
            response = Response(self.jsonificator.convert_dict_to_json(data),
                                status=status,
                                mimetype="application/json",
                                headers={"Cache-Control": "no-cache, no-cache"})
            return response
                
        def return_status(message: str, status: int):
            
            message = "Success" if message is None else message
            response = Response(self.jsonificator.jsonify_message(message),
                                status=status,
                                mimetype="application/json",
                                headers={"Cache-Control": "no-cache, no-cache"})
            return response
                
        def throw_exception(e, message=""):
            response = Response(self.jsonificator.jsonify_error(e, message),
                                status=500,
                                mimetype="application/json",
                                headers={"Cache-Control": "no-cache, no-cache"})
            response.headers["Cache-Control"] = "no-cache, no-cache"
            return response