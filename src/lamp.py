import numpy as np


boxWidth = 1000
boxHeight = 800
green = (0, 255, 0)
blue = (0, 0, 128)

# create lamp class which will be our creatures
class lamp:
    def __init__(self, color):
        self.x = np.random.randint(0, boxWidth)
        self.y = np.random.randint(0, boxHeight)
        self.xDot = np.random.randint(-5, 5)
        self.yDot = np.random.randint(-5, 5)
        ran = np.random.randint(-10,11)
        if ( ran < 0 ):
            self.color = color
        else:
            self.color= green

    def move(self):
        ran = np.random.randint(-10,11)
        if (ran < 0):
            self.x = self.x + self.xDot
            self.xDot = np.random.randint(-10, 11)
        elif(ran > 0):
            self.y = self.y + self.yDot
            self.yDot = np.random.randint(-10, 11)


