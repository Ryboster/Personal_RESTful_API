

from flask import render_template, request, redirect, url_for
from lib.jsonificator import Jsonificator
from lib.databases.dao import DAO
from lib.authenticator import Authenticator
from lib.endpoints.signer import Signer

class Collaborations(DAO, Signer):
    def __init__(self):
        super().__init__()
        self.jsonificator = Jsonificator()
        self.authy = Authenticator()
        
    def register(self, app):
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
                    return self.make_response(data=collaborations, status=200)
                except Exception as e:
                    return self.make_response(e=e, status=500)