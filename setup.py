import pygame as pg
import Graphics.graphics as gfx
from settings import screen_width, screen_height, fps
from sys import exit

clock = pg.time.Clock()

pairs = [("Mark", "GUY #5"), ("Stacy", "GUY #6"), ("GUY #1", "GUY #7"), ("GUY #2", "GUY #8"), ("GUY #3", "GUY #9"), ("GUY #4", "GUY #10")]

screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption('Are You The One?')
pg.display.set_icon(gfx.icon)

def tick():
    # Update frames
    pg.display.update()
    # Limit FPS
    clock.tick(fps)
