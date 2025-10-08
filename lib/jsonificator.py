import json


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