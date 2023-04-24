from datetime import datetime
import os
from pathlib import Path
import numpy as np
class AirCircCalc:

    def __init__(self, name, calctype):
        self.name = name    # Name of Calculation
        self.calculation= calctype # Calculation type
        self.dt_string = datetime.now().strftime("%d/%m/%Y %H:%M")    # Time of Creation
        #self.varList = varList # List of Calculation Vars
        #List of Vars
        self.IsOpen = False
        
        self.TunDiameter = 0
        self.FlowRate = 0
        self.anfo = 40
        self.Emul = 40
        self.Dust50m = 300
        self.STWA = 1.2   #Time weighted average
        self.TunLength = 0
        self.ExpQTY = 0
        self.COTWA = 30
        self.Length = np.zeros(5)
        self.Efficiency = 70
        self.DistInt = 'Default'
        self.dt = 0.01

    def __str__(self):
        return f"{self.name} ({self.dt_string})"

    def saveFile(CalcList):
        #Saves Calculation File
        saveString = ""
        for i in CalcList:
            saveString = saveString + i.name\
                  + '\t' + str(i.calculation)\
                  + '\t' + i.dt_string\
                  + '\t' + str(i.TunDiameter)\
                  + '\t' + str(i.FlowRate)\
                  + '\t' + str(i.anfo)\
                  + '\t' + str(i.Emul)\
                  + '\t' + str(i.Dust50m)\
                  + '\t' + str(i.STWA)\
                  + '\t' + str(i.TunLength)\
                  + '\t' + str(i.ExpQTY)\
                  + '\t' + str(i.COTWA)\
                  + '\t' + str(i.Length)\
                  + '\t' + str(i.Efficiency)\
                  + '\t' + str(i.DistInt)\
                  + '\t' + str(i.dt)\
                  + '\tend'  + '\n'
            print('done')
            
        filename = Path(os.path.join(os.path.expanduser('~'),'Documents','GrydaleAirCirculation.txt'))
        filename.touch(exist_ok=True)
        file = open(filename, 'w')
        file.write(saveString)
        file.close


        pass

    def loadFile(CalcList):
        #Load Calculation File
        filename = Path(os.path.join(os.path.expanduser('~'),'Documents','GrydaleAirCirculation.txt'))
        filename.touch(exist_ok=True)
        file = open(filename, 'r+')
        readData = file.readlines()
        file.close
        
        # Process String
        for i in readData:
            # Split into Tabs 
            varsData = i.split('\t')
            if len(varsData) == 17:
                # New Calc Class
                newClass = AirCircCalc(varsData[0],varsData[1])
                # Load data
                newClass.calculation = str(varsData[1])
                newClass.dt_string = varsData[2]
                newClass.TunDiameter = float(varsData[3])
                newClass.FlowRate = float(varsData[4])
                newClass.anfo = float(varsData[5])
                newClass.Emul = float(varsData[6])
                newClass.Dust50m = float(varsData[7])
                newClass.STWA = float(varsData[8])
                newClass.TunLength = float(varsData[9])
                newClass.ExpQTY = float(varsData[10])
                newClass.COTWA = float(varsData[11])
                newClass.Length = varsData[12].strip("[")
                newClass.Length = newClass.Length.strip("]")
                newClass.Length = np.asarray(newClass.Length.split(','))
                newClass.Efficiency = float(varsData[13])
                newClass.DistInt = str(varsData[14])
                newClass.dt = float(varsData[15])
                CalcList.append(newClass)
                
        
         
    def exportFile(self):
        #Export Calculation Data to Excel
        pass