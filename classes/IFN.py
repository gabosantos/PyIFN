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
        mn_fileMenu.add_command(label = "Exit", command = "")
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
        self.c.pack(fill='both')    

        bt = tk.Button(master, text="Print Nodes", command = lambda: self.getNodesList())
        bt2 = tk.Button(master, text="Print Links", command = lambda: self.getLinksList())
        bt.pack(pady = 10, padx = 10)
        bt2.pack(pady = 10, padx = 10)

        self.c.bind("<Double-Button-1>", self.addNode)
        self.c.bind("<B1-Motion>", self.addLink)
        self.c.bind("<Button-1>", self.getOrigin)
        self.c.bind("<ButtonRelease-1>", self.getFinal)
        self.c.bind("<Button-3>", self.selectObject)
        self.c.tag_bind("node", "<B3-Motion>", self.moveObject)
        #self.c.tag_bind("node", "<Any-Enter>", self.mouseEnter)
        #self.c.tag_bind("node", "<Any-Leave>", self.mouseLeave)

    def mouseEnter(self, event):
        # the CURRENT tag is applied to the object the cursor is over.
        # this happens automatically.
        self.c.itemconfig(tk.CURRENT, fill="blue")
        try:
            self.c.itemconfig(self.c.find_above(tk.CURRENT)[0], state = tk.NORMAL)
        except:
            pass

    def mouseLeave(self, event):
        # the CURRENT tag is applied to the object the cursor is over.
        # this happens automatically.
        self.c.itemconfig(tk.CURRENT, fill="orange")
        try:
            self.c.itemconfig(self.c.find_above(tk.CURRENT)[0], state = tk.HIDDEN)
            pass
        except:
            pass        

    def getNodesList(self):
        #return self.network.getNodesList()
        #print(self.network.getNodesList())

        popup = tk.Tk()

        popup.wm_title("Nodes List")

        nodeslist = self.network.getNodesList()

        label = ""

        numcols = len(nodeslist[0])

        for i in range(len(nodeslist)):
            label = label + numcols + " " + nodeslist[i].getAllProperties() + "\n"

        label_list = ttk.Label(popup, text=label, font=NORM_FONT)
        label_list.pack(pady = 10, padx = 10)

        popup.mainloop()

    def getLinksList(self):
        #return self.network.getLinksList()
        #print(self.network.getLinksList())

        popup = tk.Tk()

        popup.wm_title("Links List")

        nodeslist = self.network.getLinksList()

        label = ""

        for i in range(len(nodeslist)):
            label = label + nodeslist[i].getName() + "\n"

        label_list = ttk.Label(popup, text=label, font=NORM_FONT)
        label_list.pack(pady = 10, padx = 10)

        popup.mainloop()

    def addNode(self, event):
        global node_id
        
        node_id = self.c.create_oval(10, 10, 20, 20, fill='orange', outline='blue', tags='node')
        
        #if object_id is not None:
        coord = self.c.coords(node_id)
        width = coord[2] - coord[0]
        height = coord[3] - coord[1]

        self.c.coords(node_id, event.x - (width / 2) - 7, event.y - (height / 2) - 7, event.x+width, event.y+height)

        if self.network.getNodeById(node_id) is None:
            name = ""
            lat = event.y
            lng = event.x
            self.nodePopup(node_id, name, lng, lat)

        elif self.network.getNodeById(node_id) is not None:
            name = self.network.getNodeById(node_id).getName()
            lat = self.network.getNodeById(node_id).getLatitude()
            lng = self.network.getNodeById(node_id).getLongitude()
            self.nodePopup(node_id, name, lng, lat)
            
    def nodePopup(self, id, name, lng, lat):
        popup = tk.Tk()

        def savenode(id, name, lng, lat):
            self.c.create_text(self.c.coords(node_id)[2] - ((self.c.coords(node_id)[2] - self.c.coords(node_id)[0])/2), self.c.coords(node_id)[3], text = name, state = tk.HIDDEN, tags = name)
            self.network.createNode(id, name, lng, lat)
            popup.destroy()

        def cancelnode(id):
            self.c.delete(id)
            popup.destroy()

        popup.wm_title("Node Properties")

        label_id = ttk.Label(popup, text = "Node ID: ", font = NORM_FONT, anchor = tk.W)
        entry_id = ttk.Entry(popup)
        entry_id.insert(0, id)
        entry_id.config(state=tk.DISABLED)
        label_id.grid(row=0)
        entry_id.grid(row=0, column=1)

        label_name = ttk.Label(popup, text = "Node Name: ", font = NORM_FONT, anchor = tk.W)
        entry_name = ttk.Entry(popup)
        entry_name.insert(0, name)
        label_name.grid(row=1)
        entry_name.grid(row=1, column=1)

        label_long = ttk.Label(popup, text = "Node Longitude: ", font = NORM_FONT, anchor = tk.W)
        entry_long = ttk.Entry(popup)
        entry_long.insert(0, lng)
        label_long.grid(row=2)
        entry_long.grid(row=2, column=1)

        label_lat = ttk.Label(popup, text = "Node Latitude: ", font = NORM_FONT, anchor = tk.W)
        entry_lat = ttk.Entry(popup)
        entry_lat.insert(0, lat)
        label_lat.grid(row=3)
        entry_lat.grid(row=3, column=1)

        B1 = ttk.Button(popup, text="Save", command = lambda: savenode(entry_id.get(), entry_name.get(), entry_long.get(), entry_lat.get()))
        B1.grid(row=5, column=0)
        B2 = ttk.Button(popup, text="Cancel", command = lambda: cancelnode(entry_id.get()))
        B2.grid(row=5, column=1)

        entry_name.focus_set()

        popup.mainloop()

    def LinkPopup(self, id, name, node1, node2):
        popup = tk.Tk()

        def savelink(id, name, node1, node2, capacity, distance):
            self.c.itemconfigure(link_id, width = capacity, arrow=tk.LAST)
            self.c.create_text(self.c.coords(link_id)[0] + ((self.c.coords(link_id)[2] - self.c.coords(link_id)[0])/2), self.c.coords(link_id)[1] + ((self.c.coords(link_id)[3] - self.c.coords(link_id)[1])/2), text = name)
            self.network.createLink(id, name, int(node1), int(node2))
            self.network.getLinkById(id).addProperties(capacity, distance)
            popup.destroy()

        def cancellink(id):
            self.c.delete(id)
            popup.destroy()

        popup.wm_title("Link Properties")

        label_id = ttk.Label(popup, text = "Link ID: ", font = NORM_FONT, anchor = tk.W)
        entry_id = ttk.Entry(popup)
        entry_id.insert(0, id)
        entry_id.config(state=tk.DISABLED)
        label_id.grid(row=0)
        entry_id.grid(row=0, column=1)

        label_name = ttk.Label(popup, text = "Link Name: ", font = NORM_FONT, anchor = tk.W)
        entry_name = ttk.Entry(popup)
        entry_name.insert(0, name)
        label_name.grid(row=1)
        entry_name.grid(row=1, column=1)

        label_long = ttk.Label(popup, text = "Start Node: ", font = NORM_FONT, anchor = tk.W)
        entry_long = ttk.Entry(popup)
        entry_long.insert(0, node1)
        label_long.grid(row=2)
        entry_long.grid(row=2, column=1)

        label_lat = ttk.Label(popup, text = "End Node: ", font = NORM_FONT, anchor = tk.W)
        entry_lat = ttk.Entry(popup)
        entry_lat.insert(0, node2)
        label_lat.grid(row=3)
        entry_lat.grid(row=3, column=1)

        sep = ttk.LabelFrame(popup, text="Advanced Properties")
        sep.grid(row=4, columnspan = 2, padx = 10, pady = 10)

        lb_weight = ttk.Label(sep, text = "Capacity: ", font = NORM_FONT, anchor = tk.W)
        lb_weight.grid(row=2)
        tb_weight = ttk.Entry(sep)
        tb_weight.insert(0, 1)
        tb_weight.grid(row=2, column=1, columnspan = 2)

        lb_dist = ttk.Label(sep, text = "Distance: ", font = NORM_FONT, anchor = tk.W)
        lb_dist.grid(row=1)
        tb_dist = ttk.Entry(sep)
        tb_dist.grid(row=1, column=1, columnspan=2)
        

        B1 = ttk.Button(popup, text="Save", command = lambda: savelink(entry_id.get(), entry_name.get(), entry_long.get(), entry_lat.get(), tb_weight.get(), tb_dist.get()))
        B1.grid(row=7, column=0)
        B2 = ttk.Button(popup, text="Cancel", command = lambda: cancellink(entry_id.get()))
        B2.grid(row=7, column=1)

        popup.mainloop()

    def addLink(self, event):
        global link_id
        
        if self.c.find_withtag(tk.CURRENT) and self.c.type(tk.CURRENT) == "oval":
            coord = self.c.coords(tk.CURRENT)
            width = coord[2] - coord[0]
            height = coord[3] - coord[1]
            init_x = coord[2] - (width / 2)
            init_y = coord[3] - (height / 2)
            
            link_id = self.c.create_line(init_x,init_y,init_x,init_y, tags='link', arrow = tk.LAST)
                #self.c.delete(self.link_id)
        else:
            pass

        while(event.type=="Motion"):
            self.c.coords(link_id, init_x, init_y, event.x, event.y)
    
    def getOrigin(self, event):
        global init_x, init_y, origin_node, link_id
        
        init_x = None
        init_y = None
        origin_node = None
        link_id = None
        
        if self.c.find_withtag(tk.CURRENT) and self.c.type(tk.CURRENT) == "oval":
            coord = self.c.coords(tk.CURRENT)
            width = coord[2] - coord[0]
            height = coord[3] - coord[1]
            init_x = coord[2] - (width / 2)
            init_y = coord[3] - (height / 2)
            origin_node = self.c.find_closest(event.x, event.y)
            self.origin_node = origin_node[0]
            #self.link_id = self.c.create_line(init_x,init_y,init_x,init_y, arrow=tk.LAST, arrowshape='30 84 60')
            #print("start: ", init_x, " ", init_y, " Node ID: ", self.origin_node, " Line ID: ", link_id, " Event Type: ", event.type)
        elif self.c.find_withtag('link'):
            pass
        else:
            pass
            #print(self.c.type(tk.CURRENT))
        
    def getFinal(self, event):
        global end_x, end_y, end_node
        
        end_x = None
        end_y = None
        
        end_node = None
        
        if self.c.find_withtag(tk.CURRENT) and self.c.type(tk.CURRENT) == "oval":
            coord = self.c.coords(tk.CURRENT)
            width = coord[2] - coord[0]
            height = coord[3] - coord[1]
            end_x = coord[2] - (width / 2)
            end_y = coord[3] - (height / 2)
            
            if link_id != None:
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
                self.end_node = self.c.find_closest(event.x, event.y)

                if self.network.getLinkById(link_id) is None:
                    name = ""
                    start = origin_node
                    end = self.end_node[0]
                    self.LinkPopup(link_id, name, start, end)

                elif self.network.getLinkById(link_id) is not None:
                    name = self.network.getLinkById(link_id).getName()
                    start = self.network.getLinkById(link_id).getStartNode()
                    end = self.network.getLinkById(link_id).getEndNode()
                    self.LinkPopup(link_id, name, start, end)
            else:
                pass
        elif self.c.find_withtag(tk.CURRENT) and self.c.type(tk.CURRENT) == "line":
            #print(self.c.find_closest(event.x, event.y, halo = 10))
            #self.c.delete(self.c.find_closest(event.x, event.y))
            pass
        else:
            pass
        
    def checkObject(self, event):
        if self.c.find_withtag(tk.CURRENT):
            #self.c.itemconfigure(tk.CURRENT)
            pass
        
    def selectObject(self, event):
        if self.c.find_withtag(tk.CURRENT):
            if self.c.type(tk.CURRENT) == "oval":
                self.c.itemconfig(tk.CURRENT, fill="blue", outline="orange")
                self.c.update_idletasks()
            elif self.c.type(tk.CURRENT) == "line":
                self.c.itemconfig(tk.CURRENT, )
                
    def moveObject(self, event):
        if self.c.find_withtag(tk.CURRENT):
            pass

    def addNodeValue(self, id):
        pass

class SearchLocation(tk.Frame):
    def __init__ (self, parent, controller):
        self.controller = controller
        tk.Frame.__init__ (self, parent)
        label = tk.Label(self, text="Search for Location", font=LARGE_FONT)
        label.pack(pady = 10, padx = 10)  

app = RoadNetworkSimulator()
app.mainloop()