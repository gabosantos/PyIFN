import Network as nw
import tkinter as tk
from tkinter import ttk
import Tktable as tkt
import numpy as np

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)

class RoadNetworkSimulator(tk.Tk):

    # Initializes the class
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        self.attributes("-fullscreen", True)
        self.title("Road Network Simulator")
        self.menuBar(self)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0,weight=1)

        self.frames = {}

        for F in (StartPage, CreateNewProject, StartSimulation, SearchLocation):
            
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

    def get_page(self, page_class):
        return self.frames[page_class]

    def menuBar(self, master):
        # Creating the menu bar
        mn_menuBar = tk.Menu(master)

        # File Menu
        mn_fileMenu = tk.Menu(mn_menuBar, tearoff = 0)
        mn_fileMenu.add_command(label = "New", command = lambda: self.show_frame(CreateNewProject))
        mn_fileMenu.add_command(label = "Open")
        mn_fileMenu.add_command(label = "Save")
        mn_fileMenu.add_command(label = "Save as...")
        mn_fileMenu.add_separator()
        mn_fileMenu.add_command(label = "Exit", command = self.destroy)
        mn_menuBar.add_cascade(label = "File", menu = mn_fileMenu)

        # Edit Menu
        mn_editMenu = tk.Menu(mn_menuBar, tearoff = 0)
        mn_editProject = tk.Menu(mn_editMenu, tearoff = 0)

        mn_editProject.add_command(label = "New Scenario")
        mn_editProject.add_command(label = "Select Scenario")
        mn_editProject.add_command(label = "Copy Scenario")
        mn_editProject.add_command(label = "Delete Scenario")
        mn_editProject.add_command(label = "Assign Matrix to Scenario")
        mn_editProject.add_command(label = "Open Project Property Window")

        mn_editMenu.add_cascade(label = "Edit Project", menu = mn_editProject)

        mn_editNetwork = tk.Menu(mn_editMenu, tearoff = 0)

        mn_editNode = tk.Menu(mn_editNetwork, tearoff = 0)

        mn_editNode.add_command(label = "Add Node")
        mn_editNode.add_command(label = "Select Node")
        mn_editNode.add_command(label = "Delete Selected Nodes")
        mn_editNode.add_command(label = "Move Node")
        mn_editNode.add_separator()
        mn_showhideeditnode = tk.Menu(mn_editNode, tearoff = 0)

        mn_showhideeditnode.add_command(label = "In-Degree")
        mn_showhideeditnode.add_command(label = "Out-Degree")

        mn_editNode.add_cascade(label = "Show/Hide", menu = mn_showhideeditnode)

        mn_editNetwork.add_cascade(label = "Node", menu = mn_editNode)

        mn_editLink = tk.Menu(mn_editNetwork, tearoff = 0)

        mn_editLink.add_command(label = "Add Link")
        mn_editLink.add_command(label = "Select Link")
        mn_editLink.add_command(label = "Delete Selected Links")
        mn_editLink.add_command(label = "Change Direction")
        mn_editLink.add_command(label = "Change Capacity")

        mn_editLink.add_separator()
        mn_showhideeditlink = tk.Menu(mn_editLink, tearoff = 0)

        mn_showhideeditlink.add_command(label = "Link Thickness")
        
        mn_editLink.add_cascade(label = "Show/Hide", menu = mn_showhideeditlink)

        mn_editNetwork.add_cascade(label = "Link", menu = mn_editLink)

        mn_editNetworkOptions = tk.Menu(mn_editMenu, tearoff = 0)

        mn_editNetworkOptions.add_command(label = "Get from OSM")
        mn_editNetworkOptions.add_command(label = "Select Network")
        mn_editNetworkOptions.add_command(label = "Shift (Translate)")
        mn_editNetworkOptions.add_command(label = "Delete Network")
        mn_editNetworkOptions.add_command(label = "Add Cloud Node and Dummy Links")
        mn_editNetworkOptions.add_separator()
        mn_showhideeditnetwork = tk.Menu(mn_editNetworkOptions, tearoff = 0)
        mn_showhideeditnetwork.add_command(label = "Node ID")
        mn_showhideeditnetwork.add_command(label = "Link ID")
        mn_showhideeditnetwork.add_command(label = "Node Flow")
        mn_showhideeditnetwork.add_command(label = "Link Flow")
        mn_showhideeditnetwork.add_command(label = "Cloud Node and Dummy Links")

        mn_editNetwork.add_cascade(label = "Network", menu = mn_editNetworkOptions)

        mn_editMenu.add_cascade(label = "Edit Network", menu = mn_editNetwork)

        mn_editMatrix = tk.Menu(mn_editMenu, tearoff = 0)
        mn_editMatrix.add_command(label = "Select Matrix")
        mn_editMatrix.add_command(label = "Copy Matrix")
        mn_editMatrix.add_command(label = "Delete Matrix")
        mn_editMatrix.add_command(label = "Assign Matrix")
        mn_editMenu.add_cascade(label = "Matrix", menu = mn_editMatrix)

        mn_menuBar.add_cascade(label = "Edit", menu = mn_editMenu)

        # Analysis Menu
        mn_analysisMenu = tk.Menu(mn_menuBar, tearoff = 0)
        mn_analysisMenu.add_command(label = "Adjacency Matrix")
        mn_analysisMenu.add_command(label = "Capacity Matrix")
        mn_analysisMenu.add_command(label = "Stochastic Matrix")
        mn_analysisMenu.add_command(label = "Ideal Flow")
        mn_analysisMenu.add_command(label = "Dual Ideal Flow")
        mn_analysisMenu.add_command(label = "Link Probabilities")
        mn_analysisMenu.add_command(label = "Congestion")
        mn_analysisMenu.add_command(label = "Perturbation")
        mn_menuBar.add_cascade(label = "Analysis", menu = mn_analysisMenu) 

        # View Menu
        mn_viewMenu = tk.Menu(mn_menuBar, tearoff = 0)
        mn_viewMenu.add_command(label = "Matrix")
        mn_viewMenu.add_command(label = "Network")
        
        mn_viewwindows = tk.Menu(mn_viewMenu, tearoff = 0)
        mn_viewwindows.add_command(label = "Link Properties")
        mn_viewwindows.add_command(label = "Node Properties")
        mn_viewwindows.add_command(label = "Network Properties")
        mn_viewwindows.add_command(label = "Project Properties")
        mn_viewwindows.add_command(label = "Options")
        mn_viewMenu.add_cascade(label = "Window", menu = mn_viewwindows)

        mn_zoom = tk.Menu(mn_viewMenu, tearoff = 0)
        mn_zoom.add_command(label = "Zoom In")
        mn_zoom.add_command(label = "Zoom Out")
        mn_zoom.add_command(label = "Pan")
        mn_zoom.add_command(label = "Window")
        mn_viewMenu.add_cascade(label = "Zoom", menu = mn_zoom)

        mn_menuBar.add_cascade(label = "View", menu = mn_viewMenu)

        # Calibration Menu
        mn_calibrationMenu = tk.Menu(mn_menuBar, tearoff = 0)
        mn_calibrationMenu.add_command(label = "Match Ideal Flow to Flow Matrix")
        mn_calibrationMenu.add_command(label = "Match Selected Link Flows")
        mn_calibrationMenu.add_command(label = "Stochastic from Maximum Entropy")
        mn_menuBar.add_cascade(label = "Calibration", menu = mn_calibrationMenu)       

        # Animation Menu
        mn_animationMenu = tk.Menu(mn_menuBar, tearoff = 0)
        mn_animationMenu.add_command(label = "Random Walk on Network")
        mn_animationMenu.add_command(label = "Add Lane on a Selected Link")
        mn_menuBar.add_cascade(label = "Animation", menu = mn_animationMenu)

        # Options Menu
        mn_optionsMenu = tk.Menu(mn_menuBar, tearoff = 0)
        mn_optionsMenu.add_command(label = "Categorization")

        mn_showhideopt = tk.Menu(mn_optionsMenu, tearoff = 0)
        mn_showhideopt.add_command(label = "is Ideal Flow")
        mn_showhideopt.add_command(label = "is Premagic")
        mn_showhideopt.add_command(label = "is Irreducibleis")
        mn_showhideopt.add_command(label = "is Nearly Reducible")
        mn_showhideopt.add_command(label = "is Eulerian")
        mn_showhideopt.add_command(label = "is Doubly Stochastic")
        mn_showhideopt.add_command(label = "Period")
        mn_optionsMenu.add_cascade(label = "Show/Hide Matrix Test", menu = mn_showhideopt)

        mn_inexopt = tk.Menu(mn_optionsMenu, tearoff = 0)
        mn_inexopt.add_command(label = "Dummy Links in Flow Statistics")
        mn_inexperf = tk.Menu(mn_inexopt, tearoff = 0)
        mn_inexperf.add_command(label = "Total Flow")
        mn_inexperf.add_command(label = "Average Flow")
        mn_inexperf.add_command(label = "Standard Deviation of Flow")
        mn_inexperf.add_command(label = "Average Node Entropy")
        mn_inexperf.add_command(label = "Coefficient of Variation of Flow")
        mn_inexperf.add_command(label = "Network Entropy")
        mn_inexperf.add_command(label = "T-Index")
        mn_inexopt.add_cascade(label = "Performance Indices in Network Properties", menu = mn_inexperf)
        mn_optionsMenu.add_cascade(label = "Include/Exclude", menu = mn_inexopt)

        mn_calibrationOpt = tk.Menu(mn_optionsMenu, tearoff = 0)
        mn_calibrationOpt.add_command(label = "Show/Hide R-square Chart")
        mn_calibrationOpt.add_command(label = "Show/Hide SSE Chart")
        mn_optionsMenu.add_cascade(label = "Calibration", menu = mn_calibrationOpt)
        
        mn_menuBar.add_cascade(label = "Options", menu = mn_optionsMenu)
        
        master.config(menu=mn_menuBar)

