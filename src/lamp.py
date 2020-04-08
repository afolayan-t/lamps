import numpy as np
<<<<<<< HEAD
import matplotlib.pyplot as plt


=======
>>>>>>> 03bb1569bebc5d5561f09f5bc728e3cd5cf36523
boxWidth = 1000
boxHeight = 800
green = (0, 255, 0)
blue = (0, 0, 128)
<<<<<<< HEAD
dt = 1 # global variable and essentially parameter
=======
red = (255,0, 0)

dt = 1 # Time Step
>>>>>>> 03bb1569bebc5d5561f09f5bc728e3cd5cf36523

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
<<<<<<< HEAD
    def __init__(self, color, x=None, y=None):
        ### this will be developed further to evolve with evolution
        self.max_velocity = 3
=======
    def __init__(self, color=red, x=None, y=None, max_velo=3,
                 length=15, height=12):
        
        self.max_velocity = max_velo
>>>>>>> 03bb1569bebc5d5561f09f5bc728e3cd5cf36523

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
        
<<<<<<< HEAD
        ### rndly generate velocity upon lamp creation
        xDot = np.random.randint(-1, 2)
        yDot = np.random.randint(-1, 2)
        vel = [xDot,yDot]
        self.velocity = np.array(vel)
        
        self.color = color
        self.length = 10
        self.height = 10
        # set the verticies, which are dependent on the widthand length
        self.setVerticies()

=======
        xDot = np.random.randint(-2,3)#()-.5#(-1, 2)
        yDot = np.random.randint(-2,3)#()-.5#(-1, 2)
        vel = [0,-1]#[xDot,yDot]
        self.velocity = np.array(vel)
        
        self.color = color
>>>>>>> 03bb1569bebc5d5561f09f5bc728e3cd5cf36523

        self.length = length
        self.height = height
        
        self.maxEnergy = self.length*self.height
        self.energy = self.maxEnergy/2

<<<<<<< HEAD
        
    def move(self):
        # how the force is generated will have to update once we have learning implimented
        x_force = np.random.rand() - 0.5
        y_force = np.random.rand() - 0.5
        self.force = np.array([x_force, y_force])
        oldVel = self.velocity # store old velocity for lamp rotation

        ### see if new velocity is less than the max vel
        tempVel = np.add(self.velocity, self.force*dt)
        if np.sqrt(np.sum(np.square(tempVel))) < self.max_velocity:
            self.velocity = tempVel

        oldPosition = self.position
        self.position = self.position + self.velocity*dt
        newPosition = self.position

        # print("Change in position:", newPosition - oldPosition)

        self.energy -= np.linalg.norm(self.velocity)/20
        # rotate the lamp so it can be rendered
        #self.rotate(oldVel)
        #if self.energy < 0:
         #   print("YOU'RE DEAD, e = ", self.energy)
=======
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
        self.vertices = np.add(self.vertices, -self.position)
        self.position = self.position + self.velocity*dt

        ## rotate the lamp
        self.rotate(oldVelocity)
        ## Re-add position to the vertices so that they're at the location of the lamp
        self.vertices = np.add(self.vertices, self.position)





    def rotate(self, oldVel):
        # (1) Get unit vector of the velocity for direction
        # (2) Get the rotation matrix


        # GET UNIT VECTOR
        magV = np.linalg.norm(self.velocity)
        magOldVel = np.linalg.norm(oldVel)
        if self.velocity.all() == oldVel.all():
            angle = 0
        elif (magV == 0) or (magOldVel == 0):
            print("one of vels has 0 mag")
            angle = 0
        elif np.dot(oldVel, self.velocity)/(magV*magOldVel) > 1:
            print("ROUNDING ERROR!!!!!!!")
            angle = 0

        else:
            third_component = oldVel[0]*self.velocity[1] - oldVel[1]*self.velocity[0]
            
            angle =  np.arccos(np.dot(oldVel, self.velocity)/(magV*magOldVel))
            
            if third_component < 0:
                angle *= -1




        ### Create rotation matrix
        rotationMatrix = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])

        self.vertices = np.transpose(np.matmul(rotationMatrix, np.transpose(self.vertices)))

        

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
        self.vertices = np.add(vertices, self.position)

>>>>>>> 03bb1569bebc5d5561f09f5bc728e3cd5cf36523

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
        a = self.height/2                # half the base of the lamp shade
        c = shadeHeight*self.length     # the widthof the shade
        e = (1-shadeHeight)*self.length # height of pole
        verticies = np.array([[a,0], [c/2, c], [-c/2, c], [-a,0], [-sliver, 0], [-sliver, -e], [-c/4, -e], [-c/4, -e-sliver], [c/4, -e-sliver], [c/4, -e], [sliver, -e], [sliver,0]])
        self.verticies = np.add(verticies, self.position)

    def rotate(self, oldVel): #(position, velocity, verticies):
        ### (1) get unit vector for velocity to obtain the direction
        ### (2) create rotation matrix matrix 
        ### (3) apply transformation to verticies
        ### (4) return transformed verticies

        ### Get unit vector and angle with x-axis
        magV = np.linalg.norm(self.velocity) 
        magOldVel = np.linalg.norm(oldVel)
        if (magV == 0) or (magOldVel == 0):
            angle = 0
        elif np.dot(oldVel, self.velocity)/(magV*magOldVel) > 1:
            print("!!!!", np.dot(oldVel, self.velocity)/(magV*magOldVel))
            print("dot prod:", np.dot(oldVel, self.velocity))
            print("oldVel:", oldVel)
            print("self.velocity:", self.velocity)
            print("MagV=", magV)
            print("MagOldVel=", magOldVel)
            angle = 0
        else:
            angle = np.arccos(np.dot(oldVel, self.velocity)/(magV*magOldVel)) # dotproduct with x-axis picks x component


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
        
# red = (255, 0, 0)
# myLamp = lamp(red)

# print("Velocity 1:", myLamp.velocity)
# print("position 1:", myLamp.position)
# plt.fill(myLamp.verticies[:,0], myLamp.verticies[:,1])

# myLamp.move()
# print("Velocity 2:", myLamp.velocity)
# print("position 2:", myLamp.position)
# plt.fill(myLamp.verticies[:,0], myLamp.verticies[:,1])


# myLamp.move()
# print("Velocity 3:", myLamp.velocity)
# print("position 3:", myLamp.position)
# plt.fill(myLamp.verticies[:,0], myLamp.verticies[:,1])

# myLamp.move()
# print("Velocity 4:", myLamp.velocity)
# print("position 4:", myLamp.position)
# plt.fill(myLamp.verticies[:,0], myLamp.verticies[:,1])


# plt.xlim(-100, 100)
# plt.ylim(-100, 100)
# plt.show()


#### THERE IS AN ISSUE WITH THE IMPLIMENTATION OF THE ROTATION MATRIX/
#### Each time I'm finding the angle with respect to the x-axis instead of the pervious velocity vector
#### I either need to find a different way to impliment the rotation, maybe within move()
#   Or I will have to keep the orignial shape and just rotate that every single time.
####    I will tink after the walk