import json
import os

class DataHandler:
    def __init__(self, filename="data.json"):
        self.filename = filename

    def append(self, name, id, location, temperature):
        
        # Load existing data
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                data = json.load(f)
        else:
            data = []
        
        new_data = {
            "name": name,
            "id": id,
            "location": location,
            "temperature": temperature
        }

        # append new item
        data.append(new_data)

        with open (self.filename, "w") as f:
            json.dump(data, f, indent=4)
        
    def read(self):

        if not os.path.exists(self.filename):
            return []
        
        try:
            with open(self.filename, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
        
        return data

    def get_data_by_name(self, target_name):

        data = self.read()

        for artifact in data:
            if artifact["name"] == target_name:
                return artifact
        
        return {}