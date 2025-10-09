import json

###
### This class handles all operations done on JSON files.
### It helps in moving this responsibility away from the
### Router, allowing for tidier code.
###
class Jsonificator:
    def __init__(self):
        pass
    
    def read_from_json(self, path):
        with open(path) as json_data:
            print(f"opened: {json_data}")
            x = json.load(json_data)
            json_data.close()
        return x
    
    def convert_dict_to_json(self, dict):
        print(json.dumps(dict))
        return json.dumps(dict)
    
    def jsonify_error(self, err):
        return json.dumps({"error": str(err)})