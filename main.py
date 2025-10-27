from flask import Flask
import os
from lib.router import Router

###
### This script is responsible for launching the application.
### It takes 2 optional positional arguments; PORT and HOST.
### PORT must be entered as whole number.
### HOST must be wrapped in quotaion marks ("").
### 
 
PORT = 8000
HOST = "127.0.0.1"

class DevPortfolio:
    def __init__(self):
        self.app = Flask("Developer Portfolio", static_folder="static")
        self.app.debug = False
        self.app.config['MEDIA_FOLDER'] = os.path.join(os.getcwd(), "media")        
        
dev_portfolio = DevPortfolio()
Router(dev_portfolio.app)

if os.path.exists("fullchain.crt") and os.path.exists("private.key"):
    dev_portfolio.app.run(ssl_context=("fullchain.crt", "private.key"), host=HOST, port=PORT)
else:
    dev_portfolio.app.run(host=HOST, port=PORT)
    
### Gracjan Blazejowski,
### October, 2025.