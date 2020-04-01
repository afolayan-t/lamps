import numpy as npo
from lamp import lamp,Food
import time
import matplotlib.pyplot as plt

# number of lamps in our colony
numLamps = 4000
numFoods = 15
red = (255,0,0)
blue = (0,0,128)


def isCollision(obj1, obj2):
    (x1, y1) = obj1.position
    (x2, y2) = obj2.position
    if(x1 >= x2 and x1 <= x2+obj2.length) or (x1+obj1.length >= x2 and x1+obj1.length <= x2+obj2.length):
        if(y1 >= y2 and y1 <= y2+obj2.height) or (y1+obj1.height >= y2 and y1+obj1.height <= y2+obj2.height):
            return True
    return False


def main():

    lamp_colony = []
    for i in range(numLamps):
        lamp_i  = lamp(red)
        lamp_colony.append(lamp_i)

    food_colony = []
    for j in range(numFoods):
        food_i = Food(10, 10)
        food_colony.append(food_i)
        
    num_lamps_alive = numLamps
    initial_time = time.time()
    lamps_alive  = []
    times  = []
    
    running = True    
    while running:
        
        dead_lamps = []
        for i in range(len(lamp_colony)):
            lamp_colony[i].move()
            for j in range(len(food_colony)):
                    if isCollision(lamp_colony[i], food_colony[j]):
                            food_colony[j].respawn()
                            lamp_colony[i].energy += 50
            if lamp_colony[i].energy <= 0:
                dead_lamps.append(lamp_colony[i])
                
                # for plotting purposes
                num_lamps_alive -= 1
                lamps_alive.append(num_lamps_alive)
                now = time.time()
                times.append(now-initial_time)
                print(num_lamps_alive)
                
        for lamp_ in dead_lamps:
                lamp_colony.remove(lamp_)

        if len(lamp_colony) == 0:
            running = False            



    plt.plot(times, lamps_alive)
    plt.show()

  
if __name__== "__main__":
  main()
B
