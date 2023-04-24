from tkinter import *
from tkinter import ttk

class VisNewCalc:
    def __init__(self, master):
        self.master = master
        self.name = ''
        self.calctype = ''
        self.success = False
        # Create Vis
        self.frame = ttk.Frame(self.master, width=200, height=100)
        self.frame.grid()
        
        # Input label
        self.FrameTitleLabel = ttk.Label(self.frame, text = 'New Calc Name:', justify='center').grid(column=1, row=1, columnspan=2, pady=10)

        # Fail Label
        self.nameEmptyLabel = ttk.Label(self.frame, text='Name must not be Blank', foreground='red')
        # Select calc type
        self.calc_options = ["Combined ventilation (JMS machines)", "Axial only ventilation times"]
        self.variable = StringVar(master)
        self.variable.set(self.calc_options[1]) # default value

        self.calculatoroption = OptionMenu(master, self.variable, *self.calc_options).grid(column=4, row=0, columnspan=2, pady=10)
                 
        # Get Calc Name
        self.nameTxtBx = Entry(self.frame)
        self.nameTxtBx.grid(column=1, row=2, columnspan=2, padx=40)

        # Create New Calc
        self.accptBtn = ttk.Button(self.frame, text = 'Create', command= self.CreateCalc).grid(column=2,row=5, pady=10)
        self.master.bind('<Return>', self.Acptfunc)  

        # Cancel New Calc
        self.cancelBtn = ttk.Button(self.frame, text = 'Cancel', command= self.CloseWin).grid(column=1, row=5, pady=10)
        self.master.bind('<Escape>', self.Extfunc)  

    def CreateCalc(self):
        tempname = self.nameTxtBx.get()
        calctype = self.variable.get()

        if tempname and tempname.strip(): #check if null, empty or spaces
            # accept input
            self.name = tempname
            self.calctype = calctype
            self.success= True
            self.CloseWin()
            return calctype
            
        else:
            # reject input
            self.nameEmptyLabel.grid(column=1, row=3, columnspan=2)
    
    def Acptfunc(self, event):
        self.CreateCalc()

    def Extfunc(self, event):
        self.CloseWin()
        
    def CloseWin(self):
        self.master.destroy()
        
