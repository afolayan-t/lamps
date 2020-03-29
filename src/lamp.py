import numpy as np
import pygame

boxWidth = 1000
boxHeight = 800
green = (0, 255, 0)
blue = (0, 0, 128)

# create lamp class which will be our creatures
class lamp:
    def __init__(self, color):
        self.max_velocity = 3
        
        x = np.random.randint(0, boxWidth)
        y = np.random.randint(0, boxHeight)
        pos = [x,y]
        self.position = np.array(pos)
        
        xDot = np.random.randint(-1, 2)
        yDot = np.random.randint(-1, 2)
        vel = [xDot,yDot]
        self.velocity = np.array(vel)
        
        self.color = color
        self.height = 9
        self.length = 3
        self.energy = 50
        
    def move(self):
        x_force = np.random.randint(-1,2)
        y_force = np.random.randint(-1,2) 
        self.force = [x_force, y_force]
        
        if ((self.velocity[0] + self.force[0])**2 + (self.velocity[1] + self.force[1])**2)**(1/2) < self.max_velocity:
            self.velocity += self.force

        self.position += self.velocity

        self.energy -= np.linalg.norm(self.velocity)/10
        #if self.energy < 0:
         #   print("YOU'RE DEAD, e = ", self.energy)

class Food:
    def __init__(self, heig, leng):
        x = np.random.randint(0, boxWidth)
        y = np.random.randint(0, boxHeight)
        self.position = (x,y)
        self.height = heig
        self.length = leng

    def respawn(self):
        x = np.random.randint(0, boxWidth)
        y = np.random.randint(0, boxHeight)
        self.position = (x,y)
        
