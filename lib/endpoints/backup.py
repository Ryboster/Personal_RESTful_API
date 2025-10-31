from flask import render_template, request, redirect, url_for
from lib.jsonificator import Jsonificator
from lib.databases.dao import DAO
from lib.authenticator import Authenticator
from lib.endpoints.signer import Signer
import os

class Backup(DAO, Signer):
    def __init__(self):
        super().__init__()
        self.jsonificator = Jsonificator()
        self.authy = Authenticator()
        
        
    def register(self, app):
        ###
        ### HEADED 
        @app.route("/backup", methods=["GET", "POST"])
        def backup():
            if request.method == "GET":
                backup_files = os.listdir(self.BACKUP_DIR)
                return render_template("backups.html", files=backup_files)
            else:
                if request.form["_method"] == "POST":
                    self.backup_database()
                    return redirect(url_for("backup", message="Success!"))
                elif request.form["_method"] == "DELETE":
                    os.remove(os.path.join(self.BACKUP_DIR, request.form["filename"]))
                    return redirect(url_for("backup", message="Success!"))
                elif request.form["_method"] == "ROLLBACK":
                    message = self.rollback_database(request.form["filename"])
                    return redirect(url_for("backup", message="Success!"))