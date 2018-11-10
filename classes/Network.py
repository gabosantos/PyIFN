import Node as nd
import Link as lk
import pandas as pd
import numpy as np

class Network: 
    # Initializes a network by creating Nodes and Links list
    def __init__ (self, name, network_type):
        self.name = name
        self.type = network_type
        self.nodes = []
        self.links = []

    # Creates a node in the network and append to Nodes list
    def createNode(self, id, object_id, name, longitude, latitude):
        self.nodes.append(nd.Node(id, object_id, name, longitude, latitude))

    # Creates link between two nodes in the network and append to Links list
    def createLink(self, id, object_id, name, node1, node2):
        start = self.getNodeById(node1)
        end = self.getNodeById(node2)

        self.links.append(lk.Link(id, object_id, name, start, end, 2, 10, 10))
        print("Link Registered")

    # Returns the entire list of nodes in the network
    def getNodesList(self):
        return self.nodes

    # Returns the entire list of links in the network
    def getLinksList(self):
        return self.links

    # Returns a specific node in the Nodes list by list index
    def getNode(self, index):
        return self.nodes[index]

    # Returns a specific node in the Nodes list by Node ID
    def getNodeById(self, node_ID):
        for i in range(0, len(self.nodes)):
            if (self.getNode(i).getID() == node_ID):
                return self.getNode(i)
    
    # Returns a specific link in the Links list by list index
    def getLink(self, index):
        return self.links[index]

    # Returns a specific link in the Links list by Link ID
    def getLinkById(self, link_ID):
        for i in range(0, len(self.links)):
            if (self.getLink(i).getID() == link_ID):
                return self.getLink(i)

    # Deletes a link in the network
    def deleteLinkById(self, id):
        for i in range(0, len(self.links)):
            if self.links[i].getID() == id:
                self.links.remove(self.getLink(i))

    # Deletes a link when its node is deleted
    def deleteLinkByNode(self, node_ID):
        delete = []
        for i in range(0, len(self.links)):
            if (self.links[i].getNodeA().getID() == node_ID or self.links[i].getNodeB().getID() == node_ID):
                delete.append(i)
                
        for i in range(len(delete) - 1, -1, -1):
            self.links.remove(self.getLink(delete[i]))

    # Deletes a node (and links connected) in the network
    def deleteNode(self, node_ID):
        delete = None
        for i in range(0, len(self.nodes)):
            if self.nodes[i].getID() == node_ID:
                # Return connected links and delete them
                self.deleteLinkByNode(node_ID)
                delete = i
                
        self.nodes.remove(self.getNode(delete))

    # Update Node Properties
    def updateNode(self, active_id, id, object_id, name, longitude, latitude):
        temp_node = nd.Node(id, object_id, name, longitude, latitude)
        active_node = self.getNodeById(active_id)

        if (temp_node.getAllProperties() == active_node.getAllProperties()):
            pass
        else:
            active_node.updateNode(id, object_id, name, longitude, latitude)

    # Update Node Coordinates
    def updateNodeCoords(self, id, longitude, latitude):
        active_node = self.getNodeById(id)
        active_node.updateCoords(longitude, latitude)

    # Update Link Properties
    def updateLink(self, active_id, id, object_id, name, node1, node2, direction, capacity, distance):
        temp_link = lk.Link(id, object_id, name, node1, node2, direction, capacity, distance)
        active_link = self.getLinkById(active_id)

        if(temp_link.getAllProperties() == active_link.getAllProperties()):
            pass
        else:
            active_link.updateLink(id, object_id, name, node1, node2, direction, capacity, distance)

    # Get links connected to nodes
    def getLinksByNodeId(self, node_ID):
        edges = []
        for i in range(0, len(self.links)):
            if (self.links[i].getNodeA().getID() == node_ID or self.links[i].getNodeB().getID() == node_ID):
                edges.append(self.links[i])
        
        return edges
