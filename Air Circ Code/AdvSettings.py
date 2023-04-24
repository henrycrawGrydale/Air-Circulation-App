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

class Advsettings:
        def __init__(self, master, CalcObj: calcClass.AirCircCalc):
            
            self.CalcObj = CalcObj
            self.master = master
            print(self.master)
            self.doLoop = True
            # Frame
            self.frame = ttk.Frame(self.master, padding=10)
            self.frame.grid(columnspan=3)
            self.FrameTitleLabel = ttk.Label(self.frame, text = 'Default Settings', justify='center').grid(column=1, row=1, columnspan=3)
            # InitUI
            print(self)
            self.InitUI()
            self.ShowInputs()
            
        def InitUI(self):
            # anfo
            self.anfoLabel = ttk.Label(self.frame, text = 'anfo (L/Kg)')
            self.anfoEntry = ttk.Entry(self.frame)
        
            if self.CalcObj.anfo == 0:
                self.anfoEntry.insert(0, float(40))
            else:
                self.anfoEntry.insert(0, self.CalcObj.anfo)
            # Emulsion
            self.EmulLabel = ttk.Label(self.frame, text = 'Emulsion (L/Kg)')
            self.EmulEntry = ttk.Entry(self.frame)
            
            if self.CalcObj.Emul == 0:
                self.EmulEntry.insert(0, float(40))
            else:
                self.EmulEntry.insert(0, self.CalcObj.Emul)
            # Conc. Dust 50m
            self.Dust50mLabel = ttk.Label(self.frame, text = 'Concentration of Dust per 50m (mg/m³)')
            self.Dust50mEntry = ttk.Entry(self.frame)
            
            if self.CalcObj.Dust50m == 0:
                self.Dust50mEntry.insert(0, float(300))
            else:
                self.Dust50mEntry.insert(0, self.CalcObj.Dust50m)

            # Safe Time Weighted Average
            self.STWALabel = ttk.Label(self.frame, text = 'Safe Time Weighted Ave (mg/m³)')
            self.STWAEntry = ttk.Entry(self.frame)
            if self.CalcObj.STWA == 0:
                self.STWAEntry.insert(0, float(1.2))
            else:
                self.STWAEntry.insert(0, self.CalcObj.STWA)
        
            self.COTWALabel = ttk.Label(self.frame, text = 'Safe Time Weighted Ave (ppm)')
            self.COTWAEntry = ttk.Entry(self.frame)
            self.COTWAEntry.insert(0, self.CalcObj.COTWA)

            #Clearing Efficiency

            self.EfficiencyLabel = ttk.Label(self.frame, text = 'Efficiency of particle collection (%)')
            self.EfficiencyEntry = ttk.Entry(self.frame)
            self.EfficiencyEntry.insert(0, self.CalcObj.Efficiency)

            # Graph Resoltution
            self.dtLabel = ttk.Label(self.frame, text = 'Graph Resolution')
            self.dtEntry = ttk.Entry(self.frame)
            self.dtEntry.insert(0,self.CalcObj.dt)
            # Save and Exit
            self.AcceptBtn = ttk.Button(self.frame, text='Save & Exit',command= self.Exit)
            self.master.bind('<Escape>', self.Extfunc)  

           
            
        def Exit(self):
           
            if self.Save():
                print('hit')
                self.doLoop = False
                self.CloseWin()      
           
            
        
        def ShowInputs(self):
            self.anfoLabel.grid(column=1, row=3, columnspan=2)
            self.anfoEntry.grid(column=3 , row=3)

            self.EmulLabel.grid(column=1, row=4, columnspan=2)
            self.EmulEntry.grid(column=3 , row=4)
            
            self.Dust50mLabel.grid(column=1, row=5, columnspan=2)
            self.Dust50mEntry.grid(column=3 , row=5)

            self.STWALabel.grid(column=1, row=6, columnspan=2)
            self.STWAEntry.grid(column=3 , row=6)
            
            self.COTWALabel.grid(column = 1, row=7, columnspan=2)
            self.COTWAEntry.grid(column = 3, row =7, columnspan =2)

            self.EfficiencyLabel.grid(column=1, row=8, columnspan=2)
            self.EfficiencyEntry.grid(column=3, row=8)

            self.dtLabel.grid(column=1, row=9, columnspan =2)
            self.dtEntry.grid(column= 3, row =9 )
            
            self.AcceptBtn.grid(column=2, row=10)
           
        def Extfunc(self,event):
                self.Exit()
        

        def Save(self, isCalc = False):
            
            # Get Vars from Inputs
            
            anfo = self.anfoEntry.get()
            Emul = self.EmulEntry.get()
            Dust50m = self.Dust50mEntry.get()
            STWA = self.STWAEntry.get()
            COTWA = self.COTWAEntry.get()
            Efficiency = self.EfficiencyEntry.get()
            dt = self.dtEntry.get()

            
            #Check Inputs
            if  self.is_number(anfo)\
                    and self.is_number(Emul)\
                        and  self.is_number(Dust50m, isCalc)\
                             and self.is_number(STWA, isCalc)\
                                 and self.is_number(dt, isCalc):
                # Save Inputs
                
                self.CalcObj.anfo = float(anfo)
                self.CalcObj.Emul = float(Emul)
                self.CalcObj.Dust50m = float(Dust50m)
                self.CalcObj.STWA = float(STWA)
                self.CalcObj.COTWA = float(COTWA)
                self.CalcObj.Efficiency = float(Efficiency)
                self.CalcObj.dt = float(dt)
                return True
            else:
                errorMsg.newMsg(self.master, 'Inputs Must Be Numbers\nOnly Emulsion and ANFO may be 0')
                return False
            
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
        