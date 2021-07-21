import os
import json

class JSONFile:

    def __init__(self, type, address=None):

        self.type = type
        self.address = address

        if address is not None: self.address = address
        else:
            for root, dirs, files in os.walk(os.getcwd()):
                for file in files:
                    if self.type in file:
                        self.address = os.path.join(root, self.type) + '.json'
            if self.address is None:
                raise FileNotFoundError 
            
    def get_value(self, parameter):

        json_file = open(self.address, encoding='utf-8')
        json_data = json.load(json_file)
        json_file.close()
        
        return json_data.get(parameter)

    def set_value(self):
        pass

    def get_all_values(self):
        
        json_file = open(self.address, encoding='utf-8')
        json_data = json.load(json_file)
        json_file.close()

        return json_data

    def set_all_values(self):
        pass