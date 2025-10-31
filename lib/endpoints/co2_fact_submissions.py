

from flask import render_template, request, redirect, url_for, send_from_directory
from lib.jsonificator import Jsonificator
from lib.databases.dao import DAO
from lib.authenticator import Authenticator
from lib.endpoints.signer import Signer
import sqlite3
import os

class Co2_Fact_Subbmissions(DAO, Signer):
    def __init__(self):
        super().__init__()
        self.jsonificator = Jsonificator()
        self.authy = Authenticator()
        self.query = """
        CREATE TABLE IF NOT EXISTS Submissions
        (
            Submission_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            Source TEXT UNIQUE NOT NULL,
            Fact TEXT UNIQUE NOT NULL,
            Co2 REAL NOT NULL,
            Timespan INTEGER NOT NULL
        )
        """
        
    def register(self, app):
        ###
        ### HEADED 
        @app.route("/collaborations/co2_fact_submissions", methods=["GET", "POST"])
        def co2_fact_submissions():
            if request.method == "GET":
                message = request.args.get("message") if request.args.get("message") != None else ""
                submissions = self.get_all_co2_submissions()
                return render_template("co2_fact_submissions.html", submissions=submissions, message=message)
            else:
                if request.form["_method"] == "POST":
                    message = self.create(table="Submissions",
                                          columns=("Source", "Fact", "Co2", "Timespan"),
                                          values=(request.form['Source'],
                                                  request.form['Fact'],
                                                  float(request.form['Co2']) * float(request.form["Co2Unit"]),
                                                  float(request.form["Timespan"]) * float(request.form["TimespanUnit"])))
                    return redirect(url_for("co2_fact_submissions", message=message))
                
                elif request.form["_method"] == "PUT":
                    message = self.update(table="Submissions",
                                          columns=("Source", "Fact", "Co2", "Timespan"),
                                          values=(request.form["Source"], 
                                                  request.form["Fact"], 
                                                  float(request.form['Co2']) * float(request.form["Co2Unit"]),
                                                  float(request.form["Timespan"]) * float(request.form["TimespanUnit"])),
                                          where_column="Submission_ID",
                                          where_value=request.form["ID"])
                    return redirect(url_for("co2_fact_submissions", message=message))
                
                elif request.form["_method"] == "DELETE":
                    message = self.delete(table="Submissions",
                                          where_column="Submission_ID",
                                          where_value=request.form["ID"])
                    return redirect(url_for("co2_fact_submissions", message=message))
        
        @app.route("/collaborations/co2_fact_submissions/download", methods=["GET"])
        def download_co2_fact_submissions():
            submissions = self.get_all_co2_submissions()
            filepath = os.path.join(self.BACKUP_DIR, "co2_fact_submissions")
            filename = "submissions.sqlite3"
            
            if os.path.exists(os.path.join(filepath, filename)):
                os.remove(os.path.join(filepath, filename))
            conn = sqlite3.connect(os.path.join(filepath, filename))
            cursor = conn.cursor()
            cursor.execute(self.query)
            
            for record in submissions:
                cursor.execute(f"""INSERT INTO Submissions(Source, Fact, Co2, Timespan)
                               VALUES('{submissions[record]['Source']}','{submissions[record]['Fact']}','{submissions[record]['Co2']}','{submissions[record]['Timespan']}')""")
            
            conn.commit()
            conn.close()
            return send_from_directory(filepath, filename)

        ###
        ### API
        @app.route("/api/collaborations/co2_fact_submissions", methods=["GET", "POST", "PUT", "DELETE"])
        def co2_facts_submissions():
            if request.method == "GET":
                try:
                    data = self.get_all_co2_submissions()
                    data = self.sign_actions(methods=["GET, POST, PUT, DELETE"], 
                                            url=request.base_url,
                                            payload=data)
                    return self.make_response(payload=data, status=200)
                
                except Exception as e:
                    return self.make_response(e)
            elif request.method == "POST":                
                try:
                    data = request.get_json()
                    if (not data or not "Source" in data or not "Fact" in data or not "Co2" in data
                        or not "Co2Unit" in data or not "Timespan" in data or not "TimespanUnit" in data):
                        return self.make_response(e="missing fields", status=400)

                    message = self.create(table="Submissions",
                                          columns=("Source", "Fact", "Co2", "Timespan"),
                                          values=(data.get('Source'),
                                                  data.get('Fact'),
                                                  float(data.get('Co2')) * float(data.get("Co2Unit")),
                                                  float(data.get("Timespan")) * float(data.get("TimespanUnit"))))
                    return self.make_response(message=message, status=201)
                except Exception as e:
                    return self.make_response(e=e, message=message)