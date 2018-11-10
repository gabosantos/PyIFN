# Creating Link Class
class Link:
    def __init__(self, id, widget_id, name, node_A, node_B, direction, capacity, distance):
        self.id = id
        self.widget_id = widget_id
        self.name = name
        self.nodeA = node_A
        self.nodeB = node_B
        self.direction = direction
        self.capacity = capacity
        self.distance = distance
        
    def updateLink(self, id, widget_id, name, node_A, node_B, direction, capacity, distance):
        self.id = id
        self.widget_id = widget_id
        self.name = name
        self.nodeA = node_A
        self.nodeB = node_B
        self.direction = direction
        self.capacity = capacity
        self.distance = distance

    def getAllProperties(self):
        return (self.id, self.widget_id, self.name, self.nodeA, self.nodeB, self.direction, self.capacity, self.distance)

    def getID(self):
        return self.id
    
    def getName(self):
        return self.name

    def getNodeA(self):
        return self.nodeA

    def getNodeB(self):
        return self.nodeB

    def getDirection(self):
        return self.direction

    def getCapacity(self):
        return float(self.capacity)

    def getDistance(self):
        return float(self.distance)

    def getWidgetId(self):
        return int(self.widget_id)