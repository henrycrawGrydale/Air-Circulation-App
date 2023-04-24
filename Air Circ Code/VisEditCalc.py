from tkinter import *
from tkinter import ttk
import CalculationClass as calcClass
from math import pi, log, pow, exp
import numpy as np
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import errorMsg
from tkinter import filedialog
import pandas as pd
import AdvSettings
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
from PIL import ImageTk,Image  
import subprocess
import os
import VisResults as Res

class VisEditCalc:
    def __init__(self, master, CalcObj: calcClass.AirCircCalc):
        self.CalcObj = CalcObj
        self.master = master
        VisEditCalc.master=master
        self.doLoop = True
        
        # Frame
        self.frame = ttk.Frame(self.master, padding=10,)
        self.frame.grid(columnspan=3)
        self.FrameTitleLabel = ttk.Label(self.frame, text = 'Air Circ Calculation: '+CalcObj.name, justify='center').grid(column=1, row=1, columnspan=3)
        VisEditCalc.time = 40
        # InitUI
        self.InitUI()
        self.ShowInputs()
        self.insertdropdown(self)
        
        #Calculation Obj
        self.calcVis = VisCalculation(self, self.CalcObj)
        
    def InitUI(self):
        # Value Inputs
        # Cross Section
        self.TunDiaLabel = ttk.Label(self.frame, text = 'Main Tunnel Diameter (m)')
        self.TunDiaEntry = ttk.Entry(self.frame)
        self.TunDiaEntry.insert(0, self.CalcObj.TunDiameter)

        #FlowRateTunnel
        self.FlowRateLabel = ttk.Label(self.frame, text = 'Main Tunnel FLow Rate (m³/s)')
        self.FlowRateEntry = ttk.Entry(self.frame)
        self.FlowRateEntry.insert(0, self.CalcObj.FlowRate)


        # Distances Dropdown
        self.calc_options = ["Default"]
        intervalNo = np.arange(1,6,1)
        for inter in intervalNo:
            self.calc_options.append(inter)

        self.variable = StringVar(self.master)
        
        self.DistanceLabel = ttk.Label(self.frame, text = 'Distance intervals')
        self.DistanceDropDown = ttk.OptionMenu(self.frame,self.variable,self.CalcObj.DistInt, *self.calc_options, command= self.insertdropdown)
        
        self.DistancesLabel = ttk.Label(self.frame, text= 'Distances:')
        self.Distance1Label = ttk.Label(self.frame, text = '1')
        self.Distance1Entry = ttk.Entry(self.frame)
        self.Distance2Label = ttk.Label(self.frame, text = '2')
        self.Distance2Entry = ttk.Entry(self.frame)
        self.Distance3Label = ttk.Label(self.frame, text = '3')
        self.Distance3Entry = ttk.Entry(self.frame)
        self.Distance4Label = ttk.Label(self.frame, text = '4')
        self.Distance4Entry = ttk.Entry(self.frame)
        self.Distance5Label = ttk.Label(self.frame, text = '5')
        self.Distance5Entry = ttk.Entry(self.frame)
        
        
        # Save and Exit
        self.AcceptBtn = ttk.Button(self.frame, text='Save & Exit',command= self.Exit)
        self.master.bind('<Escape>', self.Extfunc)  

        # Calculate
        self.CalcBtn = ttk.Button(self.frame, text='Calculate',command= self.Calculate)

        # Exit 
       # self.cancelBtn = ttk.Button(self.frame, text = 'Exit', command= self.CloseWin).grid(column=1, row=9, pady=10)

        # Advanced Settings
        self.AdvBtn = ttk.Button(self.frame, text = 'Default Settings', command = self.openAdv)

        
            
    def ShowInputs(self):
        # Place Input Widgets
        self.TunDiaLabel.grid(column=1, row=3, columnspan=2)
        self.TunDiaEntry.grid(column=3 , row=3)

        self.FlowRateLabel.grid(column=1, row=4, columnspan=2)
        self.FlowRateEntry.grid(column=3 , row=4)

        self.DistanceLabel.grid(column=1, row=5, columnspan=2)
        self.DistanceDropDown.grid(column=3, row=5, columnspan =2)

        

        self.AcceptBtn.grid(column=2, row=6) 
        self.CalcBtn.grid(column=3, row=6) 
        self.AdvBtn.grid(column =1 , row = 6)
       

    def HideInputs(self):
        self.TunDiaLabel.grid_forget()
        self.TunDiaEntry.grid_forget()

        self.FlowRateLabel.grid_forget()
        self.FlowRateEntry.grid_forget()

        self.Distance1Label.grid_forget()
        self.Distance2Label.grid_forget()
        self.Distance3Label.grid_forget()
        self.Distance4Label.grid_forget()
        self.Distance5Label.grid_forget()
        
        self.Distance1Entry.grid_forget()
        self.Distance2Entry.grid_forget()
        self.Distance3Entry.grid_forget()
        self.Distance4Entry.grid_forget()
        self.Distance5Entry.grid_forget()


        self.AcceptBtn.grid_forget()
        self.CalcBtn.grid_forget()
        self.AdvBtn.grid_forget()
    def Calculate(self):
        # Save vars and close window
        if self.Save(True):
            # Hide Inputs Buttons
            self.HideInputs()
            
            # Load Calculation class
            self.calcVis.ShowOutputs()


           
    def Save(self, isCalc = False):
        # Get Vars from Inputs
        TunDiameter = self.TunDiaEntry.get()
        FlowRate = self.FlowRateEntry.get()
        distanceinterval = self.variable.get()
        
        if self.variable.get() == 'Default':
            length = np.arange(25,126,25)
        elif self.variable.get() == '1':
            length = [float(self.Distance1Entry.get())]
        elif self.variable.get() == '2': 
            length = [float(self.Distance1Entry.get()), float(self.Distance2Entry.get())] 
        elif self.variable.get() == '3': 
            length = [float(self.Distance1Entry.get()), float(self.Distance2Entry.get()),float(self.Distance3Entry.get())]
        elif self.variable.get() == '4': 
            length = [float(self.Distance1Entry.get()), float(self.Distance2Entry.get()),float(self.Distance3Entry.get()),float(self.Distance4Entry.get())]
        elif self.variable.get() == '5': 
            length = [float(self.Distance1Entry.get()), float(self.Distance2Entry.get()),float(self.Distance3Entry.get()),float(self.Distance4Entry.get()),float(self.Distance5Entry.get())]
        #Check Inputs
        if self.is_number(TunDiameter, isCalc)\
              and self.is_number(FlowRate, isCalc):
               
            # Save Inputs
            self.CalcObj.TunDiameter = float(TunDiameter)
            self.CalcObj.FlowRate = float(FlowRate)
            self.CalcObj.Length = length
            self.CalcObj.DistInt = distanceinterval

            
            return True
        else:
            errorMsg.newMsg(self.master, 'Inputs Must Be Numbers\nOnly Emulsion and ANFO may be 0')
            return False

    def Exit(self):
        if self.Save():
            self.doLoop = False
            self.CloseWin()
        
    def Extfunc(self,event):
        self.Exit()
        
    def CloseWin(self):
        self.master.destroy()

    def is_number(self, string, isCalc = False):
        try:
            float(string)
    
        except ValueError:
            return False
        else:
            if isCalc and float(string) == 0:
                return False
            else: 
                return True
    def openAdv(self):  
              
            newWindow = Toplevel(self.master)
            newWindow.title("Advanced Settings")
            advset = AdvSettings.Advsettings(newWindow, self.CalcObj)
            newWindow.grab_set()
            newWindow.wait_window()
            newWindow.grab_release()
    
    def insertdropdown(self,event):
        self.AcceptBtn.grid_forget()
        self.CalcBtn.grid_forget()
        self.AdvBtn.grid_forget()
        interNo = self.variable.get()
        print(interNo)
        if interNo == 'Default':
            self.AcceptBtn.grid(column=2, row=8) 
            self.CalcBtn.grid(column=3, row=8) 
            self.AdvBtn.grid(column =1 , row = 8)
            return
        if interNo == '1':
            self.DistancesLabel.grid( column=1,row=6,columnspan=2)
            self.Distance1Label.grid(column=1, row=7,columnspan= 2)
            self.Distance1Entry.grid(column=3, row=7)
            if len(self.Distance1Entry.get()) == 0 and len(self.CalcObj.Length) == 1:
                self.Distance1Entry.insert(0, self.CalcObj.Length[0])

            self.AcceptBtn.grid(column=2, row=8) 
            self.CalcBtn.grid(column=3, row=8) 
            self.AdvBtn.grid(column =1 , row = 8)
            
            self.Distance2Label.grid_forget()
            self.Distance3Label.grid_forget()
            self.Distance4Label.grid_forget()
            self.Distance5Label.grid_forget()
            
            self.Distance2Entry.grid_forget()
            self.Distance3Entry.grid_forget()
            self.Distance4Entry.grid_forget()
            self.Distance5Entry.grid_forget()

            
        elif interNo == '2':
            self.DistancesLabel.grid( column=1,row=6,columnspan=2)
            self.Distance1Label.grid(column=1, row=7,columnspan= 2)
            self.Distance1Entry.grid(column=3, row=7)
            if len(self.Distance1Entry.get()) == 0 and len(self.CalcObj.Length) == 2:
                self.Distance1Entry.insert(0, self.CalcObj.Length[0])
            self.Distance2Label.grid(column=1, row=8,columnspan= 2)
            self.Distance2Entry.grid(column=3,row=8)
            if len(self.Distance2Entry.get()) == 0 and len(self.CalcObj.Length) == 2:
                self.Distance2Entry.insert(0, self.CalcObj.Length[1])

            self.AcceptBtn.grid(column=2, row=9) 
            self.CalcBtn.grid(column=3, row=9) 
            self.AdvBtn.grid(column =1 , row = 9)
            
            self.Distance3Label.grid_forget()
            self.Distance4Label.grid_forget()
            self.Distance5Label.grid_forget()

            self.Distance3Entry.grid_forget()
            self.Distance4Entry.grid_forget()
            self.Distance5Entry.grid_forget()

            

        elif interNo == '3':
            self.DistancesLabel.grid( column=1,row=6,columnspan=2)
            self.Distance1Label.grid(column=1, row=7,columnspan= 2)
            self.Distance1Entry.grid(column=3, row=7)
            if len(self.Distance1Entry.get()) == 0 and len(self.CalcObj.Length) == 3:
                self.Distance1Entry.insert(0, self.CalcObj.Length[0])
            self.Distance2Label.grid(column=1, row=8,columnspan= 2)
            self.Distance2Entry.grid(column=3,row=8)
            if len(self.Distance2Entry.get()) == 0 and len(self.CalcObj.Length) == 3:
                self.Distance2Entry.insert(0, self.CalcObj.Length[1])
            self.Distance3Label.grid(column=1, row=9,columnspan= 2)
            self.Distance3Entry.grid(column=3,row=9)
            if len(self.Distance3Entry.get()) == 0 and len(self.CalcObj.Length) == 3:
                self.Distance3Entry.insert(0, self.CalcObj.Length[2])

            self.AcceptBtn.grid(column=2, row=10) 
            self.CalcBtn.grid(column=3, row=10) 
            self.AdvBtn.grid(column =1 , row = 10)
            
            self.Distance4Label.grid_forget()
            self.Distance5Label.grid_forget()

            self.Distance4Entry.grid_forget()
            self.Distance5Entry.grid_forget()

            
            
        elif interNo == '4':
            self.DistancesLabel.grid( column=1,row=6,columnspan=2)
            self.Distance1Label.grid(column=1, row=7,columnspan= 2)
            self.Distance1Entry.grid(column=3, row=7)
            if len(self.Distance1Entry.get()) == 0 and len(self.CalcObj.Length) == 4:
                self.Distance1Entry.insert(0, self.CalcObj.Length[0])
            self.Distance2Label.grid(column=1, row=8,columnspan= 2)
            self.Distance2Entry.grid(column=3,row=8)
            if len(self.Distance2Entry.get()) == 0 and len(self.CalcObj.Length) == 4:
                self.Distance2Entry.insert(0, self.CalcObj.Length[1])
            self.Distance3Label.grid(column=1, row=9,columnspan= 2)
            self.Distance3Entry.grid(column=3,row=9)
            if len(self.Distance3Entry.get()) == 0 and len(self.CalcObj.Length) == 4:
                self.Distance3Entry.insert(0, self.CalcObj.Length[2])
            self.Distance4Label.grid(column=1, row=10, columnspan=2)
            self.Distance4Entry.grid(column=3,row=10)
            if len(self.Distance4Entry.get()) == 0 and len(self.CalcObj.Length) == 4:
                self.Distance4Entry.insert(0, self.CalcObj.Length[3])
            
            self.AcceptBtn.grid(column=2, row=11) 
            self.CalcBtn.grid(column=3, row=11) 
            self.AdvBtn.grid(column =1 , row = 11)

            self.Distance5Label.grid_forget()
            self.Distance5Entry.grid_forget()

            
        elif interNo == '5':
            self.DistancesLabel.grid( column=1,row=6,columnspan=2)
            self.Distance1Label.grid(column=1, row=7,columnspan= 2)
            self.Distance1Entry.grid(column=3, row=7)
            if len(self.Distance1Entry.get()) == 0 and len(self.CalcObj.Length) == 5:
                self.Distance1Entry.insert(0, self.CalcObj.Length[0])
            self.Distance2Label.grid(column=1, row=8,columnspan= 2)
            self.Distance2Entry.grid(column=3,row=8)
            if len(self.Distance2Entry.get()) == 0 and len(self.CalcObj.Length) == 5:
                self.Distance2Entry.insert(0, self.CalcObj.Length[1])
            self.Distance3Label.grid(column=1, row=9,columnspan= 2)
            self.Distance3Entry.grid(column=3,row=9)
            if len(self.Distance3Entry.get()) == 0 and len(self.CalcObj.Length) == 5:
                self.Distance3Entry.insert(0, self.CalcObj.Length[2])
            self.Distance4Label.grid(column=1, row=10, columnspan=2)
            self.Distance4Entry.grid(column=3,row=10)
            if len(self.Distance4Entry.get()) == 0 and len(self.CalcObj.Length) == 5:
                self.Distance4Entry.insert(0, self.CalcObj.Length[3])
            self.Distance5Label.grid(column=1, row=11, columnspan=2)
            self.Distance5Entry.grid(column=3,row=11)
            if len(self.Distance5Entry.get()) == 0 and len(self.CalcObj.Length) == 5:
                self.Distance5Entry.insert(0, self.CalcObj.Length[4])

            self.AcceptBtn.grid(column=2, row=12) 
            self.CalcBtn.grid(column=3, row=12) 
            self.AdvBtn.grid(column =1 , row = 12)
        
            
        elif interNo == 'Default':
            self.length = np.arange(25,101,25) 

    def openResults(self):
        print('open')
        newWindow = Toplevel(VisEditCalc.master)
        newWindow.title("Results")
        advset = Res.VisShowResults(newWindow, self.fig,self.tablesfig)
        newWindow.grab_set()
        newWindow.wait_window()
        newWindow.grab_release() 
    
    
        
    
