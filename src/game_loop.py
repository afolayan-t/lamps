import numpy as np
from lamp import lamp,Food
import time
import matplotlib.pyplot as plt
import sys


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
black = (0,0,0)



try:
    numLamps = int(sys.argv[1])
    numFoods = int(sys.argv[2])
    foodResupply = int(sys.argv[3])
except:
    # number of lamps in our colony
    numLamps = int(input("number of lamps? "))
    numFoods = int(input("number of foods? "))
    foodResupply = int(input("number of foods per respawn? "))

use_pygame = input("Use pygame?? (y/n) ")
while use_pygame != "y" and use_pygame != "n":
    print("must reply 'y' or 'n'")
    use_pygame = input("Use pygame?? (y/n):\n")

if use_pygame == 'y':
    RUN_PYGAME = True
else:
    RUN_PYGAME = False

    
if RUN_PYGAME:
    import pygame
    # intialize screen object 
    screen = pygame.display.set_mode((boxWidth, boxHeight))
    background = pygame.Surface((boxWidth, boxHeight))
    screen.fill(white)
    
    # sets the title for the window
    pygame.display.set_caption('Environment')

    pygame.init()
    
lamp_colony = []
food_colony  = []


def dumpFoods(n):
    for i in range(n):
        food_i = Food()
        food_colony.append(food_i)
        if RUN_PYGAME:
            renderFood(food_i)
        
def lampSex(parent):
    x_ = parent.position[0]
    y_ = parent.position[1]
    velo_buff = 0
    length_buff = 0
    if parent.color == green:
        velo_buff =  np.random.uniform(low=-parent.max_velocity/3, high=parent.max_velocity/3)
        length_buff = np.random.randint(low=-2, high=3)
        
    baby = lamp(color=parent.color,
                x=x_+2, y=y_+2,
                max_velo=parent.max_velocity+velo_buff,
                length=parent.length+length_buff,
                height=parent.height)    

    if baby.length <= 0:
        baby.length = 1
    if baby.max_velocity <= 0:
        baby.max_velocity = parent.max_velocity
    lamp_colony.append(baby)
    return baby
        
def renderLamp(lamp):
        """
        A function for rendering a lamp on the screen
        args:
        lamp - the lamp to be rendered
        display - the display on which to render our lamp
        """
        l = lamp.length
        h = lamp.height

        #print("Lamp verticies:", lamp.vertices)
        pygame.draw.polygon(screen, lamp.color, lamp.vertices)

        # This draws the direction of the velocity vectors
        pygame.draw.line(screen, black, lamp.position, lamp.position + lamp.velocity*20) 

        # draw the scent points for each lamp

        for i in range(0,3):
            x = int(lamp.scentPoints[i,0])
            y = int(lamp.scentPoints[i,1])
            pygame.draw.circle(screen, blue, (x,y), int(np.floor(lamp.height/4)))
#        pygame.draw.rect(screen, lamp.color, (lamp.position[0], lamp.position[1], l, h), 0)

def renderFood(food):
        h = food.height
        l = food.length
        pygame.draw.rect(screen, blue, (food.position[0], food.position[1], l,h), 0)

def isCollision(obj1, obj2):
   #(x1, y1) = obj1.position
    (x2, y2) = obj2.position

    try:
        subVerts = obj1.vertices[0:4]
    except:
        print("object 1 must be a lamp")

    for i in range(len(subVerts)):
        x1 = subVerts[i][0]
        y1 = subVerts[i][1]

        if (x1 >= x2 and x1 <= x2+obj2.length):
            if(y1 >= y2 and y1 <= y2+obj2.height):
                return True
    
    ### Code for if lamp is rectangle: ###
#    if(x1 >= x2 and x1 <= x2+obj2.length) or (x1+obj1.length >= x2 and x1+obj1.length <= x2+obj2.length):
 #       if(y1 >= y2 and y1 <= y2+obj2.height) or (y1+obj1.height >= y2 and y1+obj1.height <= y2+obj2.height):
  #          return True
    return False

def endGame(display_):
    display_.fill([255,255,255])
    myfont = pygame.font.SysFont('Comic Sans MS', 50)
    textsurface = myfont.render('LAMPS EXTINCT, GG.', False, (0, 0, 0))
    display_.blit(textsurface,(boxWidth/4,boxHeight/2))
    pygame.display.update()
    time.sleep(3)

