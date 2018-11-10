import Network as nw
import time

Network1 = nw.Network("Test Network", "Drive")

Network1.createNode(1, 1, "Node 1", 0, 0)
Network1.createNode(2, 2, "Node 2", 100, 100)
Network1.createNode(3, 3, "Node 3", 24, 50)
Network1.createNode(4, 4, "Node 4", 75, 36)
Network1.createNode(5, 5, "Node 5", 50, 25)

Network1.createLink(1, "Node 1 to Node 2", 1, 2)
Network1.createLink(2, "Node 2 to Node 3", 2, 3)
Network1.createLink(3, "Node 3 to Node 1", 3, 1)
Network1.createLink(4, "Node 3 to Node 4", 3, 4)
Network1.createLink(5, "Node 4 to Node 5", 4, 5)
Network1.createLink(6, "Node 5 to Node 1", 5, 1)


print("Links:")
for i in range(0, len(Network1.getLinksList())):
    #print(Network1.getLink(i))
    print("ID:", Network1.getLink(i).getID(), "| Name:", Network1.getLink(i).getName(), "| Start Node:", Network1.getLink(i).getStartNode().getName(), "| End Node:", Network1.getLink(i).getEndNode().getName())

print("Deleting", Network1.getLinkById(6).getName(), "...")
Network1.deleteLinkById(6)
time.sleep(2)

print("Deleting", Network1.getNodeById(4).getName(), "and links connected...")
Network1.deleteNode(4)
time.sleep(2)

print("Rebuilding network...")
time.sleep(4)
Network1.createLink(7, "Node 3 to Node 5", 3, 5)
Network1.createLink(8, "Node 5 to Node 1", 5, 1)

print("Nodes: ")
for i in range(0, len(Network1.getNodesList())):
    print("Node ID:", Network1.getNode(i).getID(), "| Node Name:", Network1.getNode(i).getName())

print("Links: ")
for i in range(0, len(Network1.getLinksList())):
    print("Link ID:", Network1.getLink(i).getID(), "| Link Name:", Network1.getLink(i).getName(), "| Start Node:", Network1.getLink(i).getStartNode().getName(), "| End Node:", Network1.getLink(i).getEndNode().getName())

print(Network1.getNodeById(1) == Network1.createTempNode(1, 1, "Node 1", 0, 0))

node1 = Network1.getNodeById(1)
node2 = Network1.createTempNode(1, 1, "Node 1", 0, 0)

print(node1)
print(node2)
print(node1.getAllProperties() == node2.getAllProperties())