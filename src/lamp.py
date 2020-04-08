import numpy as np
boxWidth = 1000
boxHeight = 800
green = (0, 255, 0)
blue = (0, 0, 128)
red = (255,0, 0)

dt = .5 # Time Step

# create lamp class which will be our creatures
class lamp:
    def __init__(self, color=red, x=None, y=None, max_velo=3,
                 length=30, height=25):
        
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
        
        xDot = np.random.randint(-2,3)#()-.5#(-1, 2)
        yDot = np.random.randint(-2,3)#()-.5#(-1, 2)
        vel = [0,-1]#[xDot,yDot]
        self.velocity = np.array(vel)
        
        self.color = color

        self.length = length
        self.height = height
        
        self.maxEnergy = self.length*self.height
        self.energy = self.maxEnergy/2

        self.setVertices()
        
        
    def move(self):
        
        ### get current velocity to pass to rotate()
        oldVelocity = self.velocity
        
        x_force = np.random.randint(-1,2)
        y_force = np.random.randint(-1,2) 
        force = [x_force, y_force]
        self.force = np.array(force)
        
        if ((self.velocity[0] + self.force[0]*dt)**2 + (self.velocity[1] + self.force[1]*dt)**2)**(1/2) < self.max_velocity:
            self.velocity = self.velocity + self.force*dt

        self.energy -= np.linalg.norm(self.velocity)/20



        ### Make verticies such that they are around the origin of the lamp
        self.position = self.position + self.velocity*dt

        ## rotate the lamp
        self.rotate()





    def rotate(self):
        # (1) Get unit vector of the velocity for direction
        # (2) Get the rotation matrix


        # GET UNIT VECTOR
        magV = np.linalg.norm(self.velocity)
        
        # IF THERE IS NO VELOCITY VECTOR THEN WE DON'T ROTATE
        if (magV > 0):
            xAxis = np.array([1 ,0])
            dotProd = np.dot(self.velocity, xAxis)
            third_component = -self.velocity[1] # cross prod with unit vector
            
            angle =  np.arccos(np.dot(xAxis, self.velocity)/(magV))
            # this comes from the cross product to see if w rotate clwwise or cnt clckwise
            if third_component > 0:
                angle *= -1
            print("velocity: ", self.velocity)
            print("Dot Product:", dotProd)
            print("Angle: ", angle)
            ### Create rotation matrix
            rotationMatrix = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
            self.vertices = np.transpose(np.matmul(rotationMatrix, np.transpose(self._vertices)))
            # put the vertices where the lamp is
            self.vertices = self.vertices + self.position
        

    def setVertices(self):
        ###                  _
        ###      *---*      |
        ###     /c/2  \     c
        ###    /       \    |
        ###   /    --a--\   -
        ###       ||
        ###       ||  e
        ###       ||
        ###     ====== c/4
        shadeHeight= .4                # proportion of how much of lamp is shade
        sliver = self.length/50         # width of pole and base
        a = self.height/2                # half the base of the lamp shade
        c = shadeHeight*self.length     # the widthof the shade
        e = (1-shadeHeight)*self.length # height of pole
        vertices = np.array([[a,0], [c/2, c], [-c/2, c], [-a,0], [-sliver, 0], [-sliver, -e], [-c/4, -e], [-c/4, -e-sliver], [c/4, -e-sliver], [c/4, -e], [sliver, -e], [sliver,0]])
        angle = -np.pi/2

        rotationMatrix = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
        vertices = np.transpose(np.matmul(rotationMatrix, np.transpose(vertices)))
        self.vertices = np.add(vertices, self.position)
        self._vertices = vertices

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
