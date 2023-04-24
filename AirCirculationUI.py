from tkinter import *
from tkinter import ttk
import VisNewCalc as VisNC
import CalculationClass as CalcClass
import confirmChoice as delCal
import VisEditCalc as VisEC
import VisEditCalc2 as VisEC2
import errorMsg
from PIL import ImageTk,Image  
import preview as prev
import AdvSettings

class VisMain:
    

    def __init__(self, master):
        self.master = master
        self.version = '1.1'
        self.CalcList = []
        CalcClass.AirCircCalc.loadFile(self.CalcList)
        
        

        # Create Vis
        self.frame = ttk.Frame(self.master, padding=10)
        self.frame.grid(columnspan=1)
        self.FrameTitleLabel = ttk.Label(self.frame, text = 'Air Circulation\nCalculator', justify='center', font=("Helvetica", "14", "bold")).grid(column=2, row=0, columnspan=2)

        # Add Logo
        self.LogoCanvas = Canvas(self.frame, width=100, height=50)
        self.LogoCanvas.grid(row=0, column=0, columnspan=2)
        self.Logo = ImageTk.PhotoImage(Image.open("GrydaleLogo.png").resize((100,50),Image.ANTIALIAS))
        self.LogoCanvas.create_image(50,25, image=self.Logo)
        

        # --Calcs Selection Frame--
        self.calcSelFrame = ttk.Frame(self.frame)
        self.calcSelFrame.grid(row=1, column=0, rowspan=2, columnspan=5)

        # Existing Calcs Listbox
        self.CalcTree = ttk.Treeview(self.calcSelFrame, columns=('Calculation','Date', 'Time'))
        self.CalcTree.pack(side="left", fill="y")

        self.CalcTree.heading('#0', text = 'Name')
        self.CalcTree.heading('#1', text = 'Calculation')
        self.CalcTree.heading('#2', text = 'Date Created')
        self.CalcTree.heading('#3', text = 'Time Created')
        self.CalcTree.column('#0', width=100)
        self.CalcTree.column('#1', width=100)
        self.CalcTree.column('#2', width=80)
        self.CalcTree.column('#3', width=80)
        
        #On Click
        self.CalcTree.bind('<ButtonRelease-1>', self.OnClick)
        #On double-click
        self.CalcTree.pack()
        self.CalcTree.bind("<Double-1>", self.OnDoubleClick)
        
        # Preview Frame
        
        self.prevframe = ttk.Frame(master)
        self.prevframe.grid( row = 0, column = 9, rowspan = 1, columnspan = 5)

        
        self.PreviewCanvas = Canvas(self.prevframe, width=800, height=600, bg = 'white')
        self.PreviewCanvas.config(scrollregion=(0,0,700,700))
      
       

        self.hbar=ttk.Scrollbar(master,orient=HORIZONTAL)
        self.hbar.config(command=self.PreviewCanvas.xview)
        self.hbar.grid(row = 1, column = 9, rowspan = 1, columnspan = 5)
        
        self.vbar=ttk.Scrollbar(self.prevframe,orient=VERTICAL)
        self.vbar.config(command=self.PreviewCanvas.yview)
        self.vbar.pack(side="right", fill="y")
        
        self.PreviewCanvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.hbar.set)
        self.PreviewCanvas.pack(side="left", fill="both")

        # Existing Calcs Scroll Bar
        self.CalcTreeScroll = ttk.Scrollbar(self.calcSelFrame, command = self.CalcTree.yview)
        self.CalcTreeScroll.pack(side="right", fill="y")
        self.CalcTree.configure(yscrollcommand=self.CalcTreeScroll.set)


        # --Func Buttons--
        # New Calc
        self.AcceptBtn = ttk.Button(self.frame, text='New Calculation',command=self.newCalc)
        self.AcceptBtn.grid(column=3, row=3, columnspan=3) 

        # Delete Calc
        self.delBtn = ttk.Button(self.frame, text = 'Delete Calc' , command = self.delCalc)
        self.delBtn.grid(column= 0, row= 3)
        self.master.bind('<Delete>', self.delCalc) 

        # Open Calc
        self.openBtn = ttk.Button(self.frame, text = 'Open Calc' , command = self.openCalc)
        self.openBtn.grid(column= 2, row= 3)

        # Display Version Number
        self.vers = ttk.Label(self.frame, text='Ver. '+ self.version, foreground='grey70')
        self.vers.grid(row=4, column=3)

        # Exit
        self.master.bind('<Escape>', self.Extfunc) 

        self.updateTreeview()

        

    def newCalc(self):
        # Prompt User To Name new Calculation
        newWindow = Toplevel(self.master)
        newWindow.title('Create New Calc')
        newcalc = VisNC.VisNewCalc(newWindow)
        newWindow.grab_set()
        newWindow.wait_window()
        newWindow.grab_release()

        # Create New Calc and add to List
        if newcalc.success:
            self.CalcList.append(CalcClass.AirCircCalc(newcalc.name,newcalc.calctype))
        
        # Update Treeview 
        self.updateTreeview()
    
    def openCalc(self):
        # Get User to Confirm
        Treeiid = self.CalcTree.focus()
        if Treeiid == '':
            errorMsg.newMsg(self.master,'Please Select Calculation')
            return
        
        index = self.CalcTree.index(Treeiid)
        
        newWindow = Toplevel(self.master)
        newWindow.title('Editing: '+ self.CalcList[index].name)
        print(self.CalcList[index].name)
        print(self.CalcList[index].calculation)
        if self.CalcList[index].calculation == "Axial only ventilation times":
            editCalc = VisEC2.VisEditCalc2(newWindow, self.CalcList[index])
        elif self.CalcList[index].calculation == "Combined ventilation (JMS machines)":
            editCalc = VisEC.VisEditCalc(newWindow, self.CalcList[index])
        newWindow.grab_set()
        newWindow.wait_window()
        newWindow.grab_release()


    def delCalc(self):
        # Get User to Confirm
        newWindow = Toplevel(self.master)
        newWindow.title('Confirm Choice')

        Treeiid = self.CalcTree.focus()
        if Treeiid == '':
            errorMsg.newMsg(self.master, 'Please Select Calculation')
            return
        index = self.CalcTree.index(Treeiid)

        confirmWin = delCal.VisConfirmInput(newWindow, 'Confirm Delete:\n'+self.CalcList[index].name+'?')
        newWindow.grab_set()
        newWindow.wait_window()
        newWindow.grab_release()
        if confirmWin.confirm:
            # delete
            self.CalcList.pop(index)
            self.updateTreeview()

    def updateTreeview(self):
        # Clear Tree
        for i in self.CalcTree.get_children():
            self.CalcTree.delete(i)
    
        # Populate Tree
        j = 0
        for i in self.CalcList:
            self.CalcTree.insert('', j, values=(f"{i.calculation}", i.dt_string[0:10],i.dt_string[11:16],), text = i.name)
            j = j+1

    def OnDoubleClick(self,event): 
        
        self.openCalc()
    def OnClick(self,event):
        #prev.Preview.addimage(self)
        return
    def Extfunc(self, event):
        self.master.quit()
        self.master.destroy()
    
    
    
    
 
    

    
  