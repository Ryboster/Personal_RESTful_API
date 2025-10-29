from flask import Flask
import os
from lib.router import Router
from lib.databases.creator import Creator

###
### This script is responsible for launching the application.
### 
 
PORT = 8000
HOST = "127.0.0.1"
DEBUG = False
PROJECT_NAME = "Developer Portfolio"

class DevPortfolio(Creator):
    def __init__(self):
        super().__init__()
        self.app = Flask(PROJECT_NAME, static_folder="static")
        self.app.debug = DEBUG
        self.app.config['MEDIA_FOLDER'] = os.path.join(os.getcwd(), "media")        

dev_portfolio = DevPortfolio()
app = dev_portfolio.app
Router(app)

if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
    
### Gracjan Blazejowski,
### October, 2025.