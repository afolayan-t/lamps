import numpy as np
import matplotlib.pyplot as plt
import math

boxWidth = 1000
boxHeight = 800
green = (0, 255, 0)
blue = (0, 0, 128)
red = (255,0, 0)


res = 1 # grid resolution!
grid_x = np.linspace(0, boxWidth, boxWidth)
grid_y = np.linspace(0, boxHeight, boxHeight)
(XS, YS) = np.meshgrid(grid_x,grid_y)

dt = 1 # Time Step



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

    def __init__(self, ID=0, parent=None, color=red, x=None, y=None, max_velo=2,
                 length=15, height=12, canMutate_=False, isAI_=False):

        ### boolean value corresponding to whether or not the lamp is an AI or not
        ### if isAI is False, it will do random walks
        self.isAI = isAI_
        self.canMutate = canMutate_
        
        self.max_velocity = max_velo

    
        self.ID = ID
        self.foods_eaten = 0
        self.steps_taken = 0
        self.parent = parent


        #### for if we are stuck at a wall; 0 = not at wall
        #### 1 = top, 2 = bottom, 3 = left, 4 = right
        if self.isAI:
            self.at_wall = 0
        
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
        vel = [self.max_velocity,0]#[xDot,yDot]
        self.velocity = np.array(vel)

        if self.canMutate:
            self.color = green
        elif self.isAI:
            self.color = blue
        else:
            self.color = color
            
        self.length = length
        self.height = height

        self.mass =  .4*self.length*( (.2*self.length + .5*self.height)/2 )
        
        self.maxEnergy = self.length*self.height
        self.energy = self.maxEnergy*.8

        self.nScentPoints = 2 # general scent points
        self.scentMagnitude = np.zeros([2])#np.zeros([3,3]) # row is nostril, col is rgb
        self.stinkRadius = 5


        self.setVertices()
        self.setScentPoints()

        self.sight_range = 160 # can evolve
        self.eye_position = np.zeros([2,2])
        self.eye_position[0,:] = np.flip(self._lampFrameVertices[1]) # oriente along y-axis
        self.eye_position[1,:] = np.flip(self._lampFrameVertices[2])
        
        self.num_nearest_seen_foods = 1
        self.nearest_food_displacements = np.zeros((self.num_nearest_seen_foods, 2))
        self.sight_righteye = np.array([0,0])
        self.sight_lefteye = np.array([0,0])
        self.sight_vector = np.array([0,0])
        self.nearest_food_coordinates = np.array([boxWidth/2,boxHeight/2])
        
    def move(self, action=0):
        """
            args: action
            action: integer [0,4] which corresponds to which action will be called if the lamp is an AI agent
                0: do nothing
                1: speed up
                2: speed down
                3: apply force left
                4: apply force right
        """
        ### get current velocity to pass to rotate()
        oldVelocity = self.velocity

#        if self.isAI:

