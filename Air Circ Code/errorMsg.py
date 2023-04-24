from tkinter import *
from tkinter import ttk

class errorMsg:
    def __init__(self, master, msg):
        self.master = master
        self.msg = msg
        
        # Create Vis
        self.frame = ttk.Frame(self.master, width=200, height=100)
        self.frame.grid()
        
        # Input label
        self.FrameTitleLabel = ttk.Label(self.frame, text = self.msg, justify='center').grid(column=1, row=1, columnspan=2, pady=5, padx=10)
        
        # Cancel
        self.cancelBtn = ttk.Button(self.frame, text = 'Ok', command= self.CloseWin).grid(column=1, row=2, pady=5, padx= 10, sticky=N+W+S+E)
        self.master.bind('<Escape>', self.Extfunc)  

    def Extfunc(self, event):
        self.CloseWin()
        
    def CloseWin(self):
        self.master.destroy()
        

def newMsg(master, msg, title='Error'):
    newWindow = Toplevel(master)
    newWindow.title(title)
    errorMsg(newWindow, msg)
    newWindow.grab_set()
    newWindow.wait_window()
    newWindow.grab_release()
