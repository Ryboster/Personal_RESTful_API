from flask import render_template
import os

###
### This script is responsible for fetching and serving static files
### based on user request.
###

STATIC_FOLDER = "static"
TEMPLATES_FOLDER = "html"

class Router:
    def __init__(self, app):
        self.app = app
        self.register_routes()
    
    def register_routes(self):
        @self.app.route("/")
        def index():
            return render_template("base.html")
    
    