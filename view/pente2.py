from tkinter import *
from images import *


def main():
    root = Tk()
    root.title("Pente")
    root.geometry("700x700")

    # Just a visual to demonstrate all the images
    images = getImages()
    row = 0
    column = 0
    for key in images:
        Label(root, image=images[key], width=27, height=27).grid(row=row, column=column, padx=10, pady=10)
        column += 1
        if (column == 12):
            row += 1
            column = 0



    # Usage example, let's say you want the image at row 0, column 0
    row += 1
    column = 0
    Label(root, text="Image at 0, 0").grid(row=row, column=column)

    row += 1
    image = getImage(0, 0)
    Label(root, image=image, width=27, height=27).grid(row=row, column=column, padx=0, pady=0)


    # Usage example, let's say you want the blue bead image at row 0, column 0
    row += 1
    column = 0
    Label(root, text="Blue and Red bead images at 0, 0").grid(row=row, column=column)

    row += 1
    blueImage = getBeadImage(0, 0, 0) # last parameter 0 indicates blue
    Label(root, image=blueImage, width=27, height=27).grid(row=row, column=column, padx=0, pady=0)

    row += 1
    redImage = getBeadImage(0, 0, 1)  # last parameter 1 indicates red
    Label(root, image=redImage, width=27, height=27).grid(row=row, column=column, padx=0, pady=0)



    # Usage example, let's say you want the image at row 9, column 9 (CENTER)
    row += 1
    column = 0
    Label(root, text="Image at 9, 9").grid(row=row, column=column)

    row += 1
    image = getImage(9, 9)
    Label(root, image=image, width=27, height=27).grid(row=row, column=column, padx=0, pady=0)



    # Usage example, let's say you want the blue bead image at row 0, column 0
    row += 1
    column = 0
    Label(root, text="Blue and Red bead images at 9, 9").grid(row=row, column=column)

    row += 1
    blueImage = getBeadImage(9, 9, 0) # last parameter 0 indicates blue
    Label(root, image=blueImage, width=27, height=27).grid(row=row, column=column, padx=0, pady=0)

    row += 1
    redImage = getBeadImage(9, 9, 1)  # last parameter 1 indicates red
    Label(root, image=redImage, width=27, height=27).grid(row=row, column=column, padx=0, pady=0)



    root.mainloop()



main()
