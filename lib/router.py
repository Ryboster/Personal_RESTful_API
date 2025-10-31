import os
from flask import send_from_directory, request, redirect, url_for
from lib.endpoints.projects import Projects
from lib.endpoints.feedback import Feedback
from lib.endpoints.about import About
from lib.endpoints.backup import Backup
from lib.endpoints.collaborations import Collaborations
from lib.endpoints.co2_fact_submissions import Co2_Fact_Subbmissions
from lib.endpoints.index import Index
from lib.endpoints.register import Register
from lib.endpoints.login import Login
from lib.endpoints.collaborators import Collaborators
from lib.authenticator import Authenticator as Authy
from lib.databases.dao import DAO
###
### This script is responsible for fetching and serving static files
### based on user request. It is the core of this application.
### Each endpoint has a /raw "subendpoint" which can be used to fetch
### the endpoint's content in JSON format.
###

STATIC_FOLDER = "static"
TEMPLATES_FOLDER = "html"

class Router(DAO):
    def __init__(self, app):
        super().__init__()                  # Initialize CRUD.
        self.app = app                      # Take ownership of the app object.
        self.authy = Authy()
        
        self.register_global(app)
        Projects().register(app)
        Feedback().register(app)
        About().register(app)
        Backup().register(app)
        Collaborations().register(app)
        Co2_Fact_Subbmissions().register(app)
        Index().register(app)
        Register().register(app)
        Login().register(app)
        Collaborators().register(app)
        
    def register_global(self, app):
        @app.before_request
        def authenticate():
            public_endpoints = {"login", "co2_fact_submissions", "logout", "register", "feedback", "serve_media", "static"}
            token = request.cookies.get("token")
            
            ### If not logged in, ignore
            if request.endpoint in public_endpoints:
                return
            if token is None and request.method == "GET":
                return
            
            ### If session expired, log out
            if token is not None and self.authy.is_session_expired(token):
                return redirect(url_for("logout"))
            
            ### If not logged in and posting, log in
            elif token is None and request.method == "POST":
                return redirect(url_for("login", message="No permission"))
            
            ### If logged in and posting, check privileges
            if request.method == "POST" and not self.authy.is_user_admin(self.get_session(token=token)["ID"]):
                return redirect(url_for("logout"))


        @app.route("/serve_backup/<path:filename>", methods=["GET"])
        def serve_backup(filename):
            session = self.get_session(request.cookies.get("token"))
            if not "ID" in session:
                return redirect(url_for("backup", message="Insufficient privileges!"))
            if self.authy.is_user_admin(session["ID"]):
                return send_from_directory(os.path.join(self.BACKUP_DIR), filename)
            else:
                return redirect(url_for("backup", message="Insufficient privileges!") )
            
        ### "Helper" endpoint used for fetching media resources by other endpoints
        @app.route("/serve_media/<path:path>")
        def serve_media(path):
            return send_from_directory(app.config["MEDIA_FOLDER"], path)