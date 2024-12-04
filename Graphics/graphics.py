import pygame as pg
from settings import screen_width, screen_height

icon = pg.image.load('Graphics/pg_icon.png')

title_bg = pg.image.load('Graphics/island_bg.jpg')
title_bg = pg.transform.scale(title_bg, (screen_width, screen_height))

gs1_bg = pg.image.load('Graphics/enterance_dock.jpg')
gs1_bg = pg.transform.scale(gs1_bg, (screen_width, screen_height))

tb_bg = pg.image.load('Graphics/tb_bg.jpg')
tb_bg = pg.transform.scale(tb_bg, (screen_width, screen_height))

boat_png = pg.image.load('Graphics/boat.png')
boat_png = pg.transform.scale(boat_png, (int(screen_width/4), int(screen_height/4)))

man1_png = pg.image.load('Graphics/man1_updated.png')
man2_png = pg.image.load('Graphics/man2_updated.png')
man3_png = pg.image.load('Graphics/man3_updated.png')
man4_png = pg.image.load('Graphics/man4_updated.png')
man5_png = pg.image.load('Graphics/man5_updated.png')
pg_png = pg.image.load('Graphics/placeholder_guy_updated.png')

woman1_png = pg.image.load('Graphics/woman1_updated.png')
woman2_png = pg.image.load('Graphics/woman2_updated.png')
woman3_png = pg.image.load('Graphics/woman3_updated.png')
woman4_png = pg.image.load('Graphics/woman4_updated.png')
woman5_png = pg.image.load('Graphics/woman5_updated.png')
woman6_png = pg.image.load('Graphics/woman6_updated.png')