def init_lamps():
    for i in range(numLamps):
        if i % 2 == 0:
            lamp_i = lamp(green)
        else:
            lamp_i = lamp(red)
        lamp_colony.append(lamp_i)
        if RUN_PYGAME:
            renderLamp(lamp_colony[i])

def init_foods():
    for j in range(numFoods):
        food_i = Food()
        food_colony.append(food_i)
        if RUN_PYGAME:
            renderFood(food_colony[j])


def main():

    init_lamps()
    init_foods()

    
    num_lamps_alive = numLamps
    initial_time = time.time()
    lamps_alive  = []
    times  = []

    num_greens = numLamps/2
    greens_alive = []
    green_times = []
    num_reds = numLamps/2
    reds_alive = []
    red_times = []

    num_iterations = 0
    running = True
    try:
        while running:
            # reset screen color to white
            if RUN_PYGAME:
                screen.fill([255,255,255])
    
            dead_lamps = []
            dead_greens = []
            dead_reads = []
            # iterate through the lamps
            for i in range(len(lamp_colony)):
                if RUN_PYGAME:
                    renderLamp(lamp_colony[i])
                # update position of lamp
                lamp_colony[i].move()
                eaten_foods = []
                # iterate through the foods (we should see if we can avoid O(n*m) here)
                for j in range(len(food_colony)):
                    if RUN_PYGAME:
                        renderFood(food_colony[j])
                    if isCollision(lamp_colony[i], food_colony[j]):
    
                        if lamp_colony[i].energy >= lamp_colony[i].maxEnergy:
                            lamp_colony[i].energy = lamp_colony[i].maxEnergy

                        if lamp_colony[i].energy >= .8*lamp_colony[i].maxEnergy:
                            lamp_colony[i].energy *= .5
                            baby = lampSex(lamp_colony[i])
    
                            num_lamps_alive += 1
                            lamps_alive.append(num_lamps_alive)
                            now = time.time()
                            times.append(now-initial_time)
                            if baby.color == green:
                                num_greens += 1
                                greens_alive.append(num_greens)
                                green_times.append(now-initial_time)
                            elif baby.color == red:
                                num_reds += 1
                                reds_alive.append(num_reds)
                                red_times.append(now-initial_time)
                                    
                        lamp_colony[i].energy += food_colony[j].energy
                        eaten_foods.append(food_colony[j])        
    
                for food_ in eaten_foods:
                    food_colony.remove(food_)
     
                            
                if lamp_colony[i].energy <= 0:
                    dead_lamps.append(lamp_colony[i])
    
                    # for plotting purposes
                    num_lamps_alive -= 1
                    lamps_alive.append(num_lamps_alive)
                    now = time.time()
                    times.append(now-initial_time)
    
                    if lamp_colony[i].color == green:
                        num_greens -= 1
                        greens_alive.append(num_greens)
                        green_times.append(now-initial_time)
                    elif lamp_colony[i].color == red:
                        num_reds -= 1
                        reds_alive.append(num_reds)
                        red_times.append(now-initial_time)
                    
            for lamp_ in dead_lamps:
                lamp_colony.remove(lamp_)
    
            if RUN_PYGAME:
                # if we click 'X' on the screen, stop rendering the screen
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
    
    
            if len(lamp_colony) == 0:
                if RUN_PYGAME:
                    endGame(screen)
                running = False
    
            num_iterations += 1
            if num_iterations == 400:
                dumpFoods(foodResupply)
                num_iterations = 0
    
            if RUN_PYGAME:
                pygame.display.update()

#            time.sleep(.2)
    except KeyboardInterrupt:
        print('interrupted!')




        

    if RUN_PYGAME:
        pygame.display.quit() # quit the GUI

    if num_greens > 0:
        avg_len_gr = 0
        avg_max_v_gr = 0
        for gr in lamp_colony:
            if gr.color == green:
                avg_len_gr += gr.length
                avg_max_v_gr += gr.max_velocity
            
        avg_len_gr /= num_greens
        avg_max_v_gr /= num_greens
        
        print("avg length of greens: ", avg_len_gr)
        print("avg top speed of greens: ", avg_max_v_gr)
        
    plt.plot(times, lamps_alive)
    plt.plot(green_times, greens_alive, color='green')
    plt.plot(red_times, reds_alive, color='red')
    plt.xlabel("time (s)")
    plt.ylabel("lamps")
    plt.show()

  
if __name__== "__main__":
  main()
