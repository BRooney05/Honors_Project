import pygame as pg
from sys import exit
from settings import screen_width, screen_height, width_center, height_center, screen_center, num_characters
from setup import screen, pairs, tick
import Graphics.graphics as gfx

class Text(pg.sprite.Sprite):
    def __init__(self, font, font_size, text, antialias_bool, color, location_tuple, location = 'center', flashing = False, bouncing = False, clicked_function = None, filled = False):
        super().__init__()

        self.flashing = flashing
        self.bouncing = bouncing
        self.filled = filled

        self.font = pg.font.Font(font, font_size)
        self.image = self.font.render(text, antialias_bool, color)
        if location == 'midleft':
            self.rect = self.image.get_rect(midleft = location_tuple)
        if location == 'topleft':
            self.rect = self.image.get_rect(topleft = location_tuple)
        else:
            self.rect = self.image.get_rect(center = location_tuple)
        self.clicked_function = clicked_function

        if flashing:
            self.flash_index = 0
            self.images = [self.image, pg.Surface((0, 0))]

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

    def fill(self):
        pg.draw.rect(screen, 'white', self.rect)

    def update(self):
        if self.flashing:
            self.flash()
        if self.bouncing:
            self.bounce()
        if self.filled:
            self.fill()
        
    def clicked(self, guessed_pairs_param = None, week_param = None, person1_param = None, person2_param = None):
        if self.clicked_function:
            if self.clicked_function == pick_screen_w_input:
                guessed_pairs_param.append([person1_param, person2_param])
                self.clicked_function(week_param, guessed_pairs = guessed_pairs_param)
            elif person1_param:
                self.clicked_function(week_param, person1_param, person2_param)
            else:
                self.clicked_function()

    def get_rect(self):
        return self.rect

class Person(pg.sprite.Sprite):
    def __init__(self, image, name, location_tuple, intro_speech = None, scalar = 1.0, location = 'center'):
        super().__init__()
        self.image = image.convert_alpha()
        self.image = pg.transform.scale_by(self.image, scalar)

        self.name = name
        self.intro_speech = intro_speech

        if location == 'bottomleft':
            self.rect = self.image.get_rect(bottomleft = location_tuple)
        else:
            self.rect = self.image.get_rect(center = location_tuple)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def get_rect(self):
        return self.rect
    
    def get_intro_speech(self):
        return self.intro_speech
    
    def get_name(self):
        return self.name

def title_screen():

    text_boxes = pg.sprite.Group()
    text_boxes.add(Text('Fonts/Easter Season.otf', 400, 'PLAY', True, 'Pink', screen_center, bouncing = True, clicked_function = intro_scene))
    text_boxes.add(Text('Fonts/Coolvetica.otf', 40, ' SETTINGS', True, 'Pink', (0, 0), location = 'topleft', clicked_function = open_settings))

    while True:

        for event in pg.event.get():
            check_quit(event)

            if event.type == pg.MOUSEBUTTONUP:
                for text_box in text_boxes:
                    if text_box.get_rect().collidepoint(pg.mouse.get_pos()):
                        text_box.clicked()

        blit_background(gfx.title_bg) 
        text_boxes.update()
        text_boxes.draw(screen)

        tick()

def intro_scene():
    wait_for_boat()
    boat_moves()
    boat_arrived_wo_text()
    boat_arrived_w_text()

def wait_for_boat():
    initial_ticks = pg.time.get_ticks()
    while (pg.time.get_ticks()-initial_ticks)<2000:

        for event in pg.event.get():
            check_quit(event)

            if event.type == pg.MOUSEBUTTONUP:
                return

        blit_background(gfx.gs1_bg)

        tick()

