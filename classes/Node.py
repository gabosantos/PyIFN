# Creating Node Class
class Node:
    def __init__(self, id, name, longitude, latitude):
        self.id = id
        self.name = name
        self.long = longitude
        self.lat = latitude
        
    def moveNode(self, name, longitude, lattitude):
        self.name = name
        self.long = longitude
        self.lat = lattitude
        
    def getAllProperties(self):
        return ("Node Name: ", self.name, "\nLongtitude: ", self.long, "\nLatitude: ", self.lat)
    
    def getID(self):
        return int(self.id)
    
    def getName(self):
        return self.name
    
    def getLongitude(self):
        return float(self.long)
    
    def getLatitude(self):
        return float(self.lat)
