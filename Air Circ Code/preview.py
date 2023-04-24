from tkinter import *
from tkinter import ttk
from PIL import ImageTk,Image  

class Preview:

    def addimage(self):

    # Add preview image
        
        self.Preview = ImageTk.PhotoImage(Image.open("combined.png").resize((500,300),Image.ANTIALIAS))
        self.PreviewCanvas.create_image(500,50, image=self.Preview)