def boat_moves():

    boat_rect = gfx.boat_png.get_rect(bottomright = (-(screen_width//3), screen_height//2.5))

    while boat_rect.x <= screen_width//6:

        for event in pg.event.get():
            check_quit(event)

            if event.type == pg.MOUSEBUTTONUP:
                return

        blit_background(gfx.gs1_bg)
        screen.blit(gfx.boat_png, boat_rect)

        boat_rect.x += screen_width//200
        boat_rect.y += screen_height//800

        tick()

    print(boat_rect.center)
    
def boat_arrived_wo_text():

    boat_rect = gfx.boat_png.get_rect(center = (screen_width//3.42, screen_height//2.265))

    initial_ticks = pg.time.get_ticks()

    while (pg.time.get_ticks()-initial_ticks)<2000:

        for event in pg.event.get():
            check_quit(event)

            if event.type == pg.MOUSEBUTTONUP:
                introductions()

        blit_background(gfx.gs1_bg)
        screen.blit(gfx.boat_png, boat_rect)

        tick()

def boat_arrived_w_text():

    text_boxes = pg.sprite.Group()
    text_boxes.add(Text('Fonts/Easter Season.otf', screen_height//10, '- CLICK TO CONTINUE -', True, 'pink', (width_center, 9*(screen_height//10)), flashing = True))

    boat_rect = gfx.boat_png.get_rect(center = (screen_width//3.42, screen_height//2.265))

    while True:
        
        for event in pg.event.get():
            check_quit(event)

            if event.type == pg.MOUSEBUTTONUP:
                introductions()

        blit_background(gfx.gs1_bg)
        screen.blit(gfx.boat_png, boat_rect)
        text_boxes.update()
        text_boxes.draw(screen)

        tick()

def introductions():

    people = pg.sprite.Group()
    people.add(Person(gfx.man1_png, 'Mark', (0, screen_height), intro_speech = 'This is my text. yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap', scalar = .5, location = 'bottomleft'))
    people.add(Person(gfx.woman1_png, 'Stacy', (0, screen_height), intro_speech = 'My turn to talk! Look at how the text wraps just right! yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap yap', scalar = .5, location = 'bottomleft'))
    for n in range(1, num_characters-1):
        people.add(Person(gfx.pg_png, f'GUY #{n}', (0, screen_height), intro_speech = f'My name is Placeholder Guy number #{n}! I am in place of the other characters that will be added.', scalar = .5, location = 'bottomleft'))

    for person in people:

        text_boxes = text_wrap(person.get_intro_speech(), 'Fonts/Coolvetica Condensed.otf', 30, screen_width//2.5, (person.get_rect().midright[0]+screen_width)//2, person.get_rect().midright[1])
        text_boxes.add(Text('Fonts/Coolvetica.otf', 60, person.get_name(), True, 'pink', (person.get_rect().topright[0]+screen_width//25, person.get_rect().topright[1]+screen_height//15), filled = True, location = 'topleft'))

        clicked = False

        while not clicked:
            #Introduction code, works for everyone
            for event in pg.event.get():
                check_quit(event)

                if event.type == pg.MOUSEBUTTONUP:
                    clicked = True
            
            blit_background(gfx.gs1_bg)
            text_boxes.update()
            text_boxes.draw(screen)
            person.draw(screen)
            tick()

    pick_screen_wo_input_wo_text()

def pick_screen_wo_input_wo_text():

    bg = pg.surface.Surface((screen_width, screen_height))
    bg.fill('white')

    text_boxes = pg.sprite.Group()
    text_boxes.add(Text('Fonts/Coolvetica.otf', 200, 'MEET THE ISLAND', True, 'pink', (width_center, screen_height//10)))

    people = pg.sprite.Group()
    people.add(Person(gfx.man1_png, "Mark", (screen_width//(num_characters+2)*2, screen_height//2.75), scalar = 0.25))
    people.add(Person(gfx.woman1_png, "Stacy", (screen_width//(num_characters+2)*4, screen_height//2.75), scalar = 0.25))

    for n in range(1, 5):
        people.add(Person(gfx.pg_png, f'GUY #{n}', (screen_width//(num_characters+2)*2*(n+2), screen_height//2.75), scalar = 0.25))
    for n in range(5, 11):
        people.add(Person(gfx.pg_png, f'GUY #{n}', (screen_width//(num_characters+2)*2*(n-4), screen_height//1.45), scalar = 0.25))

    for person in people:
        text_boxes.add(Text('Fonts/Coolvetica.otf', 50, person.get_name(), True, 'pink', (person.get_rect().center[0], person.get_rect().center[1] + screen_height//7)))

    initial_ticks = pg.time.get_ticks()

    while (pg.time.get_ticks()-initial_ticks)<2000:

        for event in pg.event.get():
            check_quit(event)

            if event.type == pg.MOUSEBUTTONUP:
                play_week(1)

        blit_background(bg)
        people.draw(screen)
        text_boxes.draw(screen)
        
        tick()

    pick_screen_wo_input_w_text()

def pick_screen_wo_input_w_text():

    bg = pg.surface.Surface((screen_width, screen_height))
    bg.fill('white')

    text_boxes = pg.sprite.Group()
    text_boxes.add(Text('Fonts/Coolvetica.otf', 200, 'MEET THE ISLAND', True, 'pink', (width_center, screen_height//10)))
    text_boxes.add(Text('Fonts/Coolvetica.otf', screen_height//10, '- CLICK TO CONTINUE -', True, 'pink', (width_center, 95*(screen_height//100)), flashing = True))

    people = pg.sprite.Group()
    people.add(Person(gfx.man1_png, "Mark", (screen_width//(num_characters+2)*2, screen_height//2.75), scalar = 0.25))
    people.add(Person(gfx.woman1_png, "Stacy", (screen_width//(num_characters+2)*4, screen_height//2.75), scalar = 0.25))

    for n in range(1, 5):
        people.add(Person(gfx.pg_png, f'GUY #{n}', (screen_width//(num_characters+2)*2*(n+2), screen_height//2.75), scalar = 0.25))
    for n in range(5, 11):
        people.add(Person(gfx.pg_png, f'GUY #{n}', (screen_width//(num_characters+2)*2*(n-4), screen_height//1.45), scalar = 0.25))

    for person in people:
        text_boxes.add(Text('Fonts/Coolvetica.otf', 50, person.get_name(), True, 'pink', (person.get_rect().center[0], person.get_rect().center[1] + screen_height//7)))

    while True:

        for event in pg.event.get():
            check_quit(event)

            if event.type == pg.MOUSEBUTTONUP:
                play_week(1)

        blit_background(bg)
        people.draw(screen)
        text_boxes.update()
        text_boxes.draw(screen)
        
        tick()

def play_week(week):

    if week > 10:
        lost_screen()

    bg = pg.surface.Surface((screen_width, screen_height))
    bg.fill('white')

    text_boxes = pg.sprite.Group()
    text_boxes.add(Text('Fonts/Coolvetica.otf', 100, f'Week {week} Challenge: *challenge_name*', True, 'black', (width_center, screen_height//15)))
    text_boxes.add(Text('Fonts/Coolvetica.otf', 80, 'Info About Weekly Competitions Will Go Here', True, 'black', screen_center))
    text_boxes.add(Text('Fonts/Coolvetica.otf', 50, "These will give the player valuable information about characters' chemistry", True, 'black', (width_center, screen_height//1.6)))

    while True:
        for event in pg.event.get():
            check_quit(event)

            if event.type == pg.MOUSEBUTTONUP:
                truth_booth(week)

        blit_background(bg)

        text_boxes.draw(screen)

        tick()

def truth_booth(week, person1 = None, circle1_center = None, person2 = None, circle2_center = None):
    
    bg = pg.surface.Surface((screen_width, screen_height))
    bg.fill('white')

    text_boxes = pg.sprite.Group()
    text_boxes.add(Text('Fonts/Coolvetica.otf', 150, f'Week {week}: Enter the Booth', True, 'pink', (width_center, screen_height//10)))

    people = pg.sprite.Group()
    people.add(Person(gfx.man1_png, "Mark", (screen_width//(num_characters+2)*2, screen_height//2.75), scalar = 0.25))
    people.add(Person(gfx.woman1_png, "Stacy", (screen_width//(num_characters+2)*4, screen_height//2.75), scalar = 0.25))

    for n in range(1, 5):
        people.add(Person(gfx.pg_png, f'GUY #{n}', (screen_width//(num_characters+2)*2*(n+2), screen_height//2.75), scalar = 0.25))
    for n in range(5, 11):
        people.add(Person(gfx.pg_png, f'GUY #{n}', (screen_width//(num_characters+2)*2*(n-4), screen_height//1.45), scalar = 0.25))

    for person in people:
        text_boxes.add(Text('Fonts/Coolvetica.otf', 50, person.get_name(), True, 'pink', (person.get_rect().center[0], person.get_rect().center[1] + screen_height//7)))

    if person2:
        text_boxes.add(Text('Fonts/Coolvetica.otf', screen_height//10, 'SEND THEM TO THE BOOTH', True, 'pink', (width_center, 95*(screen_height//100)), clicked_function = booth_reveal))

    while True:

        for event in pg.event.get():
            check_quit(event)

            if event.type == pg.MOUSEBUTTONUP:

                if person2:
                    for text_box in text_boxes:
                        if text_box.get_rect().collidepoint(pg.mouse.get_pos()):
                            text_box.clicked(week_param = week, person1_param = person1, person2_param = person2)

                for person in people:
                    if person.get_rect().collidepoint(pg.mouse.get_pos()):
                        if not person1:
                            truth_booth(week, person1 = person, circle1_center = person.get_rect().center)
                        if person1 and not person2:
                            if person.get_name() == person1.get_name():
                                return
                            else:
                                truth_booth(week, person1 = person1, circle1_center = circle1_center, person2 = person, circle2_center = person.get_rect().center)
                        if person1 and person2:
                            if person.get_name() == person1.get_name():
                                truth_booth(week, person1 = person2, circle1_center = circle2_center)
                            elif person.get_name() == person2.get_name():
                                return
        
        blit_background(bg)

        if person1:
            pg.draw.circle(screen, color = 'pink', center = circle1_center, radius = person1.get_rect().width//1.75)
            if person2:
                pg.draw.circle(screen, color = 'pink', center = circle2_center, radius = person1.get_rect().width//1.75)
        
        people.draw(screen)
        text_boxes.draw(screen)

        tick()

def booth_reveal(week, person1, person2):

    guessed = False
    
    for pair in pairs:
        if person1.get_name() in pair and person2.get_name() in pair:
            guessed = True
            break

    bg = pg.surface.Surface((screen_width, screen_height))
    bg.fill('white')

    text_boxes = pg.sprite.Group()
    
    if guessed:

        text_boxes.add(Text('Fonts/Coolvetica.otf', 200, 'Correct!', True, 'black', screen_center))
        text_boxes.add(Text('Fonts/Coolvetica.otf', 50, f'Pair identified: {person1.get_name()} and {person2.get_name()}.', True, 'black', (width_center, screen_height//1.6)))

        while True:
            for event in pg.event.get():
                check_quit(event)

                if event.type == pg.MOUSEBUTTONUP:
                    pick_screen_w_input(week, guessed_pairs = [], person1 = None, circle1_center = None, person2 = None, circle2_center = None)

            blit_background(bg)

            text_boxes.draw(screen)

            tick()
    else:

        text_boxes.add(Text('Fonts/Coolvetica.otf', 300, 'Wrong!', True, 'black', screen_center))

        while True:
            for event in pg.event.get():
                check_quit(event)

                if event.type == pg.MOUSEBUTTONUP:
                    pick_screen_w_input(week, guessed_pairs = [], person1 = None, circle1_center = None, person2 = None, circle2_center = None)

            blit_background(bg)

            text_boxes.draw(screen)

            tick()

def pick_screen_w_input(week, person1 = None, circle1_center = None, person2 = None, circle2_center = None, guessed_pairs = []):

    while len(guessed_pairs) < num_characters/2:

        bg = pg.surface.Surface((screen_width, screen_height))
        bg.fill('white')

        text_boxes = pg.sprite.Group()
        text_boxes.add(Text('Fonts/Coolvetica.otf', 150, f'Week {week}: Guess Your Pairs', True, 'pink', (width_center, screen_height//10)))

        people = pg.sprite.Group()
        people.add(Person(gfx.man1_png, "Mark", (screen_width//(num_characters+2)*2, screen_height//2.75), scalar = 0.25))
        people.add(Person(gfx.woman1_png, "Stacy", (screen_width//(num_characters+2)*4, screen_height//2.75), scalar = 0.25))

        for n in range(1, 5):
            people.add(Person(gfx.pg_png, f'GUY #{n}', (screen_width//(num_characters+2)*2*(n+2), screen_height//2.75), scalar = 0.25))
        for n in range(5, 11):
            people.add(Person(gfx.pg_png, f'GUY #{n}', (screen_width//(num_characters+2)*2*(n-4), screen_height//1.45), scalar = 0.25))

        for person in people:
            text_boxes.add(Text('Fonts/Coolvetica.otf', 50, person.get_name(), True, 'pink', (person.get_rect().center[0], person.get_rect().center[1] + screen_height//7)))

        if person2:
            text_boxes.add(Text('Fonts/Coolvetica.otf', screen_height//10, 'SUBMIT', True, 'pink', (width_center, 95*(screen_height//100)), clicked_function = pick_screen_w_input))

        while True:

            for event in pg.event.get():
                check_quit(event)

                if event.type == pg.MOUSEBUTTONUP:

                    if person2:
                        for text_box in text_boxes:
                            if text_box.get_rect().collidepoint(pg.mouse.get_pos()):
                                text_box.clicked(guessed_pairs_param = guessed_pairs, week_param = week, person1_param = person1, person2_param = person2)

                    for person in people:
                        if person.get_rect().collidepoint(pg.mouse.get_pos()):
                            if not person1:
                                pick_screen_w_input(week, person1 = person, circle1_center = person.get_rect().center, guessed_pairs = guessed_pairs)
                            if person1 and not person2:
                                if person.get_name() == person1.get_name():
                                    pick_screen_w_input(week, guessed_pairs = guessed_pairs)
                                else:
                                    pick_screen_w_input(week, person1 = person1, circle1_center = circle1_center, person2 = person, circle2_center = person.get_rect().center, guessed_pairs = guessed_pairs)
                            if person1 and person2:
                                if person.get_name() == person1.get_name():
                                    pick_screen_w_input(week, person1 = person2, circle1_center = circle2_center, guessed_pairs = guessed_pairs)
                                elif person.get_name() == person2.get_name():
                                    pick_screen_w_input(week, person1 = person1, circle1_center = circle1_center, guessed_pairs = guessed_pairs)
                
            blit_background(bg)

            if person1:
                pg.draw.circle(screen, color = 'pink', center = circle1_center, radius = person1.get_rect().width//1.75)
                if person2:
                    pg.draw.circle(screen, color = 'pink', center = circle2_center, radius = person1.get_rect().width//1.75)
                
            people.draw(screen)
            text_boxes.draw(screen)

            tick()

    check_pairs(week, guessed_pairs)

def check_pairs(week, guessed_pairs):
    
    num_guessed = 0
    
    for guessed_pair in guessed_pairs:
        for pair in pairs:
            if guessed_pair[0].get_name() in pair and guessed_pair[1].get_name() in pair:
                num_guessed += 1

    if num_guessed >= num_characters/2:
        won_screen()
    else:
        bg = pg.surface.Surface((screen_width, screen_height))
        bg.fill('white')

        text_boxes = pg.sprite.Group()
        text_boxes.add(Text('Fonts/Easter Season.otf', 75, f'{num_guessed} pairs correctly identified.', True, 'pink', screen_center))

        while True:
            for event in pg.event.get():
                check_quit(event)

                if event.type == pg.MOUSEBUTTONUP:
                    play_week(week+1)

            blit_background(bg)

            text_boxes.draw(screen)

            tick()

def lost_screen():

    bg = pg.surface.Surface((screen_width, screen_height))
    bg.fill('white')

    text_boxes = pg.sprite.Group()
    text_boxes.add(Text('Fonts/Easter Season.otf', 600, 'YOU LOST.', True, 'pink', screen_center))
    text_boxes.add(Text('Fonts/Coolvetica.otf', 30, ' Return to Title Screen', True, 'pink', (0, 0), location = 'topleft', clicked_function = title_screen))

    while True:
        for event in pg.event.get():
            check_quit(event)

            if event.type == pg.MOUSEBUTTONUP:
                for text_box in text_boxes:
                    if text_box.get_rect().collidepoint(pg.mouse.get_pos()):
                        text_box.clicked()

        blit_background(bg)
        text_boxes.draw(screen)

        tick()

def won_screen():

    bg = pg.surface.Surface((screen_width, screen_height))
    bg.fill('white')

    text_boxes = pg.sprite.Group()
    text_boxes.add(Text('Fonts/Easter Season.otf', 600, 'YOU WON!', True, 'pink', screen_center))
    text_boxes.add(Text('Fonts/Coolvetica.otf', 30, ' Return to Title Screen', True, 'pink', (0, 0), location = 'topleft', clicked_function = title_screen))

    while True:
        for event in pg.event.get():
            check_quit(event)

            if event.type == pg.MOUSEBUTTONUP:
                for text_box in text_boxes:
                    if text_box.get_rect().collidepoint(pg.mouse.get_pos()):
                        text_box.clicked()

        blit_background(bg)
        text_boxes.draw(screen)

        tick()

def open_settings():
    while True:
        
        text_boxes = pg.sprite.Group()
        text_boxes.add(Text('Fonts/Easter Season.otf', 50, 'hi', True, 'white', screen_center))

        for event in pg.event.get():
            check_quit(event)

            if event.type == pg.MOUSEBUTTONUP:
                for text_box in text_boxes:
                    if text_box.get_rect().collidepoint(pg.mouse.get_pos()):
                        text_box.clicked()

        screen.blit(gfx.boat_png, screen_center)
        
        tick()
  
def blit_background(background):
    screen.blit(background, (0,0))

def check_quit(event):
    # Stop game loop if user quits
    if event.type == pg.QUIT: 
        # Stop all code
        pg.quit()
        exit()

def text_wrap(text, font_arg, font_size, allowed_width, center_x, center_y):
    # first, split the text into words
    words = text.split()

    font = pg.font.Font(font_arg, font_size)

    # now, construct lines out of these words
    lines = []
    while len(words) > 0:
        # get as many words as will fit within allowed_width
        line_words = []
        while len(words) > 0:
            line_words.append(words.pop(0))
            fw = font.size(' '.join(line_words + words[:1]))[0]
            if fw > allowed_width:
                break

        # add a line consisting of those words
        line = ' '.join(line_words)
        lines.append(line)

    text_boxes = pg.sprite.Group()
    y_offset = 0
    for line in lines:
        fw, fh = font.size(line)

        # (tx, ty) is the top-left of the font surface
        tx = center_x - fw / 2
        ty = center_y + y_offset
        text_boxes.add(Text(font_arg, 40, line, True, 'black', (tx, ty), location = 'topleft', filled = True))

        y_offset += fh

    return text_boxes

if __name__ == '__main__':
    pg.init()
    title_screen()
