from tkinter import *
from tkinter import ttk


class VisConfirmInput:
    def __init__(self, master, msg):
        self.master = master
        self.msg = msg
        self.confirm = False
        # Create Vis
        self.frame = ttk.Frame(self.master, width=200, height=100)
        self.frame.grid()
        
        # Input label
        self.FrameTitleLabel = ttk.Label(self.frame, text = self.msg, justify='center').grid(column=1, row=1, columnspan=2, pady=10)
        
        # Confirm
        self.accptBtn = ttk.Button(self.frame, text = 'Confirm', command= self.ConfirmInput).grid(column=2,row=5, pady=10)
        self.master.bind('<Return>', self.Acptfunc)  

        # Cancel
        self.cancelBtn = ttk.Button(self.frame, text = 'Cancel', command= self.CloseWin).grid(column=1, row=5, pady=10)
        self.master.bind('<Escape>', self.Extfunc)  

    def ConfirmInput(self):
        self.confirm = True
        self.CloseWin()

    def Acptfunc(self, event):
        self.ConfirmInput()

    def Extfunc(self, event):
        self.CloseWin()
        
    def CloseWin(self):
        self.master.destroy()
        
