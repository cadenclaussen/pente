from tkinter import *
from images import *

root = Tk()
root.title('Pente')
root.geometry('590x775+20+20')
root.resizable(False, False)
boardFrame = Frame(root)
boardFrame.pack()

offset = 0
for y in range(19):
    for x in range(19):
        label = Label(boardFrame, image=getOpenImage(x, y), borderwidth=0)
        label.grid(row=(y + offset), column=x, padx=0, pady=0)

# offset += 19
# for y in range(19):
#     for x in range(19):
#         label = Label(boardFrame, image=getOpenImageOffense(x, y), borderwidth=0)
#         label.grid(row=(y + offset), column=x, padx=0, pady=0)

# offset += 19
# for y in range(19):
#     for x in range(19):
#         label = Label(boardFrame, image=getOpenImageDefense(x, y), borderwidth=0)
#         label.grid(row=(y + offset), column=x, padx=0, pady=0)

# for color in [ 'Blue', 'Red', 'Green' ]:
#     offset += 19
#     for y in range(19):
#         for x in range(19):
#             label = Label(boardFrame, image=getBeadImage(x, y, color), borderwidth=0)
#             label.grid(row=(y + offset), column=x, padx=0, pady=0)

# for color in [ 'Blue', 'Red', 'Green' ]:
#     offset += 19
#     for y in range(19):
#         for x in range(19):
#             label = Label(boardFrame, image=getHighlightedBeadImage(x, y, color), borderwidth=0)
#             label.grid(row=(y + offset), column=x, padx=0, pady=0)


root.mainloop()
