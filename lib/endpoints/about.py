from flask import render_template, request, redirect, url_for
import time
import os
from lib.jsonificator import Jsonificator
from lib.databases.dao import DAO
from lib.authenticator import Authenticator
from lib.endpoints.signer import Signer

class About(DAO, Signer):
    def __init__(self):
        super().__init__()
        self.jsonificator = Jsonificator()
        self.authy = Authenticator()
        
    def register(self, app):
        ###
        ### HEADED
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
        
        ### /about Endpoint
        @app.route("/api/about", methods=["GET"])
        def API_about():
            try:
                about_dict = self.jsonificator.read_from_json(os.path.join(app.config["MEDIA_FOLDER"], "json", "About.json"))
                about_dict = self.sign_actions(methods=["GET"], 
                                  url=request.base_url,
                                  payload = about_dict)
                return self.make_response(payload=about_dict, status=200)
            except Exception:
                return self.make_response(e="resource not found", status=404)