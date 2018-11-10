# Creating Link Class
class Link:
    def __init__(self, id, name, node_A, node_B):
        self.id = id
        self.name = name
        self.nodeA = node_A
        self.nodeB = node_B
        self.direction = ""
        
    def addProperties(self, capacity, distance):
        self.capacity = capacity
        self.distance = distance

    def getID(self):
        return self.id
    
    def getName(self):
        return self.name

    def getStartNode(self):
        return self.nodeA

    def getEndNode(self):
        return self.nodeB

    def getDirection(self):
        return self.direction

    def getCapacity(self):
        return self.capacity

    def getDistance(self):
        return self.distance