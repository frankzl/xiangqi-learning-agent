from tkinter import *
from PIL import ImageTk, Image
import os
import board as b

piece_shape=50

def click(board, event):
    pos_x = (event.x-piece_shape//2)//piece_shape
    pos_y = (event.y-piece_shape//2)//piece_shape

    print(pos_x,pos_y)

    new_img = board.click_field( pos_x,pos_y )
    if new_img:
        print("drawing")
        img2 = ImageTk.PhotoImage(new_img)
        panel.configure(image=img2)
        panel.image = img2





if __name__ == "__main__":
    root = Tk()
    board = b.Board(piece_shape=50)
    w,h = board.size
    root.geometry(f"{w}x{h}")
    img = ImageTk.PhotoImage(board.get_image())
    
    panel = Label(root, image=img)
    panel.bind("<Button-1>", lambda event: click(board, event))
    
    panel.pack(side = "bottom", fill = "both", expand = "yes")
    root.mainloop()
