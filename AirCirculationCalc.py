from tkinter import *
import AirCirculationUI
import CalculationClass as CalcClass
import os
def main():


    #Setup GUI
    root = Tk()
    root.iconbitmap("Icon.ico")
    root.title('Air Circulation Calculator')
    app = AirCirculationUI.VisMain(root)
    root.state('zoomed')
    root.mainloop()

    print('GUI Ended')

    # Save Files
    CalcClass.AirCircCalc.saveFile(app.CalcList)
    print("saved")
    pass




main()