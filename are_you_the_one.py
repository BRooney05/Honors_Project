import pygame as pg
import setup
from sys import exit
from settings import screen_width, screen_height, width_center, height_center, screen_center, num_characters, fps
from setup import screen, pairs, challenge_names, challenge_descriptions, challenge_goals, challenge_hints, tick
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
        
    def clicked(self, guessed_pairs_param = None, week_param = None, person1_name = None, person2_name = None):
        if self.clicked_function:
            if self.clicked_function == pick_screen_w_input:
                guessed_pairs_param.append([person1_name, person2_name])
                self.clicked_function(week_param, guessed_pairs = guessed_pairs_param)
            elif person1_name:
                self.clicked_function(week_param, person1_name, person2_name)
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
    # text_boxes.add(Text('Fonts/Coolvetica.otf', 40, ' SETTINGS', True, 'Pink', (0, 0), location = 'topleft', clicked_function = open_settings))

    while True:

        for event in pg.event.get():
            check_quit(event)

            if event.type == pg.MOUSEBUTTONUP:
                click_sound.play()
                for text_box in text_boxes:
                    if text_box.get_rect().collidepoint(pg.mouse.get_pos()):
                        text_box.clicked()

        blit_background(gfx.title_bg) 
        text_boxes.update()
        text_boxes.draw(screen)

        tick()

def intro_scene():
    boat_arrival()
    boat_arrived_wo_text()
    boat_arrived_w_text()

