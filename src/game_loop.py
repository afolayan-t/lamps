import numpy as np
from lamp import lamp,Food
from smart_lamp import DQNLamp
import time
import matplotlib.pyplot as plt
import sys
import datetime
import pygame
import pandas as pd
import tensorflow as tf
import random

# Time that we will sleep each iteration
timeStep = .2
# here are some RGB
white = (255, 255, 255) 
green = (0, 255, 0) 
blue = (0, 0, 128) 
red = (255, 0, 0)
black = (0,0,0)

model_path = "/Users/ben/Documents/GitRepos/lamps/models/rev7/"

#if len(sys.argv) == 4: #all arguments present
#     numLamps = int(sys.argv[1])
#     numFoods = int(sys.argv[2])
#     foodResupply = int(sys.argv[3])

# if len(sys.argv) == 3: #2 arguments provided
#     numLamps = int(sys.argv[1])
#     numFoods = int(sys.argv[2])
#     foodResupply = int(input("number of foods per respawn? "))

# if len(sys.argv) == 2: #1 argument present
#     numLamps = int(sys.argv[1])
#     numFoods = int(input("number of foods? "))
#     foodResupply = int(input("number of foods per respawn? "))


# if len(sys.argv) == 1: #no arguments present
#     numLamps = int(input("number of lamps? "))
#     numFoods = int(input("number of foods? "))
#     foodResupply = int(input("number of foods per respawn? "))


# use_pygame = input("Use pygame?? (y/n) ")
# while use_pygame != "y" and use_pygame != "n":
#     print("must reply 'y' or 'n'")
#     use_pygame = input("Use pygame?? (y/n):\n")


class Life:

    def __init__(self, boxWidth_=1000, boxHeight_=800, numLamps_=40, numFoods_=65, foodResupply_=25, usePygame=False):
        # Establish size of environment window#
        self.boxWidth = boxWidth_
        self.boxHeight = boxHeight_

        #### ID NUMBER TO ASSIGN TO LAMPS, WILL BE INCREASED BY WITH EACH NEW LAMP
        self.lamp_ID = 0
        
        #try:
        #    self.numLamps = int(sys.argv[1])
        #    self.numFoods = int(sys.argv[2])
        #    self.foodResupply = int(sys.argv[3])
        #except:
        #    # number of lamps in our colony
        self.numLamps = numLamps_
        self.numFoods = numFoods_
        self.foodResupply = foodResupply_
            
#        use_pygame = input("Use pygame?? (y/n) ")
#        while use_pygame != "y" and use_pygame != "n":
#            print("must reply 'y' or 'n'")
#            use_pygame = input("Use pygame?? (y/n):\n")
            
#        if use_pygame == 'y':
#            self.RUN_PYGAME = True
#        else:
#            self.RUN_PYGAME = False
        try:                                                                                                                                                                                               
           usePygameArg = sys.argv[1]
           if usePygameArg == "pg":
               self.RUN_PYGAME = True
           else:
               self.RUN_PYGAME = False
        except:   
            self.RUN_PYGAME = usePygame
            
            
        if self.RUN_PYGAME:
            # intialize screen object 
            self.screen = pygame.display.set_mode((self.boxWidth, self.boxHeight))
            #background = pygame.Surface((boxWidth, boxHeight))
            self.screen.fill(white)
    
            # sets the title for the window
            pygame.display.set_caption('Environment')

            pygame.init()
    

        ##############################################################################
        # PARAMETERS FOR AI STUFF
        ##############################################################################
        self.actionSpace = [0,1,2,3,4]
        #self.maxSteps = 15000
        self.maxFoodsToEat = 20
        self.done = False
        # to play
