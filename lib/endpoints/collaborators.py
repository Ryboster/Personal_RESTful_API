

from flask import render_template, request, redirect, url_for
from lib.jsonificator import Jsonificator
from lib.databases.dao import DAO
from lib.authenticator import Authenticator
from lib.endpoints.signer import Signer

class Collaborators(DAO, Signer):
    def __init__(self):
        super().__init__()
        self.jsonificator = Jsonificator()
        self.authy = Authenticator()
        
    def register(self, app):
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
                
                