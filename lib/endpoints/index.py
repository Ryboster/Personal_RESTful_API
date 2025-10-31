from flask import render_template, request, redirect, url_for
from lib.jsonificator import Jsonificator
from lib.databases.dao import DAO
from lib.authenticator import Authenticator
from lib.endpoints.signer import Signer
import os

class Index(DAO, Signer):
    def __init__(self):
        super().__init__()
        self.jsonificator = Jsonificator()
        self.authy = Authenticator()
        
    def register(self, app):
        ### /home Endpoint
        @app.route("/", methods=["GET"])
        def index():
            return render_template("base.html")
                