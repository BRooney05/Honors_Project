import pygame as pg
import Graphics.graphics as gfx
from GameScreens import *
from settings import screen_width, screen_height
from setup import screen, mouse_pos, tick
from sys import exit

pg.init()
# init_screen()
# Starts pygame

title_font = pg.font.Font('Fonts/Easter Season.otf', 300)
hovered_title_font = pg.font.Font('Fonts/Easter Season.otf', 400)

text_surf = title_font.render('Play!', True, 'pink')
text_rect = text_surf.get_rect(center = (screen_width/2, screen_height/2))

hovered_text_surf = hovered_title_font.render('Play!', True, 'pink')
hovered_text_rect = hovered_text_surf.get_rect(center = (screen_width/2, screen_height/2))

# Loops through frames endlessly until conditions are met to quit game
while True:
    # Draw all elements
    # Update everything

    for event in pg.event.get():

        # Stop game loop if user quits
        if event.type == pg.QUIT: 
            pg.quit()
            # Stop all code
            exit()

        if event.type == pg.MOUSEMOTION:
            mouse_pos = event.pos

    screen.blit(gfx.title_bg, (0, 0))

    if hovered_text_rect.collidepoint(mouse_pos) or text_rect.collidepoint(mouse_pos):
        screen.blit(hovered_text_surf, hovered_text_rect)
        if any(pg.mouse.get_pressed()):
            print('clicked!')
    else:
        screen.blit(text_surf, text_rect)

    tick()
