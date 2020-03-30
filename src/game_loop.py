import numpy as npo
from lamp import lamp,Food
import pygame
import time
import matplotlib.pyplot as plt

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
numLamps = 100
numFoods = 25
# sets the title for the window
pygame.display.set_caption('Environment') 


def renderLamp(lamp, display):
        """
        A function for rendering a lamp on the screen
        args:
        lamp - the lamp to be rendered
        display - the display on which to render our lamp
        """
        l = lamp.length
        h = lamp.height
        pygame.draw.rect(display, lamp.color, (lamp.position[0], lamp.position[1], l, h), 0)

def renderFood(food, display):
        h = food.height
        l = food.length
        pygame.draw.rect(display, blue, (food.position[0], food.position[1], l,h), 0)

def isCollision(obj1, obj2):
    (x1, y1) = obj1.position
    (x2, y2) = obj2.position
    if(x1 >= x2 and x1 <= x2+obj2.length) or (x1+obj1.length >= x2 and x1+obj1.length <= x2+obj2.length):
        if(y1 >= y2 and y1 <= y2+obj2.height) or (y1+obj1.height >= y2 and y1+obj1.height <= y2+obj2.height):
            return True
    return False

def endGame(display_):
    display_.fill([255,255,255])
    myfont = pygame.font.SysFont('Comic Sans MS', 50)
    textsurface = myfont.render('LAMPS EXTINCT, GG.', False, (0, 0, 0))
    display_.blit(textsurface,(boxWidth/4,boxHeight/2))
    pygame.display.update()
    time.sleep(3)


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

    food_colony = []
    for j in range(numFoods):
        food_i = Food(10, 10)
        food_colony.append(food_i)
        renderFood(food_colony[j], screen)
        

    num_lamps_alive = numLamps
    initial_time = time.time()
    lamps_alive  = []
    times  = []
    
    running = True    
    while running:
        # reset screen color to white
        screen.fill([255,255,255])
        
        dead_lamps = []
        for i in range(len(lamp_colony)):
            lamp_colony[i].move()
            renderLamp(lamp_colony[i], screen)
            for j in range(len(food_colony)):
                    renderFood(food_colony[j], screen)
                    if isCollision(lamp_colony[i], food_colony[j]):
                            food_colony[j].respawn()
                            lamp_colony[i].energy += 50
            if lamp_colony[i].energy <= 0:
                dead_lamps.append(lamp_colony[i])

                # for plotting purposes
                num_lamps_alive -= 1 
                lamps_alive.append(num_lamps_alive)
                now = time.time()
                times.append(now-initial_time)
                
        for lamp_ in dead_lamps:
                lamp_colony.remove(lamp_)

        # if we click 'X' on the screen, stop rendering the screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if len(lamp_colony) == 0:
            endGame(screen)
            running = False            
        pygame.display.update()
        # pause the window so the graphics update
#        time.sleep(timeStep/8)


    pygame.display.quit() # quit the GUI

    plt.plot(times, lamps_alive)
    plt.show()

  
if __name__== "__main__":
  main()