def boat_arrival():
    initial_ticks = pg.time.get_ticks()

    boat_sound = pg.mixer.Sound('Sounds/Boat Engine Sound.flac')
    boat_sound.set_volume(0.80)
    boat_sound.play()

    while (pg.time.get_ticks()-initial_ticks)<2000:

        for event in pg.event.get():
            check_quit(event)

            if event.type == pg.MOUSEBUTTONUP:
                click_sound.play()
                boat_sound.stop()
                return

        blit_background(gfx.gs1_bg)

        tick()

    boat_rect = gfx.boat_png.get_rect(bottomright = (-(screen_width//3), screen_height//2.5))

    while boat_rect.x <= screen_width//6:

        for event in pg.event.get():
            check_quit(event)

            if event.type == pg.MOUSEBUTTONUP:
                click_sound.play()
                boat_sound.stop()
                return

        blit_background(gfx.gs1_bg)
        screen.blit(gfx.boat_png, boat_rect)

        boat_rect.x += screen_width//200
        boat_rect.y += screen_height//800

        tick()

    print(boat_rect.center)
    
    boat_sound.fadeout(1000)

def boat_arrived_wo_text():

    boat_rect = gfx.boat_png.get_rect(center = (screen_width//3.42, screen_height//2.265))

    initial_ticks = pg.time.get_ticks()

    while (pg.time.get_ticks()-initial_ticks)<2000:

        for event in pg.event.get():
            check_quit(event)

            if event.type == pg.MOUSEBUTTONUP:
                click_sound.play()
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
                click_sound.play()
                introductions()

        blit_background(gfx.gs1_bg)
        screen.blit(gfx.boat_png, boat_rect)
        text_boxes.update()
        text_boxes.draw(screen)

        tick()

def introductions():

    boat_rect = gfx.boat_png.get_rect(center = (screen_width//3.42, screen_height//2.265))

    people = pg.sprite.Group()
    people.add(Person(gfx.woman1_png, 'Stacy', (0, screen_height), intro_speech = "Hey y'all, it's Stacy! I didn't come the way from Arkansas to not find true love. I may be a country gal, but I've got my eyes set on bigger things! Someday, I wanna live in one of those big fancy high-rise apartments. Someday...", scalar = .5, location = 'bottomleft'))
    people.add(Person(gfx.woman2_png, 'Grace', (0, screen_height), intro_speech = "My name's Grace, or Gracie as my friends call me. I'd call myself something of a party girl, but that doesn't mean I wouldn't like to find my one and settle down.", scalar = .5, location = 'bottomleft'))
    people.add(Person(gfx.woman3_png, 'Jessica', (0, screen_height), intro_speech = "Hi! I'm Jess, a New Yorker through and through! I love the sights, the food, the music, and everything to do with this beautiful city. It's my forever home, that's for sure.", scalar = .5, location = 'bottomleft'))
    people.add(Person(gfx.woman4_png, 'Sarah', (0, screen_height), intro_speech = "Hey! My name's Sarah. My dream is to travel the world. Other cultures have always fascinated me. I want to see Rome, Greece, Egypt... If there's history, I'm interested!", scalar = .5, location = 'bottomleft'))
    people.add(Person(gfx.woman5_png, 'Cecelia', (0, screen_height), intro_speech = "Hey everybody, I'm Cecelia! The first thing you'll learn about me is that I adore kids. I've been a preschool teacher for 7 years, and I can't wait to settle down and have children of my own. The money isn't all there yet, but maybe a win on this show could take off some pressure!", scalar = .5, location = 'bottomleft'))
    people.add(Person(gfx.woman6_png, 'Kendall', (0, screen_height), intro_speech = "Hi, I'm Kendall. I work as a real-estate agent in Miami. I may look nice, but I take my job very, very seriously. I dominate my district- other agents dont stand a chance!", scalar = .5, location = 'bottomleft'))

    people.add(Person(gfx.man1_png, 'Mark', (0, screen_height), intro_speech = "What's up? I'm Mark, an aspiring actor from sunny San Diego! Nothing grinds my gears more than someone who can't appreciate culture. If you can't settle down and watch a classic movie or read a good book, you're not the one for me!", scalar = .5, location = 'bottomleft'))
    people.add(Person(gfx.man2_png, 'Jaden', (0, screen_height), intro_speech = "Hi, I'm Jaden! I moved from Puerto Rico when I was little, but the outdoors still calls my name. I love to surf and enjoy the fresh summer breeze on my face.", scalar = .5, location = 'bottomleft'))
    people.add(Person(gfx.man3_png, 'Thomas', (0, screen_height), intro_speech = "My name is Thomas. After getting my PhD from UConn, I opened my practice in the Big Apple. It's hard work, but it brings in more than enough to support the family that I'll start someday.", scalar = .5, location = 'bottomleft'))
    people.add(Person(gfx.man4_png, 'Adam', (0, screen_height), intro_speech = "Howdy! The name's Adam. I'm a golfer from way down in Austin. I love going out on the town and finding a good time, and the bar is always a good place to start. Who knows where the night will take me? That's the adventure!", scalar = .5, location = 'bottomleft'))
    people.add(Person(gfx.man5_png, 'Bradley', (0, screen_height), intro_speech = "Yo, It's Brad. I started working as a concierge after football didn't work out, but you bet I'm still addicted to competition. Any kind of sporting event, I'm there. I don't think twice.", scalar = .5, location = 'bottomleft'))
    people.add(Person(gfx.pg_png, 'Guy', (0, screen_height), intro_speech = "Fan favorite Placeholder Guy here, as requested! I know you missed me. No hints here... Good luck finding my match!", scalar = .5, location = 'bottomleft'))

    for person in people:

        text_boxes = text_wrap(person.get_intro_speech(), 'Fonts/Coolvetica Condensed.otf', 30, screen_width//2.5, (person.get_rect().midright[0]+screen_width)//2, person.get_rect().midright[1])
        text_boxes.add(Text('Fonts/Coolvetica.otf', 60, person.get_name(), True, 'pink', (person.get_rect().topright[0]+screen_width//25, person.get_rect().topright[1]+screen_height//15), filled = True, location = 'topleft'))

        clicked = False

        while not clicked:
            #Introduction code, works for everyone
            for event in pg.event.get():
                check_quit(event)

                if event.type == pg.MOUSEBUTTONUP:
                    click_sound.play()
                    clicked = True
            
            blit_background(gfx.gs1_bg)
            screen.blit(gfx.boat_png, boat_rect)
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
    people.add(Person(gfx.woman1_png, "Stacy", (screen_width//(num_characters+2)*2, screen_height//2.75), scalar = 0.25))
    people.add(Person(gfx.woman2_png, "Grace", (screen_width//(num_characters+2)*4, screen_height//2.75), scalar = 0.25))
    people.add(Person(gfx.woman3_png, "Jessica", (screen_width//(num_characters+2)*6, screen_height//2.75), scalar = 0.25))
    people.add(Person(gfx.woman4_png, "Sarah", (screen_width//(num_characters+2)*8, screen_height//2.75), scalar = 0.25))
    people.add(Person(gfx.woman5_png, "Cecelia", (screen_width//(num_characters+2)*10, screen_height//2.75), scalar = 0.25))
    people.add(Person(gfx.woman6_png, "Kendall", (screen_width//(num_characters+2)*12, screen_height//2.75), scalar = 0.25))
    people.add(Person(gfx.man1_png, "Mark", (screen_width//(num_characters+2)*2, screen_height//1.45), scalar = 0.25))
    people.add(Person(gfx.man2_png, "Jaden", (screen_width//(num_characters+2)*4, screen_height//1.45), scalar = 0.25))
    people.add(Person(gfx.man3_png, "Thomas", (screen_width//(num_characters+2)*6, screen_height//1.45), scalar = 0.25))
    people.add(Person(gfx.man4_png, "Adam", (screen_width//(num_characters+2)*8, screen_height//1.45), scalar = 0.25))
    people.add(Person(gfx.man5_png, "Bradley", (screen_width//(num_characters+2)*10, screen_height//1.45), scalar = 0.25))
    people.add(Person(gfx.pg_png, "Guy", (screen_width//(num_characters+2)*12, screen_height//1.45), scalar = 0.25))

    for person in people:
        text_boxes.add(Text('Fonts/Coolvetica.otf', 50, person.get_name(), True, 'pink', (person.get_rect().center[0], person.get_rect().center[1] + screen_height//7)))

    initial_ticks = pg.time.get_ticks()

    while (pg.time.get_ticks()-initial_ticks)<2000:

        for event in pg.event.get():
            check_quit(event)

            if event.type == pg.MOUSEBUTTONUP:
                click_sound.play()
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
    people.add(Person(gfx.woman1_png, "Stacy", (screen_width//(num_characters+2)*2, screen_height//2.75), scalar = 0.25))
    people.add(Person(gfx.woman2_png, "Grace", (screen_width//(num_characters+2)*4, screen_height//2.75), scalar = 0.25))
    people.add(Person(gfx.woman3_png, "Jessica", (screen_width//(num_characters+2)*6, screen_height//2.75), scalar = 0.25))
    people.add(Person(gfx.woman4_png, "Sarah", (screen_width//(num_characters+2)*8, screen_height//2.75), scalar = 0.25))
    people.add(Person(gfx.woman5_png, "Cecelia", (screen_width//(num_characters+2)*10, screen_height//2.75), scalar = 0.25))
    people.add(Person(gfx.woman6_png, "Kendall", (screen_width//(num_characters+2)*12, screen_height//2.75), scalar = 0.25))
    people.add(Person(gfx.man1_png, "Mark", (screen_width//(num_characters+2)*2, screen_height//1.45), scalar = 0.25))
    people.add(Person(gfx.man2_png, "Jaden", (screen_width//(num_characters+2)*4, screen_height//1.45), scalar = 0.25))
    people.add(Person(gfx.man3_png, "Thomas", (screen_width//(num_characters+2)*6, screen_height//1.45), scalar = 0.25))
    people.add(Person(gfx.man4_png, "Adam", (screen_width//(num_characters+2)*8, screen_height//1.45), scalar = 0.25))
    people.add(Person(gfx.man5_png, "Bradley", (screen_width//(num_characters+2)*10, screen_height//1.45), scalar = 0.25))
    people.add(Person(gfx.pg_png, "Guy", (screen_width//(num_characters+2)*12, screen_height//1.45), scalar = 0.25))

    for person in people:
        text_boxes.add(Text('Fonts/Coolvetica.otf', 50, person.get_name(), True, 'pink', (person.get_rect().center[0], person.get_rect().center[1] + screen_height//7)))

    while True:

        for event in pg.event.get():
            check_quit(event)

            if event.type == pg.MOUSEBUTTONUP:
                click_sound.play()
                play_week(1)

        blit_background(bg)
        people.draw(screen)
        text_boxes.update()
        text_boxes.draw(screen)
        
        tick()

def play_week(week):

    if week > 6:
        lost_screen()

    bg = pg.surface.Surface((screen_width, screen_height))
    bg.fill('white')

    text_boxes = pg.sprite.Group()
    text_boxes.add(Text('Fonts/Coolvetica.otf', 100, f'Week {week} Challenge: {challenge_names[week-1]}', True, 'black', (width_center, screen_height//15)))
    text_boxes.add(Text('Fonts/Coolvetica.otf', 30, challenge_descriptions[week-1], True, 'black', (width_center, screen_height//6)))
    text_boxes.add(Text('Fonts/Coolvetica.otf', 50, challenge_goals[week-1], True, 'black', (width_center, screen_height//4.5)))
    text_boxes.add(Text('Fonts/Coolvetica.otf', 40, challenge_hints[week-1][0], True, 'black', (width_center, screen_height//2.10)))
    text_boxes.add(Text('Fonts/Coolvetica.otf', 40, challenge_hints[week-1][1], True, 'black', (width_center, screen_height//1.73)))
    text_boxes.add(Text('Fonts/Coolvetica.otf', 40, challenge_hints[week-1][2], True, 'black', (width_center, screen_height//1.50)))

    while True:
        for event in pg.event.get():
            check_quit(event)

            if event.type == pg.MOUSEBUTTONUP:
                click_sound.play()
                truth_booth(week)

        blit_background(bg)

        text_boxes.draw(screen)

        tick()

def truth_booth(week, person1 = None, circle1_center = None, person2 = None, circle2_center = None):
    
    text_boxes = pg.sprite.Group()
    text_boxes.add(Text('Fonts/Coolvetica.otf', 150, f'Week {week}: Enter the Booth', True, 'pink', (width_center, screen_height//10), filled = True))

    people = pg.sprite.Group()
    people.add(Person(gfx.woman1_png, "Stacy", (screen_width//(num_characters+2)*2, screen_height//2.75), scalar = 0.25))
    people.add(Person(gfx.woman2_png, "Grace", (screen_width//(num_characters+2)*4, screen_height//2.75), scalar = 0.25))
    people.add(Person(gfx.woman3_png, "Jessica", (screen_width//(num_characters+2)*6, screen_height//2.75), scalar = 0.25))
    people.add(Person(gfx.woman4_png, "Sarah", (screen_width//(num_characters+2)*8, screen_height//2.75), scalar = 0.25))
    people.add(Person(gfx.woman5_png, "Cecelia", (screen_width//(num_characters+2)*10, screen_height//2.75), scalar = 0.25))
    people.add(Person(gfx.woman6_png, "Kendall", (screen_width//(num_characters+2)*12, screen_height//2.75), scalar = 0.25))
    people.add(Person(gfx.man1_png, "Mark", (screen_width//(num_characters+2)*2, screen_height//1.45), scalar = 0.25))
    people.add(Person(gfx.man2_png, "Jaden", (screen_width//(num_characters+2)*4, screen_height//1.45), scalar = 0.25))
    people.add(Person(gfx.man3_png, "Thomas", (screen_width//(num_characters+2)*6, screen_height//1.45), scalar = 0.25))
    people.add(Person(gfx.man4_png, "Adam", (screen_width//(num_characters+2)*8, screen_height//1.45), scalar = 0.25))
    people.add(Person(gfx.man5_png, "Bradley", (screen_width//(num_characters+2)*10, screen_height//1.45), scalar = 0.25))
    people.add(Person(gfx.pg_png, "Guy", (screen_width//(num_characters+2)*12, screen_height//1.45), scalar = 0.25))

    for person in people:
        text_boxes.add(Text('Fonts/Coolvetica.otf', 50, person.get_name(), True, 'pink', (person.get_rect().center[0], person.get_rect().center[1] + screen_height//7)))

    if person2:
        text_boxes.add(Text('Fonts/Coolvetica.otf', screen_height//10, 'SEND THEM TO THE BOOTH', True, 'pink', (width_center, 95*(screen_height//100)), clicked_function = booth_reveal, filled = True))

    while True:

        for event in pg.event.get():
            check_quit(event)

            if event.type == pg.MOUSEBUTTONUP:
                click_sound.play()

                if person2:
                    for text_box in text_boxes:
                        if text_box.get_rect().collidepoint(pg.mouse.get_pos()):
                            text_box.clicked(week_param = week, person1_name = person1.get_name(), person2_name = person2.get_name())

                for person in people:
                    if person.get_rect().collidepoint(pg.mouse.get_pos()):

                        not_yet_confirmed = True
                        for pair in confirmed_pairs:
                            if person.get_name() in pair:
                                not_yet_confirmed = False
                                break
                        
                        if not_yet_confirmed:
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
        
        blit_background(gfx.tb_bg)

        if person1:
            pg.draw.circle(screen, color = 'pink', center = circle1_center, radius = person1.get_rect().width//1.75)
            if person2:
                pg.draw.circle(screen, color = 'pink', center = circle2_center, radius = person1.get_rect().width//1.75)

        for person in people:
            for pair in confirmed_pairs:
                if person.get_name() in pair:
                    pg.draw.circle(screen, color = 'chartreuse4', center = person.get_rect().center, radius = person.get_rect().width//1.75)
        
        people.draw(screen)
        text_boxes.update()
        text_boxes.draw(screen)

        tick()

def booth_reveal(week, person1_name, person2_name):

    guessed = False
    
    for pair in pairs:
        if person1_name in pair and person2_name in pair:
            guessed = True
            break

    bg = pg.surface.Surface((screen_width, screen_height))
    bg.fill('white')

    text_boxes = pg.sprite.Group()
    
    if guessed:

        text_boxes.add(Text('Fonts/Coolvetica.otf', 200, 'Correct!', True, 'black', screen_center))
        text_boxes.add(Text('Fonts/Coolvetica.otf', 50, f'Pair identified: {person1_name} and {person2_name}.', True, 'black', (width_center, screen_height//1.6)))

        confirmed_pairs.append((person1_name, person2_name))

        while True:
            for event in pg.event.get():
                check_quit(event)

                if event.type == pg.MOUSEBUTTONUP:
                    click_sound.play()
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
                    click_sound.play()
                    pick_screen_w_input(week, guessed_pairs = [], person1 = None, circle1_center = None, person2 = None, circle2_center = None)

            blit_background(bg)

            text_boxes.draw(screen)

            tick()

def pick_screen_w_input(week, person1 = None, circle1_center = None, person2 = None, circle2_center = None, guessed_pairs = []):

    while len(guessed_pairs)+len(confirmed_pairs) < num_characters/2:

        bg = pg.surface.Surface((screen_width, screen_height))
        bg.fill('white')

        text_boxes = pg.sprite.Group()
        text_boxes.add(Text('Fonts/Coolvetica.otf', 150, f'Week {week}: Guess Your Pairs', True, 'pink', (width_center, screen_height//10)))

        people = pg.sprite.Group()
        people.add(Person(gfx.woman1_png, "Stacy", (screen_width//(num_characters+2)*2, screen_height//2.75), scalar = 0.25))
        people.add(Person(gfx.woman2_png, "Grace", (screen_width//(num_characters+2)*4, screen_height//2.75), scalar = 0.25))
        people.add(Person(gfx.woman3_png, "Jessica", (screen_width//(num_characters+2)*6, screen_height//2.75), scalar = 0.25))
        people.add(Person(gfx.woman4_png, "Sarah", (screen_width//(num_characters+2)*8, screen_height//2.75), scalar = 0.25))
        people.add(Person(gfx.woman5_png, "Cecelia", (screen_width//(num_characters+2)*10, screen_height//2.75), scalar = 0.25))
        people.add(Person(gfx.woman6_png, "Kendall", (screen_width//(num_characters+2)*12, screen_height//2.75), scalar = 0.25))
        people.add(Person(gfx.man1_png, "Mark", (screen_width//(num_characters+2)*2, screen_height//1.45), scalar = 0.25))
        people.add(Person(gfx.man2_png, "Jaden", (screen_width//(num_characters+2)*4, screen_height//1.45), scalar = 0.25))
        people.add(Person(gfx.man3_png, "Thomas", (screen_width//(num_characters+2)*6, screen_height//1.45), scalar = 0.25))
        people.add(Person(gfx.man4_png, "Adam", (screen_width//(num_characters+2)*8, screen_height//1.45), scalar = 0.25))
        people.add(Person(gfx.man5_png, "Bradley", (screen_width//(num_characters+2)*10, screen_height//1.45), scalar = 0.25))
        people.add(Person(gfx.pg_png, "Guy", (screen_width//(num_characters+2)*12, screen_height//1.45), scalar = 0.25))

        for person in people:
            text_boxes.add(Text('Fonts/Coolvetica.otf', 50, person.get_name(), True, 'pink', (person.get_rect().center[0], person.get_rect().center[1] + screen_height//7)))

        if person2:
            text_boxes.add(Text('Fonts/Coolvetica.otf', screen_height//10, 'SUBMIT', True, 'pink', (width_center, 95*(screen_height//100)), clicked_function = pick_screen_w_input))

        while True:

            for event in pg.event.get():
                check_quit(event)

                if event.type == pg.MOUSEBUTTONUP:
                    click_sound.play()

                    if person2:
                        for text_box in text_boxes:
                            if text_box.get_rect().collidepoint(pg.mouse.get_pos()):
                                text_box.clicked(guessed_pairs_param = guessed_pairs, week_param = week, person1_name = person1.get_name(), person2_name = person2.get_name())

                    for person in people:
                        if person.get_rect().collidepoint(pg.mouse.get_pos()):
                            not_yet_guessed = True
                            for pair in guessed_pairs:
                                if person.get_name() in pair:
                                    not_yet_guessed = False
                                    break

                            not_yet_confirmed = True
                            for pair in confirmed_pairs:
                                if person.get_name() in pair:
                                    not_yet_confirmed = False
                                    break

                            if not_yet_guessed and not_yet_confirmed:
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
                
            for person in people:
                for pair in confirmed_pairs:
                    if person.get_name() in pair:
                        pg.draw.circle(screen, color = 'chartreuse4', center = person.get_rect().center, radius = person.get_rect().width//1.75)
                for pair in guessed_pairs:
                    if person.get_name() in pair:
                        pg.draw.circle(screen, color = 'darksalmon', center = person.get_rect().center, radius = person.get_rect().width//1.75)

            people.draw(screen)
            text_boxes.draw(screen)

            tick()

    check_pairs(week, guessed_pairs)

def check_pairs(week, guessed_pairs):
    
    num_guessed = 0
    
    for guessed_pair in guessed_pairs:
        for pair in pairs:
            if guessed_pair[0] in pair and guessed_pair[1] in pair:
                num_guessed += 1

    if num_guessed+len(confirmed_pairs) >= num_characters/2:
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
                    click_sound.play()
                    play_week(week+1)

            blit_background(bg)

            text_boxes.draw(screen)

            tick()

def lost_screen():

    global confirmed_pairs 
    confirmed_pairs = []

    bg = pg.surface.Surface((screen_width, screen_height))
    bg.fill('white')

    text_boxes = pg.sprite.Group()
    text_boxes.add(Text('Fonts/Easter Season.otf', 600, 'YOU LOST.', True, 'pink', screen_center))
    text_boxes.add(Text('Fonts/Coolvetica.otf', 30, ' Return to Title Screen', True, 'pink', (0, 0), location = 'topleft', clicked_function = title_screen))

    while True:
        for event in pg.event.get():
            check_quit(event)

            if event.type == pg.MOUSEBUTTONUP:
                click_sound.play()
                for text_box in text_boxes:
                    if text_box.get_rect().collidepoint(pg.mouse.get_pos()):
                        text_box.clicked()

        blit_background(bg)
        text_boxes.draw(screen)

        tick()

def won_screen():

    global confirmed_pairs 
    confirmed_pairs = []

    bg = pg.surface.Surface((screen_width, screen_height))
    bg.fill('white')

    text_boxes = pg.sprite.Group()
    text_boxes.add(Text('Fonts/Easter Season.otf', 600, 'YOU WON!', True, 'pink', screen_center))
    text_boxes.add(Text('Fonts/Coolvetica.otf', 30, ' Return to Title Screen', True, 'pink', (0, 0), location = 'topleft', clicked_function = title_screen))

    while True:
        for event in pg.event.get():
            check_quit(event)

            if event.type == pg.MOUSEBUTTONUP:
                click_sound.play()
                for text_box in text_boxes:
                    if text_box.get_rect().collidepoint(pg.mouse.get_pos()):
                        text_box.clicked()

        blit_background(bg)
        text_boxes.draw(screen)

        tick()

def open_settings():
    while True:
        
        text_boxes = pg.sprite.Group()
        text_boxes.add(Text('Fonts/Coolvetica.otf', 150, 'Settings', True, 'pink', (width_center, screen_height//15)))
        text_boxes.add(Text('Fonts/Coolvetica Condensed.otf', 90, f'Screen Dimensions: {screen_width}x{screen_height}', True, 'pink', (width_center, 3.5*screen_height//15)))
        text_boxes.add(Text('Fonts/Coolvetica Condensed.otf', 90, f'FPS: {fps}', True, 'pink', (width_center, 6*screen_height//15)))
        text_boxes.add(Text('Fonts/Coolvetica Condensed.otf', 90, f'Number of Characters: {num_characters}', True, 'pink', (width_center, 8.5*screen_height//15)))
        text_boxes.add(Text('Fonts/Coolvetica Condensed.otf', 90, f'Game Mode:', True, 'pink', (width_center, 11*screen_height//15)))
        text_boxes.add(Text('Fonts/Coolvetica Condensed.otf', 70, f'Easy', True, 'pink', (int(width_center*0.85), 12.5*screen_height//15)))
        text_boxes.add(Text('Fonts/Coolvetica Condensed.otf', 70, f'Hard', True, 'pink', (int(width_center*1.15), 12.5*screen_height//15)))
        text_boxes.add(Text('Fonts/Coolvetica.otf', 40, ' Back to Title', True, 'Pink', (0, 0), location = 'topleft', clicked_function = title_screen))

        bg = pg.surface.Surface((screen_width, screen_height))
        bg.fill('white')

        for event in pg.event.get():
            check_quit(event)

            if event.type == pg.MOUSEBUTTONUP:
                click_sound.play()
                for text_box in text_boxes:
                    if text_box.get_rect().collidepoint(pg.mouse.get_pos()):
                        text_box.clicked()

        blit_background(bg)
        pg.draw.line(screen, 'pink', (int(width_center*0.65), screen_height//7), (int(width_center*1.35), screen_height//7), screen_height//150)
        text_boxes.draw(screen)
        
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
    pg.mixer.init()

    pg.mixer.music.load('Sounds/Background Music.wav')
    pg.mixer.music.play(loops=-1)

    click_sound = pg.mixer.Sound('Sounds/Click.wav')

    confirmed_pairs = []

    title_screen()