class StartPage(tk.Frame):
    
    def __init__ (self, parent, controller):

        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Welcome to Road Network Simulator\nBrought to you by the Ateneo Pedestrian and Traffic Computing Laboratory\nCopyright 2018", font=LARGE_FONT)
        label.pack(pady = 10, padx = 10)

        bt_CreateNewProject = tk.Button(self, text = "Create New Project", command = lambda: controller.show_frame(CreateNewProject))
        bt_CreateNewProject.pack(pady = 10)

class CreateNewProject(tk.Frame):

    def __init__ (self, parent, controller):
        self.controller = controller
        tk.Frame.__init__ (self, parent)
        label = tk.Label(self, text="Create New Simulation", font=LARGE_FONT)
        label.pack(pady = 10, padx = 10)

        self.networkName = ""
        self.networkType = ""

        fr_networkName = tk.Frame(self,parent)
        fr_networkName.pack(pady = 10)

        fr_networkType = tk.Frame(self, parent)
        fr_networkType.pack(pady = 10)
        
        fr_buttons = tk.Frame(self, parent)
        fr_buttons.pack(pady = 10)

        lb_networkName = tk.Label(fr_networkName, text = "Network Name: ", anchor = tk.W)
        self.tb_networkName = ttk.Entry(fr_networkName)
        lb_networkType = tk.Label(fr_networkType, text = "Network Type:", anchor = tk.W)
        self.tb_networkType = ttk.Entry(fr_networkType)
        bt_createNetwork = ttk.Button(fr_buttons, text = "Create", command = lambda: self.saveNetwork(controller))
        bt_cancelNetwork = ttk.Button(fr_buttons, text = "Cancel", command = lambda: controller.show_frame(StartPage))
        
        lb_networkName.grid(row = 0)
        self.tb_networkName.grid(row = 0, column = 2)
        lb_networkType.grid(row = 0)
        self.tb_networkType.grid(row = 0, column = 2)
        bt_createNetwork.grid(row = 0)
        bt_cancelNetwork.grid(row = 0, column = 2)

        self.nw = nw.Network(self.getNetworkName(), self.getNetworkType())

    def saveNetwork(self, controller):
        self.networkName = self.tb_networkName.get()
        self.networkType = self.tb_networkType.get()
        x = lambda: controller.show_frame(StartSimulation)
        x()

    def getNetworkName(self):
        return self.networkName

    def getNetworkType(self):
        return self.networkType