#            if action == 0: # do nothing
#                force = [0,0]
#            elif action == 1: # speed up
#                force = self.speedUp(1)
#            elif action == 2: # slow down
#                force = self.speedDown(1)
#            elif action == 3: # turn left
#                force = self.turnLeft(1)
#            elif action == 4: # turn right
#                force = self.turnRight(1)
        
        if self.isAI:

            if action == 0: # do nothing
                force = [0,0]
            elif action == 1: # turn left
                force = self.turnLeft(1)
            elif action == 2: # turn right
                force = self.turnRight(1)

        else:
            x_force = np.random.randint(-1,2)
            y_force = np.random.randint(-1,2) 
            force = [x_force, y_force]
            
        self.force = np.array(force)
        
        #        if ((self.velocity[0] + self.force[0]*dt)**2 + (self.velocity[1] + self.force[1]*dt)**2)**(1/2) < self.max_velocity:
        
        self.velocity = self.velocity + self.force*dt
        self.velocity = self.max_velocity*self.velocity/np.linalg.norm(self.velocity)

        f = 800 ### constant to dock energy by
        dE = -(self.mass*(np.linalg.norm(self.velocity))**2)/f - dt/50 ## last term so that lamp dies if it stops
        self.energy +=  dE

        ### Make verticies such that they are around the origin of the lamp
        updown = np.random.random() - .5
        leftright = np.random.random() - .5
        if leftright < 0:
            self.position[0] = int(self.position[0] + self.velocity[0]*dt)
        else:
            self.position[0] = math.ceil(self.position[0] + self.velocity[0]*dt)
        if updown < 0:
            self.position[1] = int(self.position[1] + self.velocity[1]*dt)
        else:
            self.position[1] = math.ceil(self.position[1] + self.velocity[1]*dt)
        
        ### make lamps spawn at other side of the box
        if self.position[0] >= boxWidth: #### right
            self.position[0] = boxWidth
            self.velocity[0] *= -1
            self.at_wall = 4
        elif self.position[0] <= 0:
            self.position[0] = 0
            self.velocity[0] *= -1
            self.at_wall = 3
        elif self.position[1] >= boxHeight:
            self.position[1] =  boxHeight
            self.velocity[1] *= -1
            self.at_wall = 2
        elif self.position[1] <= 0:
            self.position[1] = 0
            self.velocity[1]  *= -1
            self.at_wall = 1
        else:
            self.at_wall = 0
            
        self.steps_taken += 1
        
        ## rotate the lamp
        self.rotate() # also moves scent points

        if self.isAI:
            ### AI's need this info for reward
            return dE
            ###### Set state vecotor
            ###### state vector consists of 4 elements:
            ###### energy, x_velocity, y_velocity, scent_magnitude
            #print(self.steps_taken)
            
        

    def speedUp(self, magnitude):
 #       if self.at_wall == 0:
        unit_vel = self.velocity/np.linalg.norm(self.velocity)
        force = magnitude*unit_vel
 #       elif self.at_wall == 1: ### top wall
 #           force = [0,-1]
 #           force = [x*magnitude for x in force]
 #       elif self.at_wall == 2: ### bottom wall
 #           force = [0,1]
 #           force = [x*magnitude for x in force]
 #       elif self.at_wall == 3: ### left wall
 #           force = [-1,0]
 #           force = [x*magnitude for x in force]
 #       elif self.at_wall == 4: ### right wall
 #           force = [1,0]
        force = [x*magnitude for x in force]
        return force
    
    
    def speedDown(self, magnitude):
        unit_vel = self.velocity/np.linalg.norm(self.velocity)
        angle_to_push = np.pi
        rot_mat = self.getRotationMatrix(angle_to_push)
        dot = magnitude*np.dot(unit_vel, rot_mat)
        new_force = [dot[0,0],dot[0,1]]
        return new_force
    
    def turnLeft(self, magnitude):
        unit_vel = self.velocity/np.linalg.norm(self.velocity)
        angle_to_push = np.pi/2
        rot_mat = self.getRotationMatrix(angle_to_push)
        dot = magnitude*np.dot(unit_vel, rot_mat)
        new_force = [dot[0,0],dot[0,1]]
        return new_force
    
    def turnRight(self, magnitude):
        unit_vel = self.velocity/np.linalg.norm(self.velocity)
        angle_to_push = -np.pi/2
        rot_mat = self.getRotationMatrix(angle_to_push)
        dot = magnitude*np.dot(unit_vel, rot_mat)
        new_force = [dot[0,0],dot[0,1]]
        return new_force


    def getRotationMatrix(self, radians):
        c,s = np.cos(radians),np.sin(radians)
        rot_mat = np.matrix([[c,-s],[s,c]])
        return rot_mat

    def limit_food_search(self, food_colony):
        
        food_coordinates = np.array([food.position for food in food_colony])
        # np.array(food_colony.position)
        # define limits

        # rotate limits of scent
        eye_theta = np.arctan(self.eye_position[1,0]/self.eye_position[1,1])
        # print('eye_theta left eye', (180/np.pi)*eye_theta)
        rotation_matrix = np.array([[np.cos(eye_theta), -np.sin(eye_theta)], [np.sin(eye_theta), np.cos(eye_theta)]])
        self.sight_vector = np.array([self.sight_range, 0])
        sight_lefteye = np.matmul(rotation_matrix, self.sight_vector)
        eye_theta = -eye_theta
        rotation_matrix = np.array([[np.cos(eye_theta), -np.sin(eye_theta)], [np.sin(eye_theta), np.cos(eye_theta)]])
        sight_righteye = np.matmul(rotation_matrix, self.sight_vector)
        # put eye vectors in gameloop frame
        third_component = -self.velocity[1] # cross prod with unit vector
        lamp_frame_angle =  np.arccos(np.dot([1, 0], self.velocity/np.linalg.norm(self.velocity)))
        # this comes from the cross product to see if w rotate clwwise or cnt clckwise
        if third_component > 0:
            lamp_frame_angle *= -1
        rotation_matrix = np.array([[np.cos(lamp_frame_angle), -np.sin(lamp_frame_angle)],[np.sin(lamp_frame_angle), np.cos(lamp_frame_angle)]])
        sight_lefteye = np.matmul(rotation_matrix, sight_lefteye)
        sight_righteye = np.matmul(rotation_matrix, sight_righteye)
        # put in game_loop reference frame
        self.sight_lefteye = sight_lefteye
        self.sight_righteye = sight_righteye
        sight_lefteye = sight_lefteye + self.position
        sight_righteye = sight_righteye + self.position
        # definte limits for range in which to serach for foods
        limit_left = np.min([self.position[0], sight_lefteye[0], sight_righteye[0]])
        limit_right = np.max([self.position[0], sight_lefteye[0], sight_righteye[0]])
        limit_top = np.max([self.position[1], sight_lefteye[1], sight_righteye[1]])
        limit_bottom = np.min([self.position[1], sight_lefteye[1], sight_righteye[1]])
        leftrighttopbottom = np.array([limit_left, limit_right, limit_top, limit_bottom])
        # select foods in list 
        horizontal_indices = (limit_left<food_coordinates[:,0]) & (food_coordinates[:,0]<limit_right)
        vertical_indices = (limit_bottom<food_coordinates[:,1]) & (food_coordinates[:,1]<limit_top)
        reduced_food_indicies= vertical_indices & horizontal_indices
        reduced_food_coordiantes = food_coordinates[reduced_food_indicies]
        return reduced_food_coordiantes

    def see_food(self, food_colony): 

        reduced_food_list= self.limit_food_search(food_colony)
        # print('num foods in bounding box: ', reduced_food_list.shape[0])
        self.nearest_food_displacements = np.zeros((self.num_nearest_seen_foods, 2)) # reset to zeros
        # check if any food is entered
        n_to_check = reduced_food_list.shape[0]
        if len(reduced_food_list) > 0:
            self.nearest_food_coordinates = reduced_food_list[0]
        else:
            self.nearest_food_coordinates = np.array([boxWidth/2,boxHeight/2])#np.array([0,0])
            
        if n_to_check > 0:
            # print('eye position:', self.eye_position)
            eye_theta = np.arctan(self.eye_position[1,0]/self.eye_position[1,1])
            # print('eye theta:', eye_theta)
            reduced_food_lamped_centered = reduced_food_list - self.position # foods in2 lamp frame
            
            distances = np.sqrt(np.sum(reduced_food_lamped_centered**2,axis=1))
            dist_indx = distances.argsort()
            # print('food position in in game frame: ', reduced_food_list[dist_indx[0]])
            mag_lamp_center = np.linalg.norm(reduced_food_lamped_centered, axis=1)
            mag_lamp_center_matrix = np.ones([reduced_food_lamped_centered.shape[0],2])
            mag_lamp_center_matrix[:,0] = mag_lamp_center
            mag_lamp_center_matrix[:,1] = mag_lamp_center
            norm_food_lamped_centered = reduced_food_lamped_centered/mag_lamp_center_matrix
            # print('norm_food_lamped_centered: ', norm_food_lamped_centered)
            food_angular_displacements =np.arccos(np.dot(norm_food_lamped_centered, self.velocity/np.linalg.norm(self.velocity)))

            # print('food_angular_displacements', (180/np.pi)*food_angular_displacements)
            # check if less than radial distance away and if within sight angle
            saw_foods_indx = (food_angular_displacements < eye_theta) & (distances < self.sight_range)
            # print('num close enough:' , sum((distances < self.sight_range)))
            # print('num angle enough: ', sum((food_angular_displacements < 2*eye_theta)))
            # check if any are seen
            if any(saw_foods_indx)==True:
                # update nNearest to be the at most nNearest 
                if sum(saw_foods_indx) < self.num_nearest_seen_foods:
                    num_saw_foods = sum(saw_foods_indx)
                else:
                    num_saw_foods = self.num_nearest_seen_foods
                # reduce count
                saw_foods = reduced_food_lamped_centered[saw_foods_indx]
                # rank list by distance 
                saw_distances = distances[saw_foods_indx]
                sorted_nearest_indxs = saw_distances.argsort()
                # sort by nearest
                sorted_nearest_foods = saw_foods[sorted_nearest_indxs[:num_saw_foods]]
                for i in range(num_saw_foods):
                    self.nearest_food_displacements[i,:] = sorted_nearest_foods[i,:]


    
    def smell(self, globalStinkField):
        
        for i in range(0,self.nScentPoints):
            x_eval = int(self.scentPoints[i,0])
            y_eval = int(self.scentPoints[i,1])
            if self.scentPoints[i,0] >= boxWidth: 
                x_eval = boxWidth-1
            if self.scentPoints[i,0] <= 0:
                x_eval = 0
            if self.scentPoints[i,1] >= boxHeight:
                y_eval = boxHeight-1
            if self.scentPoints[i,1] <= 0:
                y_eval = 0
            self.scentMagnitude[i] = globalStinkField[y_eval, x_eval]

            
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

            ### Create rotation matrix
            rotationMatrix = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])

            ### Rotate the lamp vertices
            self.vertices = np.transpose(np.matmul(rotationMatrix, np.transpose(self._lampFrameVertices)))
            # put the vertices where the lamp is
            self.vertices = self.vertices + self.position

            ### Rotate scent points
            self.scentPoints = np.transpose(np.matmul(rotationMatrix, np.transpose(self._lampFrameScentPoints)))
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
        nostralAngle = np.pi/4
        theta = np.linspace(-nostralAngle, nostralAngle, self.nScentPoints)
        r = (self.height)/3
        scent_x = r*np.cos(theta)
        scent_y = r*np.sin(theta)
        tempCoordaintes = np.transpose(np.array([scent_x, scent_y])) # make each row be a coordinate

        # Rotate each scent by -90 degrees to be coordiante with lamp
        angle = 0# -np.pi/2
        rotationMatrix = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])

        self._lampFrameScentPoints = np.floor(np.transpose(np.matmul(rotationMatrix, np.transpose(tempCoordaintes))))
        # put us with the current position of the lamp
        self.scentPoints = np.floor(np.add(self._lampFrameScentPoints, self.position))

