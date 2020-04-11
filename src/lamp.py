import numpy as np
import matplotlib.pyplot as plt
boxWidth = 1000
boxHeight = 800
green = (0, 255, 0)
blue = (0, 0, 128)
red = (255,0, 0)

res = 1 # grid resolution!
grid_x = np.linspace(0, boxWidth, boxWidth)
grid_y = np.linspace(0, boxHeight, boxHeight)
(XS, YS) = np.meshgrid(grid_x,grid_y)

dt = .5 # Time Step



# create lamp class which will be our creatures
class lamp:
    ### ATTRIBUTES
    #
    #   Static attributes
    #   length, height, maxSpeed, maxEnergy, color, _verticies, stinkRadius
    #   
    #   Dynamic attributes 
    #   position, velocity, force, energy, verticies, scentPoints, stinkField, scentValues 

    #   nomenclature:
    #   scent is what you detect where stink is what you are

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

        self.scentMagnitude = np.zeros([3,3]) # row is nostril, col is rgb
        self.stinkRadius = 5
        self.setVertices()
        self.setScentPoints()
        
        
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
        self.rotate() # also moves scent points

        ## Smell the environment 


        ## Move the sinkfield of the lamp
        self.setStinkField()


    def smell(self, globalStinkField):
        # assign the globalStinkField's rgb values to each nostril

        # allign coordiantes
        for i in range(0, len(self.scentPoints)):
            xMins = XS-self.scentPoints[i,0] # get minimum distance from grid point
            yMins = YS-self.scentPoints[i,1] 
            nearest = xMins**2 + yMins**2
            nearestIndicies= np.where(nearest == np.amin(nearest)) # returns indicies
            self.scentMagnitude[i,:] = globalStinkField[nearestIndicies[0], nearestIndicies[1], :]





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

            ### Rotate the lamp vertices
            self.vertices = np.transpose(np.matmul(rotationMatrix, np.transpose(self._vertices)))
            # put the vertices where the lamp is
            self.vertices = self.vertices + self.position

            ### Rotate scent points
            self.scentPoints = np.transpose(np.matmul(rotationMatrix, np.transpose(self._scentPoints)))
            self.scentPoints = np.floor(self.scentPoints + self.position) # scent needs to be on the grid


    
    def setScentPoints(self):
        ### Set the scent points around the lamp. 
        ### The scent points will be length /2 from the lamps center
        ### There will be N scent points
        ### They will have three channels. 

        ### I wonder the best way to store the values and positions? 
        ### maybe the should be structures? OR dictionaries? 
        ### I should be which ever is easiest to give to Tolu for reinforcement learning

        ### set general scent points
        nScentPoints = 3 # general scent points
        nostralAngle = np.pi/3
        theta = np.linspace(-nostralAngle, nostralAngle, nScentPoints)
        r = (self.height)/2
        scent_x = r*np.cos(theta)
        scent_y = r*np.sin(theta)
        tempCoordaintes = np.transpose(np.array([scent_x, scent_y])) # make each row be a coordinate

        # Rotate each scent by -90 degrees to be coordiante with lamp
        angle = 0# -np.pi/2
        rotationMatrix = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])

        self._scentPoints = np.floor(np.transpose(np.matmul(rotationMatrix, np.transpose(tempCoordaintes))))
        # put us with the current position of the lamp
        self.scentPoints = np.floor(np.add(self._scentPoints, self.position))

    def setStinkField(self):
        # define stink field as a XSxYSx3 array. I.E. an RGB at every coordinate
        # a three dimensional stink field lol

        self.stinkField = np.zeros(np.append(np.array(XS.shape), 3)) # intialize array
        stinkPlane = np.exp(-(1/self.stinkRadius)*(( (XS-self.position[0])**2 + (YS-self.position[1])**2 ) ** (1/2)))
        for i in range(0,3):
            self.stinkField[:,:,i] =  self.color[i] * stinkPlane # magnitude of each scent is the color of the food
        


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

        self.color = (209, 230, 69) # some ugly yellow
        self.stinkRadius = 50 # set stink radius. How far until (1/e) is reached

        self.position = (x_,y_)
        self.height = height
        self.length = length
        self.energy = self.height*self.length/2
        self.setStinkField()

    def setStinkField(self):
        # define stink field as a XSxYSx3 array. I.E. an RGB at every coordinate
        # a three dimensional stink field lol

        self.stinkField = np.zeros(np.append(np.array(XS.shape), 3)) # intialize array
        stinkPlane = np.exp(-(1/self.stinkRadius)*(( (XS-self.position[0])**2 + (YS-self.position[1])**2 ) ** (1/2)))
        for i in range(0,3):
            self.stinkField[:,:,i] =  self.color[i] * stinkPlane # magnitude of each scent is the color of the food




    def respawn(self):
        x = np.random.randint(boxWidth/2, boxWidth)
        y = np.random.randint(0, boxHeight)
        self.position = (x,y)


food_colony = []
totalStink = np.zeros([boxHeight,boxWidth, 3])
for i in range(0, 10):
    food_i = Food()
    food_colony.append(food_i)    
    totalStink = totalStink + food_colony[i].stinkField

np.sum(food_colony[:].totalStink)
myLamp = lamp()
myLamp.move()
myLamp.smell(totalStink)

# fig,ax=plt.subplots(1,1)

# cp = ax.contourf(XS, YS, totalStink[:,:,1])
# fig.colorbar(cp) # Add a colorbar to a plot
# ax.set_title('Filled Contours Plot')
# ax.set_xlabel('x (cm)')
# ax.set_ylabel('y (cm)')
# plt.show()