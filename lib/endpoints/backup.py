from flask import render_template, request, redirect, url_for, send_from_directory
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
                message = request.args.get("message", "")
                backup_files = [x for x in os.listdir(self.BACKUP_DIR) if x.endswith(".sql")]
                return render_template("backups.html", files=backup_files, message=message)
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
                
        @app.route("/serve_backup/<path:filename>", methods=["GET"])
        def serve_backup(filename):
            session = self.get_session(request.cookies.get("token"))
            if not "ID" in session:
                return redirect(url_for("backup", message="Insufficient privileges!"))
            if self.authy.is_user_admin(session["ID"]):
                return send_from_directory(os.path.join(self.BACKUP_DIR), filename)
            else:
                return redirect(url_for("backup", message="Insufficient privileges!"))