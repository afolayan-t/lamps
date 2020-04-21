import numpy as np
from lamp import lamp,Food
import time
import matplotlib.pyplot as plt
import sys
import datetime
import pygame

# Time that we will sleep each iteration
timeStep = .2
# here are some RGB
white = (255, 255, 255) 
green = (0, 255, 0) 
blue = (0, 0, 128) 
red = (255, 0, 0)
black = (0,0,0)



class Life:

    def __init__(self, boxWidth_=1000, boxHeight_=800):
        # Establish size of environment window#
        self.boxWidth = boxWidth_
        self.boxHeight = boxHeight_

        #### ID NUMBER TO ASSIGN TO LAMPS, WILL BE INCREASED BY WITH EACH NEW LAMP
        self.lamp_ID = 0
        
        try:
            self.numLamps = int(sys.argv[1])
            self.numFoods = int(sys.argv[2])
            self.foodResupply = int(sys.argv[3])
        except:
            # number of lamps in our colony
            self.numLamps = int(input("number of lamps? "))
            self.numFoods = int(input("number of foods? "))
            self.foodResupply = int(input("number of foods per respawn? "))
            
        use_pygame = input("Use pygame?? (y/n) ")
        while use_pygame != "y" and use_pygame != "n":
            print("must reply 'y' or 'n'")
            use_pygame = input("Use pygame?? (y/n):\n")
            
        if use_pygame == 'y':
            self.RUN_PYGAME = True
        else:
            self.RUN_PYGAME = False
            
            
        if self.RUN_PYGAME:
            # intialize screen object 
            self.screen = pygame.display.set_mode((self.boxWidth, self.boxHeight))
            #background = pygame.Surface((boxWidth, boxHeight))
            self.screen.fill(white)
    
            # sets the title for the window
            pygame.display.set_caption('Environment')

            pygame.init()
    
        self.lamp_colony = []
        self.food_colony  = []

        #### FILE TO WRITE ALL DATA TO
        self.stats_file = self.init_simulation_data()

    def dumpFoods(self, n):
        for i in range(n):
            food_i = Food()
            self.food_colony.append(food_i)
            if self.RUN_PYGAME:
                self.renderFood(food_i)
        
    def lampSex(self, parent):
    
        x_ = parent.position[0]
        y_ = parent.position[1]
        velo_buff = 0
        length_buff = 0
        height_buff = 0
        if parent.color == green:
            velo_buff =  np.random.uniform(low=-parent.max_velocity/3, high=parent.max_velocity/2)
            length_buff = np.random.randint(low=-1, high=3)
            height_buff = np.random.randint(low=-1, high=3)
            
        baby = lamp(ID=self.lamp_ID,
                    color=parent.color,
                    x=x_+2, y=y_+2,
                    max_velo=parent.max_velocity+velo_buff,
                    length=parent.length+length_buff,
                    height=parent.height+height_buff,
                    parent=parent)    
        self.lamp_ID += 1
    
        if baby.length <= 0:
            baby.length = 1
        if baby.max_velocity <= 0:
            baby.max_velocity = parent.max_velocity
        self.lamp_colony.append(baby)
        return baby
        
    def renderLamp(self, lamp):
        """
        A function for rendering a lamp on the screen
        args:
        lamp - the lamp to be rendered
        display - the display on which to render our lamp
        """
        l = lamp.length
        h = lamp.height
        
        #print("Lamp verticies:", lamp.vertices)
        pygame.draw.polygon(self.screen, lamp.color, lamp.vertices)
        
        # This draws the direction of the velocity vectors
#        pygame.draw.line(self.screen, black, lamp.position, lamp.position + lamp.velocity*20) 
        
        # draw the scent points for each lamp

 #       for i in range(0,3):
  #          x = int(lamp.scentPoints[i,0])
   #         y = int(lamp.scentPoints[i,1])
    #        pygame.draw.circle(self.screen, blue, (x,y), int(np.floor(lamp.height/4)))
            #        pygame.draw.rect(screen, lamp.color, (lamp.position[0], lamp.position[1], l, h), 0)

    def renderFood(self, food):
        h = food.height
        l = food.length
        pygame.draw.rect(self.screen, blue, (food.position[0], food.position[1], l,h), 0)

    def isCollision(self, obj1, obj2):
        #(x1, y1) = obj1.position
        (x2, y2) = obj2.position
        

        # subVerts are the vertices of the lamp shade
        # a lamp will only eat a food if one of these verticies touches food
        subVerts = obj1.vertices[0:4]

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

    def endGame(self, display_):
        display_.fill([255,255,255])
        myfont = pygame.font.SysFont('Comic Sans MS', 50)
        textsurface = myfont.render('LAMPS EXTINCT, GG.', False, (0, 0, 0))
        display_.blit(textsurface,(self.boxWidth/4,self.boxHeight/2))
        pygame.display.update()
        time.sleep(3)

    def init_lamps(self):
            
        for i in range(self.numLamps):
            if i % 2 == 0:
                lamp_i = lamp(ID=self.lamp_ID, color=green)
                self.lamp_ID += 1
                self.lamp_colony.append(lamp_i)
            else:
                lamp_i = lamp(ID=self.lamp_ID, color=red)
                self.lamp_ID += 1
                self.lamp_colony.append(lamp_i)
            if self.RUN_PYGAME:
                self.renderLamp(self.lamp_colony[i])

    def init_foods(self):
        for j in range(self.numFoods):
            food_i = Food()
            self.food_colony.append(food_i)
            if self.RUN_PYGAME:
                self.renderFood(self.food_colony[j])

    def init_simulation_data(self):
        simulation_path = "../simulation_data/"
        date = datetime.date.today()
        stats_file = open(simulation_path + str(date)+".txt", "a")
        
        date_time = datetime.datetime.now()
        stats_file.write("Start of simulation\n")
        stats_file.write(str(date_time)+"\n")
        stats_file.write(str(self.numLamps)+"\n")
        return stats_file
    

    def writeLampBirth(self, lamp, tob):
        """
        arg- tob: time of birth
        """
        ##### write lamp data to the txt file
        birth_string_to_write = "birth;"
        birth_string_to_write += (str(tob) + ";")
        birth_string_to_write += (str(lamp.ID) + ";")
        birth_string_to_write += (str(lamp.length) + ";")
        birth_string_to_write += (str(lamp.height) + ";")
        birth_string_to_write += (str(lamp.max_velocity) + ";")
        birth_string_to_write += (str(lamp.color) + ";")
        if lamp.parent == None:
            birth_string_to_write += "None"
        else:
            birth_string_to_write += str(lamp.parent.ID)    
            birth_string_to_write += "\n"
        self.stats_file.write(birth_string_to_write)
            

    def writeLampDeath(self, lamp, tod):
        """                                                                                                                                                                                            
        arg- tob: time of death                                                                                                                                                                        
        """
        death_string_to_write = "death;"
        death_string_to_write += (str(tod) + ";")
        death_string_to_write += (str(lamp.ID) + ";")
        death_string_to_write += str(lamp.foods_eaten)
        death_string_to_write += "\n"
        self.stats_file.write(death_string_to_write)
        


