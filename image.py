from tkinter import *

root = Tk()
o = image.open('images/O.gif')
x = image.open('images/X.gif')
Label(root, image=x).pack()
Label(root, image=o).pack()
mainloop()
