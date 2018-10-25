import tkinter as tk

class StartPage(tk.Frame):
    
    def __init__ (self, parent, controller):

        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Welcome to Road Network Simulator\nBrought to you by the Ateneo Pedestrian and Traffic Computing Laboratory\nCopyright 2018", font=LARGE_FONT)
        label.pack(pady = 10, padx = 10)

        bt_createNewSimulation = tk.Button(self, text = "Create New Simulation", command = lambda: controller.show_frame(CreateNewSimulation))
        bt_createNewSimulation.pack(pady = 10)