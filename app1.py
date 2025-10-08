from flask import Flask
import os
from lib.router import Router

###
### This script is responsible for launching the application.
###

### https://flask.palletsprojects.com/en/stable/api/
app = Flask("me", static_folder="static")
app.config['MEDIA_FOLDER'] = os.path.join(os.getcwd(), "media")

Router(app)

if __name__ == "__main__":
    app.run()
    
### Gracjan Blazejowski,
### October, 2025.