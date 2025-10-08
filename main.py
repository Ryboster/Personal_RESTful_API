from flask import Flask
import os
from lib.router import Router
from sys import argv

###
### This script is responsible for launching the application.
### It takes 2 optional positional arguments; PORT and HOST.
### PORT must be entered as whole number.
### HOST must be wrapped in quotaion marks ("").
### If no arguments are provided, the script will default to 0.0.0.0:443
### 

try:
    PORT = argv[1]
    HOST = argv[2]  
except IndexError:
    PORT = 443
    HOST = "0.0.0.0"

app = Flask("Developer Portfolio", static_folder="static")
app.config['MEDIA_FOLDER'] = os.path.join(os.getcwd(), "media")
Router(app)

if __name__ == "__main__":
    if os.path.exists("fullchain.crt") and os.path.exists("private.key"):
        app.run(ssl_context=("fullchain.crt", "private.key"), host=HOST, port=PORT)
    else:
        app.run(host=HOST, port=PORT)
    
### Gracjan Blazejowski,
### October, 2025.