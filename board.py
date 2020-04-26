import matplotlib.pyplot as plt
from skimage.transform import resize
import pandas as pd
import numpy as np
import os
from PIL import Image, ImageDraw


starting_position = np.array(
    [
        "rheakaehr",
        "         ",
        " c     c ",
        "p p p p p",
        "         ",
        "         ",
        "P P P P P",
        " C     C ",
        "         ",
        "RHEAKAEHR"
    ])
def get_pieces(piece_shape=100):
    pieces = "AaCcEeHhKkPpRr"
    piece_imgs = dict()
    for piece in pieces:
        piece_imgs[piece] = ( Image.open(f"dataset/assets/{piece}.png")).resize((piece_shape, piece_shape))
        #piece_imgs[piece] = (piece_imgs[piece] * 255).astype(int)
    return piece_imgs

def get_board( piece_shape=100 ):
    half_board = np.zeros( (int(5.5*piece_shape),10*piece_shape,4), dtype=int )
    half_board[:,:,0] = 206
    half_board[:,:,1] = 92
    half_board[:,:,2] = 0
    half_board[:,:,3] = 255
    
    for x in range(1,9):
        for y in range(1,5):
            start_x,start_y = piece_shape*x,piece_shape*y
            end_x,  end_y   = piece_shape*(x+1) - 4, piece_shape*(y+1) - 4
            half_board[start_y:end_y,start_x:end_x] = np.array([252, 175, 62, 255])
        
    for x in range(1,10):
        start_x
            
    return Image.fromarray(np.concatenate( (half_board, half_board[::-1,:,:])).astype(np.uint8))


def place_pieces( occupancy_grid, piece_shape, pieces, board ):
    board_cpy = board.copy()
    for y,row in enumerate(occupancy_grid):
        for x,field in enumerate(row):
            if field in pieces:
                pos_x = piece_shape*(x + 1) - piece_shape//2
                pos_y = piece_shape*(y + 1) - piece_shape//2
                piece = pieces[field]
                board_cpy.paste(piece, (pos_x,pos_y), piece)
    return board_cpy

class Board:
    def __init__(self, starting_state=None, piece_shape = 100):
        self.states = []
        if starting_state:
            self.states.append(starting_state)
        else:
            self.states.append(starting_position)

        self.images = []
        self.board = get_board(piece_shape = piece_shape)
        self.size = self.board.size
        self.piece_shape = piece_shape
        self.pieces = get_pieces(piece_shape=piece_shape)
        self.images.append(place_pieces( self.states[0], piece_shape, self.pieces, self.board))
        self.pointer = 0


    def get_image(self):
        return self.images[self.pointer]

    def click_field(self, pos_x, pos_y):
        if self.states[self.pointer][pos_y][pos_x] != " ":
            current_img = self.images[self.pointer].copy()
            draw = ImageDraw.Draw(current_img)
            print("drawing circle at")
            print(self.get_image_position(pos_x, pos_y))
            draw.ellipse(self.get_image_position(pos_x, pos_y), outline ='blue')
            return current_img
        return None

    def get_image_position( self, board_x, board_y ):
        x = board_x * self.piece_shape + self.piece_shape//2
        y = board_y * self.piece_shape + self.piece_shape//2
        return x,y,x+self.piece_shape, y+self.piece_shape
