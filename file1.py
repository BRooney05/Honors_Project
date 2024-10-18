import pygame as pg
from sys import exit

# Starts pygame
pg.init()

# Initialize clock to limit FPS
clock = pg.time.Clock()

# Set screen size, caption, and icon
screen = pg.display.set_mode((1500, 1000))
pg.display.set_caption('Are You The One?')
icon = pg.image.load('pg_icon.png')
pg.display.set_icon(icon)

# Create blue box
color = pg.Surface((1200, 800))
color.fill('blue')

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
            
    # Place color on screen
    screen.blit(color, (300, 200))    
    
    # Update frames
    pg.display.update()
    # Limit FPS
    clock.tick(30)