###########################################################################

class VisCalculation(VisEditCalc):
    def __init__(self, Parent, CalcObj: calcClass.AirCircCalc):
        self.Parent = Parent
        self.frame = self.Parent.frame
        self.CalcObj = CalcObj
       

        # Output Vis
        self.Subtitle = ttk.Label(self.frame, text = 'Calculation Results')
        self.exportBtn = ttk.Button(self.frame, text='Export to Excel',command= self.ExportExcel)
        self.editBtn = ttk.Button(self.frame, text='Edit Inputs',command= self.EditInput)
        self.timeslctLabel = ttk.Label(self.frame, text = "Edit time")
        self.timeslctEntry = ttk.Entry(self.frame)
        self.edittimeBtn = ttk.Button(self.frame, text='Enter',command= self.Edittime)
        self.timeslctEntry.insert(0,VisEditCalc.time)
        # Generate Report Button
        self.GenReportBtn = ttk.Button(self.frame, text = 'Generate Tables', command = self.GenReport)
        
    def ShowOutputs(self):
        self.DoCalc1()
        self.ShowGraphs1()
        VisEditCalc.master.state('zoomed')
        self.Subtitle.grid(row=2, column= 2)
        self.exportBtn.grid(row=13, column=3)
        self.editBtn.grid(row=13, column=2)
        self.timeslctLabel.grid(row=13, column=4)
        self.timeslctEntry.grid(row=14, column=4)
        self.edittimeBtn.grid(row=13, column=5)
        self.GenReportBtn.grid(column = 2, row =14)

    def HideOutputs(self):
        self.Subtitle.grid_forget()
        self.exportBtn.grid_forget()
        self.editBtn.grid_forget()
        self.subframe.grid_forget()
        self.summaryframe.grid_forget()
        self.timeslctEntry.grid_forget()
        self.timeslctLabel.grid_forget()
        self.GenReportBtn.grid_forget()
        self.edittimeBtn.grid_forget()
      
        



    def EditInput(self):
        self.HideOutputs()
        VisEditCalc.master.state('normal')
        VisEditCalc.ShowInputs(self.Parent)
    def Edittime(self):
         VisEditCalc.time = float(self.timeslctEntry.get())
         self.subframe.grid_forget()
         self.summaryframe.grid_forget()
         self.DoCalc1()
         self.ShowGraphs1()

    def GenReport(self):
        VisEditCalc.openResults(self)

    def DoCalc1(self):
        #Prepare Vars
        CrossSection = pi*pow(self.CalcObj.TunDiameter /2 , 2)
        ExploQuan = CrossSection * 7.5      # Explostive Quantitiy
        Emuls10 = ExploQuan * 0.1   # Emulsion (10%)
        Anfo90 = ExploQuan * 0.9    # Anfo Explosive (90%)

        tve = ((Emuls10 * self.CalcObj.Emul)/1000 )\
            + ((Anfo90 * self.CalcObj.anfo)/1000) #Total Volume Emitted
        
        # Create Distance Array (5 to 100m Incrementing by 5)
        self.LengthArr = np.asarray(self.CalcObj.Length)    # Distance from site
        self.VolArr = self.LengthArr * CrossSection   # Volume of Tunne
        
        # Create Time Array (10 - 100min, step 10)
        self.TimeArr = np.arange(0,VisEditCalc.time,self.CalcObj.dt)    # Time Array
        
        # Concentration
        Conc = (tve/self.VolArr)* 1000000
        Concdust = (self.CalcObj.Dust50m*(1-((self.LengthArr-50)/self.LengthArr)))
        # Calculate Dilution Times for CO and NOx
        i = 0 # Time Index
        j = 0 # Volume Index
        self.DiluCONOx = np.zeros(( self.VolArr.size,self.TimeArr.size))
       
        for Vol in self.VolArr:
            for Time in self.TimeArr:
                self.DiluCONOx[i,j] = exp(-self.CalcObj.FlowRate*(Time*60)/Vol)*Conc[i]
                j = j + 1
            i = i + 1
            j = 0
        
        # Table calcs
        self.columns = np.arange(1,2,1)
        self.TableNOX = np.zeros((self.columns.size,self.VolArr.size ))
        i=0
        for nums in self.columns:
            for Vol in self.VolArr:
                self.TableNOX[i,j] = (-log(30/Conc[j])\
                                    * (Vol /(self.CalcObj.FlowRate * (70/100))) ) /60
                j = j + 1
            i = i + 1
            j = 0

        # Calculate Dilution Times for Dust
        i = 0 # Time Index
        j = 0 # Volume Index
        self.DiluDust = np.zeros(( self.VolArr.size,self.TimeArr.size))
        for Vol in self.VolArr:
            for Time in self.TimeArr:
                self.DiluDust[i,j] = exp(-self.CalcObj.FlowRate*(Time*60)/Vol)*Concdust[i]
                j = j + 1
            i = i + 1
            j = 0
    
        # Table calcs
        self.columns = np.arange(1,2,1)
        self.TableDust = np.zeros((self.columns.size,self.VolArr.size ))
        i=0
        for nums in self.columns:
            for Vol in self.VolArr:
                self.TableDust[i,j] = (-log(1.2/Concdust[j])\
                                    * (Vol /(self.CalcObj.FlowRate * (70/100))) ) /60
                j = j + 1
            i = i + 1
            j = 0
        
    def DoCalc2(self):
        #Prepare Vars
        CrossSection = pi*pow(self.CalcObj.TunDiameter /2 , 2)
        ExploQuan = CrossSection * 7.5      # Explostive Quantitiy
        Emuls10 = ExploQuan * 0.1   # Emulsion (10%)
        Anfo90 = ExploQuan * 0.9    # Anfo Explosive (90%)

        tve = ((Emuls10 * self.CalcObj.Emul)/1000 )\
            + ((Anfo90 * self.CalcObj.anfo)/1000) #Total Volume Emitted
        
        # Create Distance Array (5 to 100m Incrementing by 5)
        self.LengthArr = np.arange(5,100,5)      # Distance from site
        self.VolArr = self.LengthArr * CrossSection   # Volume of Tunne
        
        # Create Time Array (10 - 100min, step 10)
        self.TimeArr = np.arange(10,100,10)    # Time Array
        
        # Concentration
        Conc = (tve/self.VolArr)* 1000000
        Concdust = (self.CalcObj.Dust50m*(1-((self.LengthArr-50)/self.LengthArr)))
        # Calculate Dilution Times for CO and NOx
        i = 0 # Time Index
        j = 0 # Volume Index
        self.DiluCONOx = np.zeros((self.TimeArr.size, self.VolArr.size))
        for Time in self.TimeArr:
            for Vol in self.VolArr:
                self.DiluCONOx[i,j] = (-log(30/Conc[j])\
                                 * (Vol /(self.CalcObj.FlowRate * (Time/100))) ) /60
                j = j + 1
            i = i + 1
            j = 0
        
        
    
        # Calculate Dilution Times for Dust
        i = 0 # Time Index
        j = 0 # Volume Index
        self.DiluDust = np.zeros((self.TimeArr.size, self.VolArr.size))
        for Time in self.TimeArr:
            for Vol in self.VolArr:
                self.DiluDust[i,j] = (-log(self.CalcObj.STWA/Concdust[j])\
                                 * (Vol /(self.CalcObj.FlowRate * (Time/100))) ) /60
                j = j + 1
            i = i + 1
            j = 0


    def ShowGraphs1(self):
         # Create Sub Frame
        self.subframe = ttk.Frame(self.frame)
        
        # Legend and row labels
        columns = []
        for col in self.LengthArr:
            col = f"{col} m" 
            columns.append(col)

        # # Plot
        fig = Figure(figsize=(10, 5), dpi=100)
        fig.suptitle('Dilution Times for '+ self.CalcObj.name)
        fig.supxlabel('Time (min)')
        fig.supylabel('Concentration')

        plot1 = fig.add_subplot(121)
        
        plot1.grid(visible=True, axis='both', which='major')
        plot1.set_xlim([0,VisEditCalc.time])
        plot1.set_title('CO and NOx')
        for elem in self.DiluCONOx:
            plot1.plot(self.TimeArr,elem)
        plot1.legend(columns)
        
        plot2 = fig.add_subplot(122)
        plot2.grid(visible=True, axis='both', which='major')
        plot2.set_xlim([0,VisEditCalc.time])
        plot2.set_title('Dust')
        for elem in self.DiluDust:
            plot2.plot(self.TimeArr,elem)
        plot2.legend(columns)    

        # Plot tables
    
        self.summaryframe = ttk.Frame(self.frame)
        

       
        rows = self.TimeArr

        rows2 = columns

        columns2 = ['Time to reach ≤30ppm']
        tablesfig = Figure( figsize= (10,5), dpi = 180)
        columns3 = ['Time to reach ≤1.2 mg/m³']
        plot3 = tablesfig.add_subplot(121)

        # Add a table at the bottom of the axes
        plot3.table(cellText=self.DiluCONOx.transpose(),
                            rowLabels=rows,
                            colLabels=columns,
                            loc='center',
                            bbox = (0,0,1,1.1),
                            cellLoc = 'left',
                            fontsize = 50)

        # Adjust layout to make room for the table:
       

               
        plot3.axis('off')
        plot3.grid('off')

        simpletablesfig = Figure( figsize = (10,3), dpi = 100)
        plot4 = simpletablesfig.add_subplot(121)
        plot4.table(cellText=self.TableNOX.transpose(),
                            rowLabels=rows2,
                            colLabels=columns2, 
                            
                            loc='center',
                            bbox = (0,0,1,1.1),
                            cellLoc = 'left',
                            fontsize = 50)
        plot4.axis('off')
        plot4.grid('off')

      
        plot5 = simpletablesfig.add_subplot(122)
        plot5.table(cellText=self.TableDust.transpose(),
                            rowLabels=rows2,
                            colLabels=columns3, 
                            
                            loc='center',
                            bbox = (0,0,1,1.1),
                            cellLoc = 'left',
                            fontsize = 50)
        plot5.axis('off')
        plot5.grid('off')

        self.fig=fig
        self.tablesfig = tablesfig

        #VisEditCalc.openResults(self)

        self.canvas = FigureCanvasTkAgg(fig, master=self.subframe)
        self.summarycanvas = FigureCanvasTkAgg(simpletablesfig, master= self.summaryframe)
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=TRUE)
        self.summarycanvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=TRUE)   
        
        # Plot Toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.subframe)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        
        # Table toolbar

        self.ttoolbar = NavigationToolbar2Tk(self.summarycanvas, self.summaryframe)
        self.ttoolbar.update()
        self.summarycanvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        
        # Show Sub Frame
        self.subframe.grid(row=4, column=1, columnspan=6, rowspan=3)
        self.summaryframe.grid(row=9,columns=1, columnspan =6,rowspan =3)
    
    def ShowGraphs2(self):
        # Create Sub Frame
        self.subframe = ttk.Frame(self.frame)

        # # Plot
        fig = Figure(figsize=(10, 5), dpi=100)
        fig.suptitle('Dilution Times for '+ self.CalcObj.name)
        fig.supxlabel('Distance from Face (m)')
        fig.supylabel('Time (min)')

        plot1 = fig.add_subplot(221)
        plot1.grid(visible=True, axis='both', which='major')
        plot1.set_xlim([0,100])
        plot1.set_title('CO and NOx')
        for elem in self.DiluCONOx:
            plot1.plot(self.LengthArr,elem)
        plot1.legend(['10%','20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'])

        plot2 = fig.add_subplot(222)
        plot2.grid(visible=True, axis='both', which='major')
        plot2.set_xlim([0,100])
        plot2.set_title('Dust')
        for elem in self.DiluDust:
            plot2.plot(self.LengthArr,elem)
        plot2.legend(['10%','20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'])    
        
        

        
        self.canvas = FigureCanvasTkAgg(fig, master=self.mscanvas)
        self.canvas.draw() 
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.subframe)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        self.vbar=ttk.Scrollbar(self.subframe,orient=VERTICAL)
        self.vbar.config(command=self.subframe.yview)
        self.vbar.pack(side="right", fill="y")
        self.canvas.config( yscrollcommand=self.vbar.set)
        # Show Sub Frame
        self.subframe.grid(row=4, column=1, columnspan=6, rowspan=3)

    

    def ExportExcel(self):
        # Open File Dialog to Select Save Location
        filename = filedialog.asksaveasfilename(initialdir="=",
                                                 title="Export to Excel Format",
                                                 filetypes= (("comma-separated values",
                                                        "*.csv*"),
                                                       ("all files",
                                                        "*.*")))
        

        # Convert to Excel Format
        exportString = 'Dilution Of CONOx\n'
        distVar = 10
        # Distance Row
        exportString = exportString + "" + ','
        for k in self.LengthArr:
            exportString = exportString + f'{k}' + ','
        exportString = exportString + '\n'
        # Dilu CONOx
        for i in self.DiluCONOx:
            exportString =  exportString + f'{distVar}%'
            distVar = distVar + 10
           
            for j in i:
                exportString = exportString +',' + str(j)
            exportString = exportString + '\n'

        
        # Dilu Dust
        exportString = exportString + '\nDilution Of Dust\n'
        distVar = 10
        # Distance Row
        exportString = exportString + "" + ','
        for k in self.LengthArr:
            exportString = exportString + f'{k}' + ','
        exportString = exportString + '\n'

        for i in self.DiluDust:
            exportString = exportString + f'{distVar}%' 
            distVar = distVar + 10
            for j in i:
                exportString = exportString + ',' + str(j)
            exportString = exportString + '\n'

        
        # Check if File ends with .txt
        if not filename.endswith('.csv'):
            filename = filename + '.csv'
                    
        # Open Txt and save in excel format
        try:
            file = open(filename, 'w')
            file.write(exportString)
          
                      
            file.close  
           
            
        except:
            pass 
            # Return Failed
            errorMsg.newMsg(self.Parent.master, "Failed To Export to Excel")

        else:
            # Return Success
            errorMsg.newMsg(self.Parent.master, "Successfully Exported to Excel", 'Note')
            pass
