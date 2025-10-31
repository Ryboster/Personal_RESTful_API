from flask import render_template, request, redirect, url_for
import time
import os
from lib.jsonificator import Jsonificator
from lib.databases.dao import DAO
from lib.authenticator import Authenticator
from lib.endpoints.signer import Signer

class Projects(DAO, Signer):
    def __init__(self):
        super().__init__()
        self.jsonificator = Jsonificator()
        self.authy = Authenticator()
        
    def register(self, app):

        ### HEADED
        ###
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
                
        ### API
        ###
        @app.route("/api/projects", methods=["GET", "PUT", "POST", "DELETE"])
        @app.route("/api/projects/<int:project_ID>", methods=["GET", "PUT", "POST", "DELETE"])
        def API_get_projects(project_ID=None):
            if request.method == "GET":
                print(project_ID)
                if project_ID:
                    all_projects = self.get_all_projects()
                    requested_project = {}
                    print(all_projects)
                    for ID in all_projects.keys():
                        if project_ID == ID:
                            requested_project[project_ID] = all_projects[project_ID]
                    if len(requested_project.keys()) == 0:
                        return self.make_response(e="resource not found", status=404)
                    else:
                        requested_project = self.sign_actions(methods=["GET","PUT","DELETE"],
                                                              url=request.base_url,
                                                              payload=requested_project)
                        return self.return_dict(data=requested_project, status=200)
                else:
                    try:
                        all_projects = self.get_all_projects()
                        all_projects["actions"] = [
                            {"href": url_for("API_projects", project_ID=None, _external=True),
                             "method": "GET"},
                            {"href": url_for("API_projects", _external=True),
                             "method": "POST"}
                        ]
                        return self.make_response(payload=all_projects, status=200)
                    
                    except Exception as e:
                        return self.make_response(e=e)

            elif request.method == "POST":
                data = request.get_json()
                if not data or not "ProjectName" in data or not "ProjectDescription" in data:
                    return self.make_response(e="missing fields", status=400)
                
                project_name = data.get("ProjectName")
                description = data.get("ProjectDescription")
                try:
                    message = self.create("Projects",
                                          values=(project_name,description),
                                          columns=("name", "description"))
                    return self.make_response(message=message, status="201") 
                except Exception as e:
                    return self.make_response(e=e, message=message)
                
            elif request.method == "PUT":
                data = request.get_json()
                if not data or not "ProjectName" in data or not "ProjectDescription" in data:
                    return self.make_response(e="missing fields", status=400)
                
                project_name = data.get("ProjectName") 
                description = data.get("ProjectDescription") 
                try:
                    message = self.update(table="Projects", 
                                          columns=("Name", "Description"),
                                          where_column="Project_ID",
                                          where_value=project_ID,
                                          values=(project_name, description))
                    return self.make_response(message=message, status=200)
                except Exception as e:
                    return self.make_response(e=e, message=message)
            else:
                try: 
                    message = self.delete("Projects", "Project_ID", project_ID)
                    return self.make_response(message= message, status=200)
                except Exception as e:
                    return self.make_response(e=e, message=message)