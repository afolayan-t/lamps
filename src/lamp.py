import numpy as np
import matplotlib.pyplot as plt


boxWidth = 50
boxHeight = 50
green = (0, 255, 0)
blue = (0, 0, 128)

# create lamp class which will be our creatures

### Sal will change things here and add many comments.


#### THE LAMP CLASS:
####    the subjects of study of whom will evolve with time
####    PROPERTIES
####
####    the properties that change upon sex
####        max_velocity        =   scalar
####        scent               =   [1x3] numpy array
####        olfactory           =   [1x3] numpy array
####        olfactoryDetection  =   [8x2] numpy array
####        size                =   [1x2] numpy array [length , width]
####        max_energy          =   scalar, length * width * const
####
####    The proerties that do not change upon sex
####        position    =   [1x2]   numpy array    
####        velocity    =   [1x2]   numpy array
####        force       =   [1x2]   numpy array
####        verticies   =   [2x12]  numpy array
####        energy      =   scalar
####
####    METHODS
####        move()
####        rotate()
####        getVerticies()
####
####        sex()

class lamp:
    def __init__(self, color, x=None, y=None):
        ### this will be developed further to evolve with evolution
        self.max_velocity = 3

        ### x,y are optional for intialization. 
        ### if a lamp comes from sex that it will inherrit positition from the parents
        ### otherwise, generate random coordinates
        if x == None:
            x_ = np.random.randint(-boxWidth, boxWidth)
        else:
            x_ = x
        if y == None:
            y_ = np.random.randint(-boxHeight, boxHeight)
        else:
            y_ = y
        pos = [x_,y_]
        self.position = np.array(pos)
        
        ### rndly generate velocity upon lamp creation
        xDot = np.random.randint(-1, 2)
        yDot = np.random.randint(-1, 2)
        vel = [xDot,yDot]
        self.velocity = np.array(vel)
        
        self.color = color
        self.length = 9
        self.width = 3
        # set the verticies, which are dependent on the widthand length
        self.setVerticies()


        self.maxEnergy = self.length*self.width*5
        self.energy = self.maxEnergy/2

        
    def move(self):
        # how the force is generated will have to update once we have learning implimented
        x_force = np.random.randint(-1,2)
        y_force = np.random.randint(-1,2) 
        self.force = np.array([x_force, y_force])

        # we will also have to figure out a dt? Maybe a paramter analysis. For now:
        dt = .1
        tempVel = np.add(self.velocity, self.force*dt)
        

        if np.sqrt(np.sum(np.square(tempVel))) < self.max_velocity:
            self.velocity = tempVel

        oldPosition = self.position
        self.position = self.position + self.velocity*dt
        newPosition = self.position

        print("Change in position:", newPosition - oldPosition)

        self.energy -= np.linalg.norm(self.velocity)/20
        # rotate the lamp so it can be rendered
        self.rotate()
        #if self.energy < 0:
         #   print("YOU'RE DEAD, e = ", self.energy)

    def setVerticies(self):
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
        a = self.width/2                # half the base of the lamp shade
        c = shadeHeight*self.length     # the widthof the shade
        e = (1-shadeHeight)*self.length # height of pole
        verticies = np.array([[a,0], [c/2, c], [-c/2, c], [-a,0], [-sliver, 0], [-sliver, -e], [-c/4, -e], [-c/4, -e-sliver], [c/4, -e-sliver], [c/4, -e], [sliver, -e], [sliver,0]])
        self.verticies = np.add(verticies, self.position)

    def rotate(self): #(position, velocity, verticies):
        ### (1) get unit vector for velocity to obtain the direction
        ### (2) create rotation matrix matrix 
        ### (3) apply transformation to verticies
        ### (4) return transformed verticies

        ### Get unit vector and angle with x-axis
        magV = np.linalg.norm(self.velocity)
        angle = np.arccos(self.velocity[0]/magV) # dotproduct with x-axis picks x component
        print("Rotation angle:", angle*(180/np.pi))
        ### Create rotation matrix
        rotationMatrix = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])

        ### Center verticies in its own coordinate system
        centeredVerts = self.verticies - self.position

        ### Rotate lamp's verticies. [2x8] = [2x2] x transpose([8x2]) 
        rotatedVerts = np.matmul(rotationMatrix, np.transpose(centeredVerts))
        rotatedVerts = np.transpose(rotatedVerts)

        ### Put lamp back it is current position
        newVerts = np.add(rotatedVerts, self.position)
        self.verticies = newVerts
        
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
        
red = (255, 0, 0)
myLamp = lamp(red)
myLamp.move()

plt.xlim(-100, 100)
plt.ylim(-100, 100)

plt.fill(myLamp.verticies[:,0], myLamp.verticies[:,1])
print("position 1:", myLamp.position)
print('Verticies 1:', myLamp.verticies)
myLamp.move()
plt.fill(myLamp.verticies[:,0], myLamp.verticies[:,1])
print("position 2:", myLamp.position)
print('Verticies 2:', myLamp.verticies)

myLamp.move()
plt.fill(myLamp.verticies[:,0], myLamp.verticies[:,1])
print("position 3:", myLamp.position)
myLamp.move()
plt.fill(myLamp.verticies[:,0], myLamp.verticies[:,1])
print("position 4:", myLamp.position)
plt.show()


#### THERE IS AN ISSUE WITH THE IMPLIMENTATION OF THE ROTATION MATRIX/
#### Each time I'm finding the angle with respect to the x-axis instead of the pervious velocity vector
#### I either need to find a different way to impliment the rotation, maybe within move()
#   Or I will have to keep the orignial shape and just rotate that every single time.
####    I will tink after the walk