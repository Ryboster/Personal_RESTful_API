
from flask import render_template, request, redirect, url_for, make_response
import time
import os
from lib.jsonificator import Jsonificator
from lib.databases.dao import DAO
from lib.authenticator import Authenticator
from lib.endpoints.signer import Signer

class Login(DAO, Signer):
    def __init__(self):
        super().__init__()
        self.jsonificator = Jsonificator()
        self.authy = Authenticator()
        
    def register(self, app):
        @app.route("/login", methods=["GET", "POST"])
        def login():
            if request.method == "GET":
                message = request.args.get("message", "")
                return render_template("login.html", message=message)
            
            elif request.method == "POST":
                _username = request.form["Username"]
                _password = request.form["Password"]
                ### Verify that username and password are correct
                user_record = self.get_user(username=_username, password=_password)
                if not "ID" in user_record:
                    return redirect(url_for("login",message="wrong credentials" ) )
                if self.authy.is_user_logged(user_record["ID"]):
                    self.delete(table="Sessions",
                                where_column="User_ID",
                                where_value=user_record["ID"])
                token = self.authy.generate_hash()
                expiry_time = int(time.time()) + self.authy.EXPIRY
                self.create(table="Sessions",
                            columns=("User_ID", "Token", "Expiry"),
                            values=(user_record["ID"], token, expiry_time))
                
                response = make_response(redirect(url_for("login",message="Success"))) 
                response.set_cookie("token", token, max_age=self.authy.EXPIRY)
                response.set_cookie("username", user_record["username"], max_age=self.authy.EXPIRY)
                return response
            return response
        @app.route("/logout", methods=["GET"])
        def logout():
            response = make_response(redirect(url_for("login",message="You have been logged out!") ))
            self.delete(table="Sessions",
                        where_column="Token",
                        where_value=request.cookies.get("token"))
            response.set_cookie("token", '', max_age=0)
            response.set_cookie("username", '', max_age=0)
            return response