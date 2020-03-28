import numpy as npo
from lamp import lamp
import pygame
import time

# Establish size of environment window#
boxWidth = 1000
boxHeight = 800
# Time that we will sleep each iteration
timeStep = .2
# here are some RGB
white = (255, 255, 255) 
green = (0, 255, 0) 
blue = (0, 0, 128) 
red = (255, 0, 0)
# number of lamps in our colony
numLamps = 2000

# sets the title for the window
pygame.display.set_caption('Environment') 


def renderLamp(lamp, display):
        """
        A function for rendering a lamp on the screen
        args:
        lamp - the lamp to be rendered
        display - the display on which to render our lamp
        """
        pygame.draw.rect(display, lamp.color, (lamp.x, lamp.y, 9,3), 0)

def main():

    pygame.init()
    # intialize screen object 
    screen = pygame.display.set_mode((boxWidth, boxHeight))
    background = pygame.Surface((boxWidth, boxHeight))
    screen.fill(pygame.Color(white))

    lamp_colony = []
    greens = 0
    reds = 0
    for i in range(numLamps):
        lamp_i  = lamp(red)
        lamp_colony.append(lamp_i)
        renderLamp(lamp_colony[i], screen)

    running = True
    
    while running:
        # reset screen color to white
        screen.fill([255,255,255])

        # iterate through lamps, move them, and plot them
        for i in range(len(lamp_colony)):
            lamp_colony[i].move()
            renderLamp(lamp_colony[i], screen)
            
        # if we click 'X' on the screen, stop rendering the screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        
        pygame.display.update()
        # pause the window so the graphics update
        time.sleep(timeStep)

    pygame.display.quit() # quit the GUI
        


  
if __name__== "__main__":
  main()
