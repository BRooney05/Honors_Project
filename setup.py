import pygame as pg
import Graphics.graphics as gfx
from settings import screen_width, screen_height, fps
from sys import exit

clock = pg.time.Clock()

pairs = [("Cecelia", "Thomas"), ("Jessica", "Mark"), ("Sarah", "Jaden"), ("Grace", "Bradley"), ("Stacy", "Adam"), ("Kendall", "Guy")]

challenge_names = ["Target Practice!", "Karaoke Night!", "Swim Meet!", "Arts & Crafts!", "Cooking Show!", "Sumo Battle!"]
challenge_descriptions = ["One contestant will hold a bow while their teammate draws and releases the string.", "One contestant will have an hour to write and compose a song that their partener will perform without practice.", "One contestant must swim through a pool of peanut butter while their teammate works to sabotage other swimmers.", "One contestant must make an modern artistic masterpiece, while their teammate acts as the canvas.", "One competetor must race to acquire ingredients so that their teammate can make the best meal possible.", "One competetor sits atop their teammate's shoulders as all six teams try to push one another out of the ring."]
challenge_goals = ["Most points after three rounds wins.", "Best performance wins.", "Fastest time wins.", "Best artwork wins.", "Best meal wins.", "Last team standing wins."]
challenge_hints = [("-Grace and Thomas bring home the win with a strong team performance", "-Jaden and Sarah struggle for two rounds, but do well on their third try", "-Adam and Jessica barely manage to hit the target"), ("-Cecelia breaks out her angelic voice, earning a win with Guy's song", "-Mark writes a great song for Jessica, which she performs beautifully", "-Bradley apologizes to Kendall after writing her a bad song"), ("-Bradley's strong swimming carried himself and Stacy to an easy win.", "-Jaden does a good job slowing others down while Cecelia steadily completes the race", "-Determined to win, Kendall swims as fast as she can, but Thomas doesn't help much"), ("-Grace paints a beautiful city skyline on Mark for the win", "-Guy and Stacy come in close second with an awesome stick man drawing", "-Sarah refuses to let Adam paint on her face"), ("-Stacy and Adam win with a delicious country dish", "-Jaden gets Celia everything she needs to make a tasty apple pie", "-Sarah fails to get Thomas more than some pasta and some sauce"), ("-Mark and Stacy avoid conflict and strike at the end, winning first place", "-Bradley stands strong while Grace forces many other teams out of the ring", "-Jessica and Guy are the first team out (he's a bit skinny...)")]

screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption('Are You The One?')
pg.display.set_icon(gfx.icon)

def tick():
    # Update frames
    pg.display.update()
    # Limit FPS
    clock.tick(fps)
