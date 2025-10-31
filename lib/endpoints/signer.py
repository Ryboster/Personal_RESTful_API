from werkzeug.wrappers import Response
from flask import request
import json


class Signer():
    def __init__(self):
        self.NO_PERMS_MESSAGE = "Insufficient privileges!"
    
    def make_response(self, e=None, message=None, status=None, payload={}):
        if e:
            payload["error"] = e
        if message:
            payload["message"] = message

        response = Response(json.dumps(payload),
                            status=status,
                            type="application/json")   
        response = self.sign_response(response)
        return response     
    
    ###
    ### Sign Response objects
    def sign_response(self, response):
        response.headers["Cache-Control"] = "no-cache, no-cache"
        return response
    
    def sign_mimetype(self, response):
        response.mimetype = "application/json"
        return response
    
    ###
    ### Sign payload
    def sign_actions(self, methods, url, payload):
        payload["actions"] = []
        for method in methods:
            payload["actions"].append({"href": url, "method": method})
        return payload