import numpy as np


boxWidth = 1000
boxHeight = 800
green = (0, 255, 0)
blue = (0, 0, 128)

# create lamp class which will be our creatures
class lamp:
    def __init__(self, color, x=None, y=None):
        self.max_velocity = 3

        if x == None:
            x_ = np.random.randint(0, boxWidth)
        else:
            x_ = x
        if y == None:
            y_ = np.random.randint(0, boxHeight)
        else:
            y_ = y
        pos = [x_,y_]
        self.position = np.array(pos)
        
        xDot = np.random.randint(-1, 2)
        yDot = np.random.randint(-1, 2)
        vel = [xDot,yDot]
        self.velocity = np.array(vel)
        
        self.color = color
        self.height = 9
        self.length = 3

        self.maxEnergy = self.length*self.height*5
        self.energy = self.maxEnergy/2
        
    def move(self):
        x_force = np.random.randint(-1,2)
        y_force = np.random.randint(-1,2) 
        self.force = [x_force, y_force]
        
        if ((self.velocity[0] + self.force[0])**2 + (self.velocity[1] + self.force[1])**2)**(1/2) < self.max_velocity:
            self.velocity += self.force

        self.position += self.velocity

        self.energy -= np.linalg.norm(self.velocity)/20
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
        x = np.random.randint(boxWidth/2, boxWidth)
        y = np.random.randint(boxHeight/2, boxHeight)
        self.position = (x,y)
        
