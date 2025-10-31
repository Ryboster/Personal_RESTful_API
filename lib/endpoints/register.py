from flask import render_template, request, redirect, url_for
import time
import os
from lib.jsonificator import Jsonificator
from lib.databases.dao import DAO
from lib.authenticator import Authenticator
from lib.endpoints.signer import Signer

class Register(DAO, Signer):
    def __init__(self):
        super().__init__()
        self.jsonificator = Jsonificator()
        self.authy = Authenticator()
        
    def register(self, app):
        @app.route("/register", methods=["GET", "POST"])
        def register():
            if request.method == "GET":
                message = request.args.get("message", "")
                return render_template("register.html", message=message)
            elif request.method == "POST":
                message = self.create("Users",
                            (request.form["Username"], request.form["Email"], request.form["Password"], False),
                            ("Username", "Email", "Password", "isAdmin"))
                return render_template("register.html", message=message)