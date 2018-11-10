# Creating Node Class
class Node:
    def __init__(self, id, widget_id, name, longitude, latitude):
        self.id = id
        self.widget_id = widget_id
        self.name = name
        self.long = longitude
        self.lat = latitude
        
    def updateNode(self, id, widget_id, name, longitude, latitude):
        self.id = id
        self.widget_id = widget_id
        self.name = name
        self.long = longitude
        self.lat = latitude

    def updateCoords(self, longitude, latitude):
        self.long = longitude
        self.lat = latitude
        
    def getAllProperties(self):
        return ("Node ID: ", self.id, "\nWidget ID: ", self.widget_id,"Node Name: ", self.name, "\nLongtitude: ", self.long, "\nLatitude: ", self.lat)
    
    def getID(self):
        return int(self.id)
    
    def getName(self):
        return self.name
    
    def getLongitude(self):
        return float(self.long)
    
    def getLatitude(self):
        return float(self.lat)

    def getWidgetId(self):
        return int(self.widget_id)
