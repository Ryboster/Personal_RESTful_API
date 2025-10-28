from flask import Flask
import os
from lib.router import Router

###
### This script is responsible for launching the application.
### 
 
PORT = 8001
HOST = "127.0.0.1"
DEBUG = False
PROJECT_NAME = "Developer Portfolio"

class DevPortfolio:
    def __init__(self):
        self.app.debug = DEBUG
        self.app = Flask(PROJECT_NAME, static_folder="static")
        self.app.config['MEDIA_FOLDER'] = os.path.join(os.getcwd(), "media")        

dev_portfolio = DevPortfolio()
Router(dev_portfolio.app)

if __name__ == "__main__":
    dev_portfolio.app.run(host=HOST, port=PORT)
    
### Gracjan Blazejowski,
### October, 2025.