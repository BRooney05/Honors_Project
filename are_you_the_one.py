import pygame as pg
from sys import exit
from settings import screen_width, screen_height, width_center, height_center, screen_center
from setup import screen, mouse_pos, tick
import Graphics.graphics as gfx

class Text(pg.sprite.Sprite):
    def __init__(self, font, font_size, text, antialias_bool, color, center_tuple, flashing = False, bouncing = False, clicked_function = None):
        super().__init__()

        self.flashing = flashing
        self.bouncing = bouncing

        self.font = pg.font.Font(font, font_size)
        self.image = self.font.render(text, antialias_bool, color)
        self.rect = self.image.get_rect(center = center_tuple)
        self.clicked_function = clicked_function

        if flashing:
            self.flash_index = 0
            self.images = [self.image, pg.Surface(self.rect.size)]

        if bouncing:
            self.increasing = True
            self.speed = -4
        

    def flash(self):
            self.flash_index += 0.05
            if int(self.flash_index) >= len(self.images):
                self.flash_index = 0
            self.image = self.images[int(self.flash_index)]

    def bounce(self):
        self.rect.y += self.speed
        if self.increasing:
            self.speed += 1
        else:
            self.speed -= 1
        if self.speed == 4:
            self.increasing = False
        elif self.speed == -4:
            self.increasing = True

    def update(self):
        if self.flashing:
            self.flash()
        if self.bouncing:
            self.bounce()
        
    def clicked(self):
        if self.clicked_function:
            self.clicked_function()

    def get_rect(self):
        return self.rect


class Person(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()


# class Background(pg.sprite.Sprite):
#     def __init__(self):
#         super().__init__()


def title_screen():

    text_boxes = pg.sprite.Group()
    text_boxes.add(Text('Fonts/Easter Season.otf', 400, 'PLAY', True, 'Pink', screen_center, bouncing = True, clicked_function = play_game))
    text_boxes.add(Text('Fonts/Easter Season.otf', 75, 'SETTINGS', True, 'Pink', (screen_width//25, screen_height//50), clicked_function = open_settings))

    while True:

        for event in pg.event.get():
            # Stop game loop if user quits
            if event.type == pg.QUIT: 
                # Stop all code
                pg.quit()
                exit()

            if event.type == pg.MOUSEBUTTONUP:
                for text_box in text_boxes:
                    if text_box.get_rect().collidepoint(pg.mouse.get_pos()):
                        text_box.clicked()

        screen.blit(gfx.title_bg, (0, 0))
        text_boxes.draw(screen)
        text_boxes.update()

        tick()

def play_game():

    while True:
        
        for event in pg.event.get():
            # Stop game loop if user quits
            if event.type == pg.QUIT: 
                # Stop all code
                pg.quit()
                exit()

            if event.type == pg.MOUSEBUTTONUP:
                introductions()

        screen.blit(gfx.gs1_bg, (0, 0))

        tick()

def introductions():
    pass

def open_settings():
    while True:
        
        text_boxes = pg.sprite.Group()
        text_boxes.add(Text('Fonts/Easter Season.otf', 50, 'hi', True, 'white', screen_center))

        for event in pg.event.get():
            if event.type == pg.QUIT: 
                # Stop all code
                pg.quit()
                exit()

            if event.type == pg.MOUSEBUTTONUP:
                for text_box in text_boxes:
                    if text_box.get_rect().collidepoint(pg.mouse.get_pos()):
                        text_box.clicked()

        screen.blit(gfx.boat_png, screen_center)
        
        tick()

pg.init()

title_screen()