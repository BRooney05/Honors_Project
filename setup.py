import pygame as pg
import Graphics.graphics as gfx
from settings import screen_width, screen_height, fps
from sys import exit

clock = pg.time.Clock()
mouse_pos = (0,0)

screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption('Are You The One?')
pg.display.set_icon(gfx.icon)

# for graphic in gfx.converted_graphics:
#     graphic = graphic.convert_alpha()
##################################################

def tick():
    # Update frames
    pg.display.update()
    # Limit FPS
    clock.tick(fps)