#        self.agent = tf.keras.models.load_model(model_path + "episode-886_model_failure.h5")
        # to train
        self.agent = DQNLamp()
        self.current_reward = 0
        self.episode_reward = 0
        self.episode_steps = 0
        self.training = True
        ##############################################################################



        self.lamp_colony = []
        self.food_colony  = []
        self.init_lamps()
        self.init_foods()

        self.init_stinkField()
        
        #### FILE TO WRITE ALL DATA TO
        self.stats_file = self.init_simulation_data()


    def dumpFoods(self):
        for i in range(self.foodResupply):
            food_i = Food()
            self.food_colony.append(food_i)
            self.updateStinkField(food_i.stinkField)
            
            if self.RUN_PYGAME:
                self.renderFood(food_i)

                
    def lampSex(self, parent):
    
        x_ = parent.position[0]
        y_ = parent.position[1]
        velo_buff = 0
        length_buff = 0
        height_buff = 0
        if parent.canMutate:
            velo_buff =  np.random.uniform(low=-parent.max_velocity/3, high=parent.max_velocity/2)
            length_buff = np.random.randint(low=-1, high=3)
            height_buff = np.random.randint(low=-1, high=3)
            
        baby = lamp(ID=self.lamp_ID,
                    color=parent.color,
                    x=x_+2, y=y_+2,
                    max_velo=parent.max_velocity+velo_buff,
                    length=parent.length+length_buff,
                    height=parent.height+height_buff,
                    parent=parent,
                    canMutate_=parent.canMutate
                    )#,isAI_=parent.isAI)    
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
        pygame.draw.rect(self.screen, food.color, (food.position[0], food.position[1], l,h), 0)

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
#        myfont = pygame.font.SysFont('Comic Sans MS', 50)
#        textsurface = myfont.render('LAMPS EXTINCT, GG.', False, (0, 0, 0))
#        display_.blit(textsurface,(self.boxWidth/4,self.boxHeight/2))
        pygame.display.update()
#        time.sleep(3)

    def init_lamps(self):#training=False):
        ### For testing AI
        if self.training:
            lamp_i = lamp(ID=self.lamp_ID, canMutate_=False, isAI_=True,color=blue)
            self.lamp_ID += 1
            self.lamp_colony.append(lamp_i)
            if self.RUN_PYGAME:
                self.renderLamp(lamp_i)
        else:
           for i in range(self.numLamps):    
               if i %2 == 0:
                   lamp_i = lamp(ID=self.lamp_ID)
                   self.lamp_ID += 1
                   self.lamp_colony.append(lamp_i)
               else:
                   lamp_i = lamp(ID=self.lamp_ID, isAI_=True, color=red)
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


    def init_stinkField(self):
        totalStink = np.zeros([self.boxHeight,self.boxWidth])#, 3])
        for i in range(self.numFoods):
            totalStink = totalStink + self.food_colony[i].stinkField
        self.globalStinkField = totalStink

    def updateStinkField(self, food_field):
        self.globalStinkField = np.add(self.globalStinkField, food_field)


    def stepAI(self, lamp, training=False, playing=False):
        """
        stepAI(lamp): this function takes in an AI agent lamp, moves it, analyzes the state
                      and returns this information
        arg: lamp that is an AI
        rerurns:
                -state: array-like, contains lamp energy,x_velo,y_velo,scentMagnitude
                -reward: int, how much reward we give based on its previous actions
                -done:   boolean, is game over?(i.e has lamp taken max steps or died?)
        """

        current_state = [
            lamp.energy,
            lamp.velocity[0],
            lamp.velocity[1],
            lamp.scentMagnitude[0],
            lamp.scentMagnitude[1]
        ]
        self.current_state = np.array(current_state, dtype=np.float32)

#        current_state.reshape(1,self.agent.numStateParameters)
        
        ##### CALL act() function of
        if not playing:
            self.current_action = self.agent.act(self.current_state)
        else:
            self.current_state = np.array([self.current_state])
            prediction_values = np.array(self.agent.predict_on_batch(self.current_state))
            self.current_action = np.argmax(prediction_values)

            
        dE = lamp.move(action=self.current_action)/50
        lamp.smell(self.globalStinkField)

        ### get updated state
        new_state = [
            lamp.energy,
            lamp.velocity[0],
            lamp.velocity[1],
            lamp.scentMagnitude[0],
            lamp.scentMagnitude[1]
        ]
        self.new_state = np.array(new_state, dtype=np.float32)
 #       new_state.reshape(1,self.agent.numStateParameters)
        
        ######## Update reward for:
        # losing energy (add dE/50)
        # dying (subtract 200)
        # eating (add 100)
        # reproducing (add 150)
        # at the wall (subtract 5)
        self.current_reward =  0

        ####### change in energy #######
        self.current_reward += dE
        ################################



        ###### dying ######
        if lamp.energy <= 0:
            self.current_reward -= 200
            self.done = True
        ###################
        ########### beating the round ###########
        if lamp.foods_eaten >= self.maxFoodsToEat:
            #reward += 100 ### we won :D
            print("won")
            self.done = True
        #########################################


    def writeAIStats(self, lamp, playing=False):

        self.episode_steps += 1
        if self.episode_steps >= 13000:
            ### taking too long