def main():

    theGameOfLife = Life(boxWidth_=1000, boxHeight_=800)
    
    theGameOfLife.init_lamps()
    theGameOfLife.init_foods()

    initial_time = time.time()
    
    num_lamps_alive = theGameOfLife.numLamps
        
    theGameOfLife.stats_file.write("greens: " + str(theGameOfLife.numLamps/2) + " reds: " + str(theGameOfLife.numLamps/2))
    theGameOfLife.stats_file.write(" foods: " + str(theGameOfLife.numFoods) + " food regeneration/day: " + str(theGameOfLife.foodResupply)+ "\n\n")

    num_iterations = 0
    running = True
    try:
        while running:
            # reset screen color to white
            if theGameOfLife.RUN_PYGAME:
                theGameOfLife.screen.fill([255,255,255])
            dead_lamps = []
            # iterate through the lamps
            for i in range(len(theGameOfLife.lamp_colony)):
                if theGameOfLife.RUN_PYGAME:
                    theGameOfLife.renderLamp(theGameOfLife.lamp_colony[i])
                # update position of lamp
                theGameOfLife.lamp_colony[i].move()
                # iterate through the foods (we should see if we can avoid O(n*m) here)
                eaten_foods = []
                for j in range(len(theGameOfLife.food_colony)):
                    if theGameOfLife.RUN_PYGAME:
                        theGameOfLife.renderFood(theGameOfLife.food_colony[j])
                    if theGameOfLife.isCollision(theGameOfLife.lamp_colony[i], theGameOfLife.food_colony[j]):
                        theGameOfLife.lamp_colony[i].foods_eaten += 1
                        
                        if theGameOfLife.lamp_colony[i].energy >= theGameOfLife.lamp_colony[i].maxEnergy:
                            theGameOfLife.lamp_colony[i].energy = theGameOfLife.lamp_colony[i].maxEnergy

                        if theGameOfLife.lamp_colony[i].energy >= .8*theGameOfLife.lamp_colony[i].maxEnergy:
                            ### string to put in txt file for data

                            
                            theGameOfLife.lamp_colony[i].energy *= .5
                            baby = theGameOfLife.lampSex(theGameOfLife.lamp_colony[i])

                            


                            now = time.time()
                            time_elapsed = round(now-initial_time, 3)

                            ##### WRITE BIRTH TO TXT FILE
                            theGameOfLife.writeLampBirth(baby, time_elapsed)

                            
                        theGameOfLife.lamp_colony[i].energy += theGameOfLife.food_colony[j].energy
                        eaten_foods.append(theGameOfLife.food_colony[j])

                        
                for food_ in eaten_foods:
                    theGameOfLife.food_colony.remove(food_)

                if theGameOfLife.lamp_colony[i].energy <= 0:
                    #### WRITE-LAMP–DEATH(lamp_colony[i])
                    ### string to put in txt file for data                                                                     
                    dead_lamps.append(theGameOfLife.lamp_colony[i])
                    
                    # for plotting purposes


                    now = time.time()
                    time_elapsed = round(now-initial_time, 3)


                    theGameOfLife.writeLampDeath(theGameOfLife.lamp_colony[i], time_elapsed)


                        
            for lamp_ in dead_lamps:
                theGameOfLife.lamp_colony.remove(lamp_)


            if theGameOfLife.RUN_PYGAME:
                # if we click 'X' on the screen, stop rendering the screen
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
    
    
            if len(theGameOfLife.lamp_colony) == 0:
                if theGameOfLife.RUN_PYGAME:
                    theGameOfLife.endGame(theGameOfLife.screen)
                running = False
    
            num_iterations += 1
            if num_iterations == 400:
                theGameOfLife.dumpFoods(theGameOfLife.foodResupply)
                num_iterations = 0
    
            if theGameOfLife.RUN_PYGAME:
                pygame.display.update()

#            time.sleep(.2)
    except KeyboardInterrupt:
        print('interrupted!')




        

    if theGameOfLife.RUN_PYGAME:
        pygame.display.quit() # quit the GUI

if __name__== "__main__":
  main()
