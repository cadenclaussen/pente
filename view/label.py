from tkinter import *
from PIL import Image as PilImage
from PIL import ImageTk

def main():
    root = Tk()
    root.title("Pente")
    root.geometry("300x300")


    corner1 = PilImage.open('images/corner.gif')
    corner2 = corner1.transpose(PilImage.ROTATE_90)
    corner3 = corner1.transpose(PilImage.ROTATE_180)
    corner4 = corner1.transpose(PilImage.ROTATE_270)

    corner1a = ImageTk.PhotoImage(corner1)
    corner2a = ImageTk.PhotoImage(corner2)
    corner3a = ImageTk.PhotoImage(corner3)
    corner4a = ImageTk.PhotoImage(corner4)

    Label(root, image=corner1a).pack()
    Label(root, image=corner2a).pack()
    Label(root, image=corner3a).pack()
    Label(root, image=corner4a).pack()

    root.mainloop()


main()
