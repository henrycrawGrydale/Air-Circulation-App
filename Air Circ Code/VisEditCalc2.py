from tkinter import *
from tkinter import ttk
import CalculationClass as calcClass
from math import pi , sqrt, pow, log,exp
import numpy as np
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import errorMsg
from tkinter import filedialog
import pandas as pd
import ffsolver 
import AdvSettings

class VisEditCalc2:
    def __init__(self, master, CalcObj: calcClass.AirCircCalc):
        self.Calclist = CalcObj
        self.CalcObj = CalcObj
        self.master = master
        print(self.master)
        self.doLoop = True
        # Frame
        self.frame = ttk.Frame(self.master, padding=10)
        self.frame.grid(columnspan=3)
        self.FrameTitleLabel = ttk.Label(self.frame, text = 'Air Circ Calculation: '+CalcObj.name, justify='center').grid(column=1, row=1, columnspan=3)
        VisEditCalc2.time = 100
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
        self.TunDiaEntry.bind('<FocusOut>', self.changestate)
        self.TunDiaEntry.insert(0, self.CalcObj.TunDiameter)

        # TunnelLength
        self.TunLeLabel = ttk.Label(self.frame, text = 'Main Tunnel Length (m)')
        self.TunLeEntry = ttk.Entry(self.frame)
        self.TunLeEntry.insert(0, self.CalcObj.TunLength)

        #FlowRateTunnel
        self.FlowRateLabel = ttk.Label(self.frame, text = 'Main Tunnel FLow Rate (m³/s)')
        self.FlowRateEntry = ttk.Entry(self.frame)
        self.FlowRateEntry.insert(0, self.CalcObj.FlowRate)

        #Explosive Quantity
        self.ExpQTYLabel = ttk.Label(self.frame, text = 'Explosive Quantity (kg)')
        self.ExpQTYEntry = ttk.Entry(self.frame)
        self.ExpQTYEntry.insert(0, self.CalcObj.ExpQTY)
             
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
        self.SaveBtn = ttk.Button(self.frame, text='Save & Exit',command= self.Exit)
        self.master.bind('<Escape>', self.Extfunc)  

        # Calculate
        self.CalcBtn = ttk.Button(self.frame, text='Calculate',command= self.Calculate)

        # Advanced Settings
        self.AdvBtn = ttk.Button(self.frame, text = 'Advanced Settings', command = self.openAdv)
      

        # Exit 
        #self.cancelBtn = ttk.Button(self.frame, text = 'Exit', command= self.CloseWin).grid(column=1, row=10, pady=10)
            
    def ShowInputs(self):
        # Place Input Widgets
        self.TunDiaLabel.grid(column=1, row=3, columnspan=2)
        self.TunDiaEntry.grid(column=3 , row=3)

        self.TunLeLabel.grid(column=1, row=4, columnspan=2)
        self.TunLeEntry.grid(column=3 , row=4)
        
        self.FlowRateLabel.grid(column=1, row=5, columnspan=2)
        self.FlowRateEntry.grid(column=3 , row=5)

        self.ExpQTYLabel.grid(column=1, row=6, columnspan=2)
        self.ExpQTYEntry.grid(column=3 , row=6)

        self.DistanceLabel.grid(column=1, row=7, columnspan=2)
        self.DistanceDropDown.grid(column=3, row=7, columnspan =2)

        self.SaveBtn.grid(column=1, row=8)
        self.CalcBtn.grid(column=3, row=8) 
        self.AdvBtn.grid(column =1 , row = 9)
        
        
    def HideInputs(self):
        self.TunDiaLabel.grid_forget()
        self.TunDiaEntry.grid_forget()

        self.FlowRateLabel.grid_forget()
        self.FlowRateEntry.grid_forget()

       
        self.SaveBtn.grid_forget()
        self.CalcBtn.grid_forget()

        self.TunLeLabel.grid_forget()
        self.TunLeEntry.grid_forget()

        self.AdvBtn.grid_forget()

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
        
        TunLength = self.TunLeEntry.get()
        EXPQTY = self.ExpQTYEntry.get()

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
        
            self.CalcObj.TunDiameter = float(TunDiameter)
            self.CalcObj.FlowRate = float(FlowRate)
            self.CalcObj.Length = length
            self.CalcObj.TunLength = float(TunLength)
            self.CalcObj.ExpQTY = float(EXPQTY)
            return True
        else:
            errorMsg.newMsg(self.master, 'Inputs Must Be Numbers\nOnly Emulsion and ANFO may be 0')
            return False

    def Exit(self):
        if self.Save():
            print('hit')
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
    def changestate(self,event):
        self.ExpQTYEntry.delete(0, END)
        self.ExpQTYEntry.insert(0, (float(self.TunDiaEntry.get())/2)**2*pi*7.5)
    
    def openAdv(self):  
              
            newWindow = Toplevel(self.master)
            newWindow.title("Advanced Settings")
            advset = AdvSettings.Advsettings(newWindow, self.CalcObj)
            newWindow.grab_set()
            newWindow.wait_window()
            newWindow.grab_release()

    def insertdropdown(self,event):
        self.SaveBtn.grid_forget()
        self.CalcBtn.grid_forget()
        self.AdvBtn.grid_forget()
        interNo = self.variable.get()
        print(interNo)
        if interNo == 'Default':
            self.SaveBtn.grid(column=2, row=8) 
            self.CalcBtn.grid(column=3, row=8) 
            self.AdvBtn.grid(column =1 , row = 8)
            return
        if interNo == '1':
            self.DistancesLabel.grid( column=1,row=8,columnspan=2)
            self.Distance1Label.grid(column=1, row=9,columnspan= 2)
            self.Distance1Entry.grid(column=3, row=9)
            if len(self.Distance1Entry.get()) == 0 and len(self.CalcObj.Length) == 1:
                    self.Distance1Entry.insert(0, self.CalcObj.Length[0])

            self.SaveBtn.grid(column=2, row=10) 
            self.CalcBtn.grid(column=3, row=10) 
            self.AdvBtn.grid(column =1 , row = 10)
            
            self.Distance2Label.grid_forget()
            self.Distance3Label.grid_forget()
            self.Distance4Label.grid_forget()
            self.Distance5Label.grid_forget()
            
            self.Distance2Entry.grid_forget()
            self.Distance3Entry.grid_forget()
            self.Distance4Entry.grid_forget()
            self.Distance5Entry.grid_forget()

            
        elif interNo == '2':
            self.DistancesLabel.grid( column=1,row=8,columnspan=2)
            self.Distance1Label.grid(column=1, row=9,columnspan= 2)
            self.Distance1Entry.grid(column=3, row=9)
            if len(self.Distance1Entry.get()) == 0 and len(self.CalcObj.Length) == 2:
                self.Distance1Entry.insert(0, self.CalcObj.Length[0])
            self.Distance2Label.grid(column=1, row=10,columnspan= 2)
            self.Distance2Entry.grid(column=3,row=10)
            if len(self.Distance2Entry.get()) == 0 and len(self.CalcObj.Length) == 2:
                self.Distance2Entry.insert(0, self.CalcObj.Length[1])

            self.SaveBtn.grid(column=2, row=11) 
            self.CalcBtn.grid(column=3, row=11) 
            self.AdvBtn.grid(column =1 , row = 11)
            
            self.Distance3Label.grid_forget()
            self.Distance4Label.grid_forget()
            self.Distance5Label.grid_forget()

            self.Distance3Entry.grid_forget()
            self.Distance4Entry.grid_forget()
            self.Distance5Entry.grid_forget()

            

        elif interNo == '3':
            self.DistancesLabel.grid( column=1,row=8,columnspan=2)
            self.Distance1Label.grid(column=1, row=9,columnspan= 2)
            self.Distance1Entry.grid(column=3, row=9)
            if len(self.Distance1Entry.get()) == 0 and len(self.CalcObj.Length) == 3:
                self.Distance1Entry.insert(0, self.CalcObj.Length[0])
            self.Distance2Label.grid(column=1, row=10,columnspan= 2)
            self.Distance2Entry.grid(column=3,row=10)
            if len(self.Distance2Entry.get()) == 0 and len(self.CalcObj.Length) == 3:
                self.Distance2Entry.insert(0, self.CalcObj.Length[1])
            self.Distance3Label.grid(column=1, row=11,columnspan= 2)
            self.Distance3Entry.grid(column=3,row=11)
            if len(self.Distance3Entry.get()) == 0 and len(self.CalcObj.Length) == 3:
                self.Distance3Entry.insert(0, self.CalcObj.Length[2])

            self.SaveBtn.grid(column=2, row=12) 
            self.CalcBtn.grid(column=3, row=12) 
            self.AdvBtn.grid(column =1 , row = 12)
            
            self.Distance4Label.grid_forget()
            self.Distance5Label.grid_forget()

            self.Distance4Entry.grid_forget()
            self.Distance5Entry.grid_forget()

            
            
        elif interNo == '4':
            self.DistancesLabel.grid( column=1,row=8,columnspan=2)
            self.Distance1Label.grid(column=1, row=9,columnspan= 2)
            self.Distance1Entry.grid(column=3, row=9)
            if len(self.Distance1Entry.get()) == 0 and len(self.CalcObj.Length) == 4:
                self.Distance1Entry.insert(0, self.CalcObj.Length[0])
            self.Distance2Label.grid(column=1, row=10,columnspan= 2)
            self.Distance2Entry.grid(column=3,row=10)
            if len(self.Distance2Entry.get()) == 0 and len(self.CalcObj.Length) == 4:
                self.Distance2Entry.insert(0, self.CalcObj.Length[1])
            self.Distance3Label.grid(column=1, row=11,columnspan= 2)
            self.Distance3Entry.grid(column=3,row=11)
            if len(self.Distance3Entry.get()) == 0 and len(self.CalcObj.Length) == 4:
                self.Distance3Entry.insert(0, self.CalcObj.Length[2])
            self.Distance4Label.grid(column=1, row=12, columnspan=2)
            self.Distance4Entry.grid(column=3,row=12)
            if len(self.Distance4Entry.get()) == 0 and len(self.CalcObj.Length) == 4:
                self.Distance4Entry.insert(0, self.CalcObj.Length[3])
            
            self.SaveBtn.grid(column=2, row=13) 
            self.CalcBtn.grid(column=3, row=13) 
            self.AdvBtn.grid(column =1 , row = 13)

            self.Distance5Label.grid_forget()
            self.Distance5Entry.grid_forget()

            
        elif interNo == '5':
            self.DistancesLabel.grid( column=1,row=8,columnspan=2)
            self.Distance1Label.grid(column=1, row=9,columnspan= 2)
            self.Distance1Entry.grid(column=3, row=9)
            if len(self.Distance1Entry.get()) == 0 and len(self.CalcObj.Length) == 5:
                self.Distance1Entry.insert(0, self.CalcObj.Length[0])
            self.Distance2Label.grid(column=1, row=10,columnspan= 2)
            self.Distance2Entry.grid(column=3,row=10)
            if len(self.Distance2Entry.get()) == 0 and len(self.CalcObj.Length) == 5:
                self.Distance2Entry.insert(0, self.CalcObj.Length[1])
            self.Distance3Label.grid(column=1, row=11,columnspan= 2)
            self.Distance3Entry.grid(column=3,row=11)
            if len(self.Distance3Entry.get()) == 0 and len(self.CalcObj.Length) == 5:
                self.Distance3Entry.insert(0, self.CalcObj.Length[2])
            self.Distance4Label.grid(column=1, row=12, columnspan=2)
            self.Distance4Entry.grid(column=3,row=12)
            if len(self.Distance4Entry.get()) == 0 and len(self.CalcObj.Length) == 5:
                self.Distance4Entry.insert(0, self.CalcObj.Length[3])
            self.Distance5Label.grid(column=1, row=13, columnspan=2)
            self.Distance5Entry.grid(column=3,row=13)
            if len(self.Distance5Entry.get()) == 0 and len(self.CalcObj.Length) == 5:
                self.Distance5Entry.insert(0, self.CalcObj.Length[4])

            self.SaveBtn.grid(column=2, row=14) 
            self.CalcBtn.grid(column=3, row=14) 
            self.AdvBtn.grid(column =1 , row = 14)
        
            
        elif interNo == 'Default':
            self.length = np.arange(500,self.CalcObj.TunLength+1,50)     
        
    

