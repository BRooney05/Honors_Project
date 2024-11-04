import pygame as pg
from settings import screen_width, screen_height

icon = pg.image.load('Graphics/pg_icon.png')

title_bg = pg.image.load('Graphics/island_bg.jpg')
title_bg = pg.transform.scale(title_bg, (screen_width, screen_height))


gs1_bg = pg.image.load('Graphics/enterance_dock.jpg')
gs1_bg = pg.transform.scale(gs1_bg, (screen_width, screen_height))

boat_png = pg.image.load('Graphics/boat.png')
boat_png = pg.transform.scale(boat_png, (int(screen_width/4), int(screen_height/4)))

man1_png = pg.image.load('Graphics/man1_updated.png')

woman1_png = pg.image.load('Graphics/woman1_updated.png')

pg_png = pg.image.load('Graphics/placeholder_guy_updated.png')