class StartSimulation(tk.Frame):

    def __init__ (self, parent, controller):
        tk.Frame.__init__ (self, parent)
        self.controller = controller

        self.network = nw.Network(self.controller.get_page(CreateNewProject).getNetworkName(), self.controller.get_page(CreateNewProject).getNetworkType())

        self.shownetworkindicator = 0
        self.frame = tk.Frame(self)
        self.frame.pack()
        self.showNetwork = tk.Button(self.frame, text = "Show Network Details", command = lambda: self.showNetworkDetails())
        self.showNetwork.pack(pady = 10, padx = 10)
        self.searchLocation = ttk.Button(self.frame, text = "Search Map", command = lambda: controller.show_frame(SearchLocation))
        self.searchLocation.pack(pady = 10, padx = 10)

        self.createCanvas(self)

        self.node_ctr = 1
        self.link_ctr = 1

    def showNetworkDetails(self):
        self.showNetwork["text"] = "Hide Network Details"
        self.showNetwork["command"] = lambda: self.hideNetworkDetails()
        networkName = self.controller.get_page(CreateNewProject).getNetworkName()
        networkType = self.controller.get_page(CreateNewProject).getNetworkType()
        
        text = "Simulation: %s (%s)" %(networkName, networkType)

        self.label = tk.Label(self.frame, text=text, font=SMALL_FONT)
        #self.label.visible = True
        self.label.pack(pady = 10, padx = 10)

    def hideNetworkDetails(self):
        self.showNetwork["text"] = "Show Network Details"
        self.showNetwork["command"] = lambda: self.showNetworkDetails()
        self.label.pack_forget()

    def createCanvas(self, master):
        frame = tk.Frame(master)
        frame.pack(fill='both')

        self.c = tk.Canvas(master, bg = "white")
        self.c.pack(fill='both', expand=True)    

        bt = tk.Button(master, text="Print Nodes", command = lambda: self.getNodesList(tk.Tk()))
        bt2 = tk.Button(master, text="Print Links", command = lambda: self.getLinksList(tk.Tk()))
        bt.pack(pady = 10, padx = 10)
        bt2.pack(pady = 10, padx = 10)

        self.c.bind("<Double-Button-1>", self.addNode)
        self.c.bind("<B1-Motion>", self.addLink)
        self.c.bind("<Button-1>", self.getOrigin)
        self.c.bind("<ButtonRelease-1>", self.getFinal)
        self.c.tag_bind("node", "<Button-3>", self.startMove)
        self.c.tag_bind("node", "<B3-Motion>", self.moveObject)
        self.c.tag_bind("node", "<ButtonRelease-3>", self.stopMove)

        self.ovals = {}
        self.selected = None

    def getNodesList(self, edit):
        #return self.network.getNodesList()
        #print(self.network.getNodesList())
        
        edit.destroy()
        
        nodeslist = self.network.getNodesList()

        popup = tk.Tk()

        popup.wm_title("Nodes List")

        fr_tableheaders = tk.Frame(popup)

        lb_nodeID = ttk.Label(fr_tableheaders, text="ID", font=NORM_FONT)
        lb_nodeName = ttk.Label(fr_tableheaders, text="Name", font=NORM_FONT)
        lb_nodeLong = ttk.Label(fr_tableheaders, text="Dim_X", font=NORM_FONT)
        lb_nodeLat = ttk.Label(fr_tableheaders, text="Dim_Y", font=NORM_FONT)
        lb_nodeActions = ttk.Label(fr_tableheaders, text="Actions", font=NORM_FONT)

        lb_nodeID.grid(row = 0, column = 0, columnspan = 2, sticky=(tk.N, tk.E, tk.W), padx = 5)
        lb_nodeName.grid(row = 0, column = 2, columnspan = 2, sticky=(tk.N, tk.E, tk.W), padx = 5)
        lb_nodeLong.grid(row = 0, column = 4, columnspan = 2, sticky=(tk.N, tk.E, tk.W), padx = 5)
        lb_nodeLat.grid(row = 0, column = 6, columnspan = 2, sticky=(tk.N, tk.E, tk.W), padx = 5)
        lb_nodeActions.grid(row = 0, column = 8, columnspan = 2, sticky=(tk.N, tk.E, tk.W), padx = 5)

        btn = []
        for i in range(len(nodeslist)):
            nodeID = nodeslist[i].getID()
            nodeName = nodeslist[i].getName()
            nodeWidget = nodeslist[i].getWidgetId()
            nodeLongitude = nodeslist[i].getLongitude()
            nodeLatitude = nodeslist[i].getLatitude()

            tb_nodeID = ttk.Entry(fr_tableheaders)
            tb_nodeID.insert(0,nodeID)
            tb_nodeID.configure(state="readonly")

            tb_nodeName = ttk.Entry(fr_tableheaders)
            tb_nodeName.insert(0,nodeName)
            tb_nodeName.configure(state="readonly")

            tb_nodeLong = ttk.Entry(fr_tableheaders)
            tb_nodeLong.insert(0,nodeLongitude)
            tb_nodeLong.configure(state="readonly")

            tb_nodeLat = ttk.Entry(fr_tableheaders)
            tb_nodeLat.insert(0,nodeLatitude)
            tb_nodeLat.configure(state="readonly")

            tb_nodeID.grid(row = i+1, column = 0, columnspan = 2, sticky=(tk.N, tk.E, tk.W), padx = 5)
            tb_nodeName.grid(row = i+1, column = 2, columnspan = 2, sticky=(tk.N, tk.E, tk.W), padx = 5)
            tb_nodeLong.grid(row = i+1, column = 4, columnspan = 2, sticky=(tk.N, tk.E, tk.W), padx = 5)
            tb_nodeLat.grid(row = i+1, column = 6, columnspan = 2, sticky=(tk.N, tk.E, tk.W), padx = 5)

            fr_actions = tk.Frame(fr_tableheaders)
            btn2 = []
            btn2.append(tk.Button(fr_actions, text = "Edit", command = lambda c=nodeID: self.nodePopup(popup,c)))
            btn2.append(tk.Button(fr_actions, text = "Delete", command = lambda c=nodeID: self.deleteNode(popup,c)))
            btn.append(btn2)
            btn2[0].grid(row = 0, column = 0, padx = 10)
            btn2[1].grid(row = 0, column = 1, padx = 10)
            fr_actions.grid(row = i+1, column = 8, columnspan = 2, sticky=(tk.N, tk.E, tk.W), padx = 5)

            self.c.coords(nodeWidget, nodeLongitude-10, nodeLatitude-10, nodeLongitude+10, nodeLatitude+10)
            self.c.coords(nodeWidget+1, nodeLongitude, nodeLatitude)

        fr_tableheaders.pack(pady = 10, padx = 10)

        popup.mainloop()

    def deleteNode(self, master, node_id):
        widgetid = self.network.getNodeById(node_id).getWidgetId()
        self.c.delete(widgetid)
        self.c.delete(widgetid+1)

        links = self.network.getLinksByNodeId(node_id)
        for i in range(len(links)):
            self.c.delete(links[i].getWidgetId())

        self.network.deleteNode(node_id)
        master.destroy()
        self.getNodesList(tk.Tk())
    
    def getLinksList(self, edit):
        #return self.network.getLinksList()
        #print(self.network.getLinksList())

        edit.destroy()

        popup = tk.Tk()

        popup.wm_title("Links List")

        linkslist = self.network.getLinksList()

        fr_tableheaders = tk.Frame(popup)

        lb_linkID = ttk.Label(fr_tableheaders, text="ID", font=NORM_FONT)
        lb_linkName = ttk.Label(fr_tableheaders, text="Name", font=NORM_FONT)
        lb_linkNodeA = ttk.Label(fr_tableheaders, text="Node A", font=NORM_FONT)
        lb_linkNodeB = ttk.Label(fr_tableheaders, text="Node B", font=NORM_FONT)
        lb_linkDirection = ttk.Label(fr_tableheaders, text="Direction", font=NORM_FONT)
        lb_linkCapacity = ttk.Label(fr_tableheaders, text="Capacity", font=NORM_FONT)
        lb_linkDistance = ttk.Label(fr_tableheaders, text="Distance", font=NORM_FONT)
        lb_linkActions = ttk.Label(fr_tableheaders, text="Actions", font=NORM_FONT)

        lb_linkID.grid(row = 0, column = 0, columnspan = 2, sticky=(tk.N, tk.E, tk.W), padx = 5)
        lb_linkName.grid(row = 0, column = 2, columnspan = 2, sticky=(tk.N, tk.E, tk.W), padx = 5)
        lb_linkNodeA.grid(row = 0, column = 4, columnspan = 2, sticky=(tk.N, tk.E, tk.W), padx = 5)
        lb_linkNodeB.grid(row = 0, column = 6, columnspan = 2, sticky=(tk.N, tk.E, tk.W), padx = 5)
        lb_linkDirection.grid(row = 0, column = 8, columnspan = 2, sticky=(tk.N, tk.E, tk.W), padx = 5)
        lb_linkCapacity.grid(row = 0, column = 10, columnspan = 2, sticky=(tk.N, tk.E, tk.W), padx = 5)
        lb_linkDistance.grid(row = 0, column = 12, columnspan = 2, sticky=(tk.N, tk.E, tk.W), padx = 5)
        lb_linkActions.grid(row = 0, column = 14, columnspan = 2, sticky=(tk.N, tk.E, tk.W), padx = 5)

        btn = []
        for i in range(len(linkslist)):
            activeLink = linkslist[i]
            linkID = activeLink.getID()
            linkName = activeLink.getName()
            linkWidget = activeLink.getWidgetId()
            linkNodeA = activeLink.getNodeA()
            linkNodeB = activeLink.getNodeB()
            linkDirection = activeLink.getDirection()
            linkCapacity = activeLink.getCapacity()
            linkDistance = activeLink.getDistance()
            
            print(type(linkNodeA), type(linkNodeB))
            tb_linkID = ttk.Entry(fr_tableheaders)
            tb_linkID.insert(0,linkID)
            tb_linkID.configure(state="readonly")

            tb_linkName = ttk.Entry(fr_tableheaders)
            tb_linkName.insert(0,linkName)
            tb_linkName.configure(state="readonly")

            tb_linkNodeA = ttk.Entry(fr_tableheaders)
            tb_linkNodeA.insert(0,linkNodeA.getName())
            tb_linkNodeA.configure(state="readonly")

            tb_linkNodeB = ttk.Entry(fr_tableheaders)
            tb_linkNodeB.insert(0,linkNodeB.getName())
            tb_linkNodeB.configure(state="readonly")

            tb_linkDirection = ttk.Entry(fr_tableheaders)
            tb_linkDirection.insert(0,linkDirection)
            tb_linkDirection.configure(state="readonly")

            tb_linkCapacity = ttk.Entry(fr_tableheaders)
            tb_linkCapacity.insert(0,linkCapacity)
            tb_linkCapacity.configure(state="readonly")

            tb_linkDistance = ttk.Entry(fr_tableheaders)
            tb_linkDistance.insert(0,linkDistance)
            tb_linkDistance.configure(state="readonly")

            tb_linkID.grid(row = i+1, column = 0, columnspan = 2, sticky=(tk.N, tk.E, tk.W), padx = 5)
            tb_linkName.grid(row = i+1, column = 2, columnspan = 2, sticky=(tk.N, tk.E, tk.W), padx = 5)
            tb_linkNodeA.grid(row = i+1, column = 4, columnspan = 2, sticky=(tk.N, tk.E, tk.W), padx = 5)
            tb_linkNodeB.grid(row = i+1, column = 6, columnspan = 2, sticky=(tk.N, tk.E, tk.W), padx = 5)
            tb_linkDirection.grid(row = i+1, column = 8, columnspan = 2, sticky=(tk.N, tk.E, tk.W), padx = 5)
            tb_linkCapacity.grid(row = i+1, column = 10, columnspan = 2, sticky=(tk.N, tk.E, tk.W), padx = 5)
            tb_linkDistance.grid(row = i+1, column = 12, columnspan = 2, sticky=(tk.N, tk.E, tk.W), padx = 5)

            fr_actions = tk.Frame(fr_tableheaders)
            btn2 = []
            btn2.append(tk.Button(fr_actions, text = "Edit", command = lambda c=linkID: self.linkPopup(popup,c)))
            btn2.append(tk.Button(fr_actions, text = "Delete", command = lambda c=linkID: self.deleteLink(popup,c)))
            btn.append(btn2)
            btn2[0].grid(row = 0, column = 0, padx = 10)
            btn2[1].grid(row = 0, column = 1, padx = 10)
            fr_actions.grid(row = i+1, column = 14, columnspan = 2, sticky=(tk.N, tk.E, tk.W), padx = 5)

            #self.c.coords(linkWidget, linkLongitude-10, linkLatitude-10, linkLongitude+10, linkLatitude+10)

        fr_tableheaders.pack(pady = 10, padx = 10)

        popup.mainloop()

    def addNode(self, event):
        global node_id
        
        node_id = self.c.create_oval(10, 10, 20, 20, fill='orange', outline='blue', tags='node')
        

        #if object_id is not None:
        coord = self.c.coords(node_id)
        width = coord[2] - coord[0]
        height = coord[3] - coord[1]

        self.c.coords(node_id, event.x - (width / 2) - 7, event.y - (height / 2) - 7, event.x+width, event.y+height)
        self.c.create_text(event.x , event.y, text = self.node_ctr, state = tk.NORMAL, tags = 'node')
        self.ovals[node_id] = self.c.coords(node_id)
        if self.network.getNodeById(node_id) is None:
            name = "Node %s" % self.node_ctr
            lat = event.y
            lng = event.x
            self.network.createNode(self.node_ctr, node_id, name, lng, lat)
            

        elif self.network.getNodeById(node_id) is not None:
            name = self.network.getNodeById(node_id).getName()
            lat = self.network.getNodeById(node_id).getLatitude()
            lng = self.network.getNodeById(node_id).getLongitude()
            self.network.createNode(self.node_ctr, node_id, name, lng, lat)

        self.node_ctr += 1
            
    def nodePopup(self, master, id):
        popup = tk.Tk()

        active = self.network.getNodeById(id)

        def savenode(active_id, entry_id, widget_id, name, lng, lat):
            self.network.updateNode(active.getID(), entry_id, widget_id, name, lng, lat)
            master.destroy()
            self.getNodesList(popup)

        popup.wm_title("Node Properties")

        label_id = ttk.Label(popup, text = "Node ID: ", font = NORM_FONT, anchor = tk.W)
        entry_id = ttk.Entry(popup)
        entry_id.insert(0, active.getID())
        entry_id.config(state=tk.DISABLED)
        label_id.grid(row=0)
        entry_id.grid(row=0, column=1)

        label_name = ttk.Label(popup, text = "Node Name: ", font = NORM_FONT, anchor = tk.W)
        entry_name = ttk.Entry(popup)
        entry_name.insert(0, active.getName())
        label_name.grid(row=1)
        entry_name.grid(row=1, column=1)

        label_long = ttk.Label(popup, text = "Node Longitude: ", font = NORM_FONT, anchor = tk.W)
        entry_long = ttk.Entry(popup)
        entry_long.insert(0, active.getLongitude())
        label_long.grid(row=2)
        entry_long.grid(row=2, column=1)

        label_lat = ttk.Label(popup, text = "Node Latitude: ", font = NORM_FONT, anchor = tk.W)
        entry_lat = ttk.Entry(popup)
        entry_lat.insert(0, active.getLatitude())
        label_lat.grid(row=3)
        entry_lat.grid(row=3, column=1)

        B1 = ttk.Button(popup, text="Save", command = lambda: savenode(active.getID(), entry_id.get(), active.getWidgetId(), entry_name.get(), entry_long.get(), entry_lat.get()))
        B1.grid(row=5, column=0)
        B2 = ttk.Button(popup, text="Cancel", command = popup.destroy)
        B2.grid(row=5, column=1)

        entry_name.focus_set()

        popup.mainloop()

    def linkPopup(self, master, id):
        popup = tk.Tk()

        active = self.network.getLinkById(id)

        def savelink(active_id, entry_id, widget_id, name, node1, node2, direction, capacity, distance):
            self.c.itemconfigure(link_id, width = capacity, arrow=tk.LAST)
            node1 = self.network.getNodeById(int(node1))
            node2 = self.network.getNodeById(int(node2))
            self.network.updateLink(active_id, entry_id, widget_id, name, node1, node2, direction, capacity, distance)
            master.destroy()
            self.getLinksList(popup)

        popup.wm_title("Link Properties")

        label_id = ttk.Label(popup, text = "Link ID: ", font = NORM_FONT, anchor = tk.W)
        entry_id = ttk.Entry(popup)
        entry_id.insert(0, active.getID())
        entry_id.config(state=tk.DISABLED)
        label_id.grid(row=0)
        entry_id.grid(row=0, column=1)

        label_name = ttk.Label(popup, text = "Link Name: ", font = NORM_FONT, anchor = tk.W)
        entry_name = ttk.Entry(popup)
        entry_name.insert(0, active.getName())
        label_name.grid(row=1)
        entry_name.grid(row=1, column=1)

        label_long = ttk.Label(popup, text = "Start Node: ", font = NORM_FONT, anchor = tk.W)
        entry_long = ttk.Entry(popup)
        entry_long.insert(0, active.getNodeA().getName())
        label_long.grid(row=2)
        entry_long.grid(row=2, column=1)

        label_lat = ttk.Label(popup, text = "End Node: ", font = NORM_FONT, anchor = tk.W)
        entry_lat = ttk.Entry(popup)
        entry_lat.insert(0, active.getNodeB().getName())
        label_lat.grid(row=3)
        entry_lat.grid(row=3, column=1)

        sep = ttk.LabelFrame(popup, text="Advanced Properties")
        sep.grid(row=4, columnspan = 2, padx = 10, pady = 10)

        lb_weight = ttk.Label(sep, text = "Capacity: ", font = NORM_FONT, anchor = tk.W)
        lb_weight.grid(row=2)
        tb_weight = ttk.Entry(sep)
        tb_weight.insert(0, active.getCapacity())
        tb_weight.grid(row=2, column=1, columnspan = 2)

        lb_dist = ttk.Label(sep, text = "Distance: ", font = NORM_FONT, anchor = tk.W)
        lb_dist.grid(row=1)
        tb_dist = ttk.Entry(sep)
        tb_dist.insert(0, active.getDistance())
        tb_dist.grid(row=1, column=1, columnspan=2)
        

        B1 = ttk.Button(popup, text="Save", command = lambda: savelink(active.getID(), entry_id.get(), active.getWidgetId(), entry_name.get(), entry_long.get(), entry_lat.get(), active.getDistance(), tb_weight.get(), tb_dist.get()))
        B1.grid(row=7, column=0)
        B2 = ttk.Button(popup, text="Cancel", command = popup.destroy)
        B2.grid(row=7, column=1)

        popup.mainloop()

    def deleteLink(self, master, link_id):
        widgetid = self.network.getLinkById(link_id).getWidgetId()
        self.c.delete(widgetid)
        self.network.deleteLinkById(link_id)
        master.destroy()
        self.getLinksList(tk.Tk())
   
    def getOrigin(self, event):
        global init_x, init_y, origin_widget_node, link_id, btn1pressed, origin_node
        
        btn1pressed = True
        init_x = None
        init_y = None
        origin_widget_node = None
        link_id = None
        origin_node = None
        
        # Find all clicked items
        self.selected = self.c.find_overlapping(event.x, event.y, event.x, event.y)
        # Get first selected item
        origin_widget_node = self.selected[0]
        origin_node = self.c.itemcget(self.selected[0]+1, 'text')
        coord = self.c.coords(origin_widget_node)
        width = coord[2] - coord[0]
        height = coord[3] - coord[1]
        if(self.c.type(origin_widget_node) == "oval"):
            init_x = coord[2] - (width / 2)
            init_y = coord[3] - (height / 2)
            link_id = self.c.create_line(init_x, init_y, init_x, init_y)
        else:
            pass
    
    def addLink(self, event):
        if btn1pressed == True:
            self.c.coords(link_id, init_x, init_y, event.x, event.y)
    
    def getFinal(self, event):
        global end_x, end_y, end_widget_node, btn1pressed, end_node
        
        btn1pressed = False
        end_x = None
        end_y = None
        end_widget_node = None
        end_node = None

        # Find all clicked items
        self.selected = self.c.find_overlapping(event.x, event.y, event.x, event.y)
        # Get first selected item
        if(len(self.selected) >= 2):
            end_widget_node = self.selected[0]
            end_node = self.c.itemcget(self.selected[0]+1, 'text')
            coord = self.c.coords(end_widget_node)
            width = coord[2] - coord[0]
            height = coord[3] - coord[1]
            if(self.c.type(end_widget_node) == "oval"):
                print(end_node, end_widget_node)
                end_x = coord[2] - (width / 2)
                end_y = coord[3] - (height / 2)
                delta_y = end_y - init_y
                delta_x = end_x - init_x
                
                slope = -(delta_y) / delta_x
                
                intercept = (-1 * end_y) - (slope * end_x)
                
                end_yy = -1 * end_y
                
                # Getting the intersection points between the line segment and the end node
                a = 1 + slope**2
                b = (-2 * end_x) + (2 * slope * intercept) - (2 * slope * end_yy)
                c = end_x**2 + intercept**2 - (2 * intercept * end_yy) + end_yy**2 - 25
                
                det = b**2 - 4*a*c
                
                if(det >= 0):
                    x_1 = (-b + (det)**0.5)/(2*a)
                    x_2 = (-b - (det)**0.5)/(2*a)
                    
                    #print("X1: ", x_1, " X2: ", x_2)
                    
                    if delta_x > 0:
                        if init_x < x_1 < end_x:
                            end_x = x_1 - .5
                        elif init_x < x_2 < end_x:
                            end_x = x_2 - .5
                        else:
                            pass
                    elif delta_x < 0:
                        if end_x < x_1 < init_x:
                            end_x = x_1 + .5
                        elif end_x < x_2 < init_x:
                            end_x = x_2 + .5
                        else:
                            pass
                    else:
                        pass
                    
                    end_y = (slope * end_x) + intercept
                else:
                    print("TADA")
                
                self.c.coords(link_id,init_x, init_y, end_x, -1 * end_y)
                self.c.tag_lower(link_id)

                name = "Link %s" % self.link_ctr
                node1 = origin_node
                node2 = end_node

                #print(type(self.network.getNodeById(node1)), type(self.network.getNodeById(node2)))
                self.network.createLink(self.link_ctr, link_id, name, int(node1), int(node2))

                self.link_ctr += 1
            else: self.c.delete(link_id)
        else: self.c.delete(link_id)
        
    def checkObject(self, event):
        if self.c.find_withtag(tk.CURRENT):
            #self.c.itemconfigure(tk.CURRENT)
            pass
        
    def startMove(self, event):
        # find all clicked items
        self.selected = self.c.find_overlapping(event.x, event.y, event.x, event.y)
        # get first selected item
        self.selected = self.selected[0]
        self.c.itemconfigure(self.selected+1, state = tk.HIDDEN)

    def moveObject(self, event):
        # move selected item
        self.c.coords(self.selected, event.x-10, event.y-10, event.x+10,event.y+10)

    def stopMove(self, event):
        # delete or release selected item
        if 100 < event.x < 300 and 250 < event.y < 350:
            self.c.delete(self.selected)
            del self.ovals[self.selected]
        else:
            self.c.coords(self.selected, event.x-10, event.y-10, event.x+10,event.y+10)
            self.c.coords(self.selected+1, event.x, event.y)
            self.c.itemconfigure(self.selected+1, state = tk.NORMAL)
            node_id = self.c.itemcget(self.selected+1, 'text')
            self.network.updateNodeCoords(int(node_id), event.x, event.y)
        # clear it so you can use it to check if you are draging item
        self.selected = None

class SearchLocation(tk.Frame):
    def __init__ (self, parent, controller):
        self.controller = controller
        tk.Frame.__init__ (self, parent)
        label = tk.Label(self, text="Search for Location", font=LARGE_FONT)
        label.pack(pady = 10, padx = 10)  

app = RoadNetworkSimulator()
app.mainloop()