###########################################################################

class VisCalculation(VisEditCalc2):
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
        self.timeslctEntry.insert(0,100)
        
        
    def ShowOutputs(self):
        self.DoCalc(self.CalcObj.dt)
        self.ShowGraphs()
        self.Subtitle.grid(row=2, column= 2)
        self.exportBtn.grid(row=9, column=3)
        self.editBtn.grid(row=9, column=2)
        self.timeslctLabel.grid(row=9, column=4)
        self.timeslctEntry.grid(row=10, column=4)
        self.edittimeBtn.grid(row=10, column=5)
    def HideOutputs(self):
        self.Subtitle.grid_forget()
        self.exportBtn.grid_forget()
        self.editBtn.grid_forget()
        self.subframe.grid_forget()
    def Edittime(self):
         VisEditCalc2.time = float(self.timeslctEntry.get())
         self.DoCalc()
         self.ShowGraphs()
    def EditInput(self):
        self.HideOutputs()
        VisEditCalc2.ShowInputs(self.Parent)

    def DoCalc(self,dt):
        #Prepare Vars
        CrossSection = pi*pow(self.CalcObj.TunDiameter /2 , 2)
        
        Emuls10 = self.CalcObj.ExpQTY * 0.1   # Emulsion (10%)
        Anfo90 = self.CalcObj.ExpQTY * 0.9    # Anfo Explosive (90%)
      
        tve = ((Emuls10 * self.CalcObj.Emul)/1000 )\
            + ((Anfo90 * self.CalcObj.anfo)/1000) #Total Volume Emitted
        print(f"tve {tve}")
        dusttve = 300 *CrossSection * 50 / 1000000
        # Calculate reynolds number
        rho =  1.2
        mu = 1.846*10**-5
        vel = self.CalcObj.FlowRate/CrossSection  
        print(f'vel {vel}')
        R = (rho*vel*self.CalcObj.TunLength)/mu
        print(f"R = {R}")
        f = ffsolver.solvef(self.CalcObj.TunDiameter,R)
        D = 5.05 * self.CalcObj.TunDiameter * vel * sqrt(f/8)
        print(f"D {D}")
        # Create Distance Array (5 to 100m Incrementing by 5)
        self.ZArr = np.asarray(self.CalcObj.Length)    # Distance from site
        print(self.ZArr)
        
        # Create Time Array (10 - 100min, step 10)
        self.TimeArr = np.arange(1,VisEditCalc2.time,dt)    # Time Array
        
        
        # Calculate Dilution Times for CO and NOx
        i = 0 # Time Index
        j = 0 # Volume Index
        self.DiluCONOx = np.zeros((self.ZArr.size,self.TimeArr.size))
        for z in self.ZArr:
            for Time in self.TimeArr:
               
                
                self.DiluCONOx[i,j] = (tve/(2*CrossSection* sqrt(pi*D*Time)))*(exp((-(z-(vel*(Time*60)))**2)/(4*D*Time)))*100000
                
                j = j + 1
            i = i + 1
            j = 0
        
    
        # Calculate Dilution Times for Dust
        i = 0 # Time Index
        j = 0 # Volume Index
        self.DiluDust = np.zeros((self.ZArr.size,self.TimeArr.size))
        for z in self.ZArr:
            for Time in self.TimeArr:
                
                self.DiluDust[i,j] = (dusttve/(2*CrossSection* sqrt(pi*D*Time)))*(exp((-(z-(vel*(Time*60)))**2)/(4*D*Time)))*100000
                j = j + 1
            i = i + 1
            j = 0
        
    

    def ShowGraphs(self):
        # Create Sub Frame
        self.subframe = ttk.Frame(self.frame)
        
        # # Plot
        fig = Figure(figsize=(10, 5), dpi=100)
        fig.suptitle('Dilution Times for '+ self.CalcObj.name)
        fig.supxlabel('Time(min)')
        fig.supylabel('Concentration')

        plot1 = fig.add_subplot(121)
        plot1.grid(visible=True, axis='both', which='major')
        plot1.set_xlim([0,VisEditCalc2.time])
        plot1.set_title('CO and NOx')
        for elem in self.DiluCONOx:
            plot1.plot(self.TimeArr,elem)
        plot1.axhline(y = 30, color = 'grey', linestyle = 'dashed')
        lgdlist = []
        for distance in self.ZArr:
            distance = f"{distance} m"
            lgdlist.append(distance)
        plot1.legend(lgdlist)

        plot2 = fig.add_subplot(122)
        plot2.grid(visible=True, axis='both', which='major')
        plot2.set_xlim([0,VisEditCalc2.time])
        plot2.set_title('Dust')
        for elem in self.DiluDust:
            plot2.plot(self.TimeArr,elem)
        plot2.axhline(y = 1.2, color = 'grey', linestyle = 'dashed')
        plot2.legend(lgdlist)
        
        
        #Add Plot to Sub Frame
        self.canvas = FigureCanvasTkAgg(fig, master=self.subframe)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.subframe)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        
        # Show Sub Frame
        self.subframe.grid(row=4, column=1, columnspan=6, rowspan=3)

    def ExportExcel(self):
        time = self.TimeArr[::100]
        self.DoCalc(0.1)

        # Open File Dialog to Select Save Location
        filename = filedialog.asksaveasfilename(initialdir="=",
                                                 title="Export to Excel Format",
                                                 filetypes= (("comma-separated values",
                                                        "*.csv*"),
                                                       ("all files",
                                                        "*.*")))
        

        # Convert to Excel Format
        exportString = 'Dilution Of CONOx\n'
        o = 0
        # Distance Row
        exportString = exportString + "" + ','
        for k in self.TimeArr:
            exportString = exportString + f'{k}' + ','
        exportString = exportString + '\n'
        # Dilu CONOx
        for i in self.DiluCONOx:
            exportString =  exportString + f'{self.ZArr[o]}'
            
           
            for j in i:
                exportString = exportString +',' + str(j)
            exportString = exportString + '\n'
            o = o +1
            
        
        # Dilu Dust
        exportString = exportString + '\nDilution Of Dust\n'
        o=0
        # Distance Row
        exportString = exportString + "" + ','
        for k in self.TimeArr:
            exportString = exportString + f'{k}' + ','
        exportString = exportString + '\n'

        for i in self.DiluDust:
            exportString = exportString + f'{self.ZArr[o]}' 
            
            for j in i:
                exportString = exportString + ',' + str(j)
            exportString = exportString + '\n'
            o = o +1
        
        # Check if File ends with .csv
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
