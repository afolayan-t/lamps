import numpy as np
boxWidth = 1000
boxHeight = 800
green = (0, 255, 0)
blue = (0, 0, 128)
red = (255, 0, 0)

# create lamp class which will be our creatures
class lamp:
    def __init__(self, color=red, x=None, y=None, max_velo=3,
                 length=3, height=9):
        
        self.max_velocity = max_velo

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

        self.length = length
        self.height = height
        
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



class Food:
    def __init__(self, x=None, y=None, height=10, length=10):

        if x == None:
            x_ = np.random.randint(0, boxWidth)
        else:
            x_ = x
        if y == None:
            y_ = np.random.randint(0, boxHeight)
        else:
            y_ = y

        self.position = (x_,y_)
        self.height = height
        self.length = length
        self.energy = self.height*self.length/2

    def respawn(self):
        x = np.random.randint(boxWidth/2, boxWidth)
        y = np.random.randint(0, boxHeight)
        self.position = (x,y)
        
