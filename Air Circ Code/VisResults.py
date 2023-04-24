from tkinter import *

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

class VisShowResults:

    def __init__(self, master, fig,tablefig ):
            fig =fig
            
            self.master = master
            master.state('zoomed')
            self.doLoop = True
            # Frame
            self.topframe = Frame(self.master, width=800, height=1000)
            self.topframe.pack(expand=True, fill=BOTH) #.grid(row=0,column=0)
            
            
            # InitUI
            self.Showgraphs(fig,tablefig)

            

    def Showgraphs(self,fig,tablefig):
            
            button = Button(self.topframe, text= 'button')
            button.pack(side= 'bottom')
            
            self.frame = Frame(self.topframe,  width=500, height=700)
           
            self.tableframe = Frame(self.topframe,  width=500, height=700)
            

           
           

            #Add Plot to Sub Frame
            self.canvas = FigureCanvasTkAgg(fig, master=self.frame)
            self.tablescanvas = FigureCanvasTkAgg(tablefig, master= self.tableframe)
            
            #self.canvas.draw()
            
         
           
            
            self.toolbar = NavigationToolbar2Tk(self.tablescanvas, self.tableframe)
            self.toolbar.update()
            self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
            
            
            self.tablescanvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=TRUE)
           
           
            
            self.tableframe.pack( fill=BOTH) #.grid(row=0,column=0)
            
