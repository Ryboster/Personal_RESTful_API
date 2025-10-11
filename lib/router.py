from lib.endpoints.api import API_Endpoints
from lib.endpoints.headed import Headed_Endpoints

###
### This script is responsible for fetching and serving static files
### based on user request. It is the core of this application.
### Each endpoint has a /raw "subendpoint" which can be used to fetch
### the endpoint's content in JSON format.
###

STATIC_FOLDER = "static"
TEMPLATES_FOLDER = "html"

class Router():
    def __init__(self, app):
        super().__init__()                  # Initialize CRUD.
        self.app = app                      # Take ownership of the app object.
        API_Endpoints().register_endpoints(app)
        Headed_Endpoints().register_endpoints(app)