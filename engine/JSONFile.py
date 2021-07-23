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
            
    def getValue(self, parameter):

        jsonFile = open(self.address, encoding='utf-8')
        jsonData = json.load(jsonFile)
        jsonFile.close()
        
        return jsonData.get(parameter)

    def setValue(self): #TODO write it
        pass

    def getAllValues(self):
        
        jsonFile = open(self.address, encoding='utf-8')
        jsonData = json.load(jsonFile)
        jsonFile.close()

        return jsonData

    def setAllValues(self): #TODO write it
        pass