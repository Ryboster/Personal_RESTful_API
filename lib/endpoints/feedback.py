from flask import render_template, request, redirect, url_for
import time
import os
from lib.jsonificator import Jsonificator
from lib.databases.dao import DAO
from lib.authenticator import Authenticator
from lib.endpoints.signer import Signer

class Feedback(DAO, Signer):
    def __init__(self):
        super().__init__()
        self.jsonificator = Jsonificator()
        self.authy = Authenticator()
        
        
    def register(self, app):
        ### 
        ### HEADED
        @app.route("/feedback", methods=["GET", "POST"])
        def feedback():
            if request.method == "GET":
                message = request.args.get("message") if request.args.get("message") != None else ""
                feedbacks = self.get_all_feedbacks()
                return render_template("feedback.html", all_feedbacks=feedbacks, message=message)
            else:
                if request.form["_method"] == "POST":
                    message=self.create("Feedbacks", 
                                        values=(request.form["Author"],
                                                request.form["Feedback"]),
                                        columns=("Author",
                                                 "Feedback"))
                    return redirect(url_for("feedback", message=message))
                elif request.form["_method"] == "DELETE":
                    message = self.delete("Feedbacks",
                                          where_column="Feedback_ID",
                                          where_value=request.form["ID"])
                    return redirect(url_for("feedback", message=message))
                
        ###
        ### API
        @app.route("/api/feedback", methods=["GET", "POST", "PUT", "DELETE"])
        def API_feedback():
            if request.method == "GET":
                try: 
                    feedbacks = self.get_all_feedbacks()
                    feedbacks = self.sign_actions(mehods=["GET", "POST"],
                                                  url=request.base_url,
                                                  payload=feedbacks)
                    return self.make_response(payload=feedbacks, status=200)

                except Exception as e:
                    return self.make_response(e=e, status=500)

            elif request.method == "POST":
                data = request.get_json()
                if not data or not "Author" in data or not "Feedback" in data:
                    return self.make_response(e="missing fields", status=400)
                try:
                    message = self.create( "Feedbacks", 
                                          values=(data.get("Author"),
                                                  data.get("Feedback")),
                                          columns=("Author",
                                                   "Feedback"))
                    return self.make_response(message=message, status=201)
                
                except Exception as e:
                    return self.make_response(e=e, message=message)