#    def setStinkField(self):
    #     # define stink field as a XSxYSx3 array. I.E. an RGB at every coordinate
    #     # a three dimensional stink field lol

        #               self.stinkField = np.zeros(np.append(np.array(XS.shape), 3)) # intialize array
        #stinkPlane = np.exp(-(1/self.stinkRadius)*(( (XS-self.position[0])**2 + (YS-self.position[1])**2 ) ** (1/2)))
        #for i in range(0,3):
        #    self.stinkField[:,:,i] =  self.color[i] * stinkPlane # magnitude of each scent is the color of the food

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
        self.vertices = np.add(vertices, self.position) # 
        self._lampFrameVertices = vertices # lamp frame verticies 


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
        stinkPlane = np.exp(-(1/self.stinkRadius)*(( (XS-self.position[0])**2 + (YS-self.position[1])**2 )  ** (1/2)))
        self.stinkField = self.color[0]*stinkPlane
        # set boundaries of stink field equal to zero
        self.stinkField[0,:] = 0
        self.stinkField[-1,:] = 0
        self.stinkField[:,0] = 0
        self.stinkField[:,-1] = 0





    def respawn(self):
        x = np.random.randint(boxWidth/2, boxWidth)
        y = np.random.randint(0, boxHeight)
        self.position = (x,y)