#            self.current_reward -= 30
            self.done = True

        if not playing:
            self.agent.remember(self.current_state, self.current_action, self.current_reward, self.new_state, self.done)
            self.agent.replay()

        
        self.episode_reward += self.current_reward

        if lamp.foods_eaten >= self.maxFoodsToEat:
            return True,lamp.foods_eaten
        else:
            return False,lamp.foods_eaten

        
        #### reset reward after each step
        #self.current_reward = 0
        
    def gameLoop(self, training=False, playing=False):
        
        beatGame = False
        
        num_lamps_alive = self.numLamps
        
        self.stats_file.write("greens: " + str(self.numLamps/2) + " reds: " + str(self.numLamps/2))
        self.stats_file.write(" foods: " + str(self.numFoods) + " food regeneration/day: " + str(self.foodResupply)+ "\n\n")

        initial_time = time.time()
        num_iterations = 0
        running = True
        try:
            while running:
                if self.training:
                    if self.done:
                        break
#                time.sleep(.3)
                # reset screen color to white
                if self.RUN_PYGAME:
                    self.screen.fill([255,255,255])
                dead_lamps = []
                # iterate through the lamps
                for i in range(len(self.lamp_colony)):
                    if self.RUN_PYGAME:
                        self.renderLamp(self.lamp_colony[i])

                    # if lamp is an AI, call our step functiton
                    if self.lamp_colony[i].isAI and training:
                        self.stepAI(self.lamp_colony[i], playing=playing)
                    else:
                        # update position of lamp
                        self.lamp_colony[i].move()
                    # iterate through the foods (we should see if we can avoid O(n*m) here)
                    eaten_foods = []
                    for j in range(len(self.food_colony)):
                        if self.RUN_PYGAME:
                            self.renderFood(self.food_colony[j])
                        ## isCollision means that the laamp has eaten
                        if self.isCollision(self.lamp_colony[i], self.food_colony[j]):

                            if self.lamp_colony[i].isAI and training:
                                print("ate, ", self.lamp_colony[i].foods_eaten)
                                self.current_reward += 100
                            
                            self.lamp_colony[i].foods_eaten += 1
                            self.lamp_colony[i].energy += self.food_colony[j].energy
                            eaten_foods.append(self.food_colony[j])
                            
                            if self.lamp_colony[i].energy >= self.lamp_colony[i].maxEnergy:
                                self.lamp_colony[i].energy = self.lamp_colony[i].maxEnergy
    
                            if self.lamp_colony[i].energy >= .8*self.lamp_colony[i].maxEnergy:

                                if self.lamp_colony[i].isAI and training:
                                    print("reproduced")
                                    self.current_reward += 150
                                
                                self.lamp_colony[i].energy *= .5
                                baby = self.lampSex(self.lamp_colony[i])
    
                                now = time.time()
                                time_elapsed = round(now-initial_time, 3)
    
                                ##### WRITE BIRTH TO TXT FILE
                                self.writeLampBirth(baby, time_elapsed)    


                    if self.lamp_colony[i].isAI and training:
                        beatGame,foods_eaten = self.writeAIStats(self.lamp_colony[i],playing=playing)
                        

                    for food_ in eaten_foods:
                        self.updateStinkField(food_.stinkField)
                        self.food_colony.remove(food_)
    
                    if self.lamp_colony[i].energy <= 0:
                        #### WRITE-LAMP–DEATH(lamp_colony[i])
                        ### string to put in txt file for data                                                                     
                        dead_lamps.append(self.lamp_colony[i])
                        
                        # for plotting purposes
    
    
                        now = time.time()
                        time_elapsed = round(now-initial_time, 3)
    
    
                        self.writeLampDeath(self.lamp_colony[i], time_elapsed)
    
    
                            
                for lamp_ in dead_lamps:
                    self.lamp_colony.remove(lamp_)
    
    
                if self.RUN_PYGAME:
                    # if we click 'X' on the screen, stop rendering the screen
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
        
        
                if len(self.lamp_colony) == 0:
                    if self.RUN_PYGAME:
                        self.endGame(self.screen)
                    running = False
        
                num_iterations += 1
                if num_iterations == 400:
                    self.dumpFoods()
                    num_iterations = 0
        
                if self.RUN_PYGAME:
                    pygame.display.update()
    
    #            time.sleep(.2)
        except KeyboardInterrupt:
            print('interrupted!')
            
        if self.RUN_PYGAME:
            pygame.display.quit() # quit the GUI
            
        self.stats_file.write("\n\n")


        if self.training:
            if beatGame and training and (not playing):
                return beatGame, foods_eaten
            elif training and (not playing):
                return beatGame, foods_eaten
        else:
            return False, 0

    def reset(self):
        self.lamp_ID = 0
            
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
        self.init_lamps()
        self.init_foods()

        self.init_stinkField()


        ############## AI STUFF TO RESET #############
        self.episode_reward = 0
        self.episode_steps = 0
        self.done = False
        
def main():


    ####### State information:
    # Energy
    # X-velocity
    # Y-velocity
    # scent magnitude
    #######
    num_episodes = 2000
    total_reward = []
    steps = []
    successes = []
    theGameOfLife = Life(numLamps_=1, numFoods_=50, foodResupply_=0,boxWidth_=1000, boxHeight_=800)
    #### MAKE CHANGES IN gameLoop to handle 
    
    ## to play instead of train:
#    for i in range(10):
#        beatGame,foods_eaten = theGameOfLife.gameLoop(training=True, playing=True)
#        theGameOfLife.reset()

    
    try:    
        for episode in range(num_episodes):
            print("======================================================")
            print("Processing episode: " + str(episode))
            print("======================================================")
            time_start = time.time()
            cur_state = np.array([0,0,0,0])
            beatGame,foods_eaten = theGameOfLife.gameLoop(training=True)
    
            #### update stats
            total_reward.append(theGameOfLife.episode_reward)
            steps.append(theGameOfLife.episode_steps)
            successes.append(beatGame)
            print("--------------------------------------------------------")
            print("Episode: " + str(int(episode)) + " completed in: " + str(theGameOfLife.episode_steps) + " steps.")
            print("--------------------------------------------------------")

            if beatGame:
                print("Successfully completed in episode: " + str(episode) + " with a total reward of: " + str(theGameOfLife.episode_reward))
                theGameOfLife.agent.save_model(model_path + "episode-{}_model_success.h5".format(episode))
            else:
                print("Failed to complete episode: " + str(episode) + " with a total reward of: " + str(theGameOfLife.episode_reward))
                print("We ate " + str(foods_eaten) + " foods")
                if episode % 10 == 0:
                    theGameOfLife.agent.save_model(model_path + "episode-{}_model_failure.h5".format(episode))
                    
            time_end = time.time()
            tf.keras.backend.clear_session()
            print("Processing episode: " + str(episode) + " took: " + str(int(time_end - time_start)) + " seconds. Avg running reward is: " + str(np.array(total_reward)[-100:].mean()))
            
            theGameOfLife.reset()
    
    except KeyboardInterrupt:
            print('interrupted!')

    results_df = pd.DataFrame(total_reward, columns = ['episode_reward'])
    results_df['steps_taken'] = steps
    results_df['Success'] = successes
    results_df['average_running_reward'] = results_df['episode_reward'].rolling(window=100).mean()
#
    results_df.to_csv(model_path+"training_results.csv")
#
    

        
        



    
    
if __name__== "__main__":
  main()
