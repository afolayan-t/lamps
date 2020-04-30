import matplotlib.pyplot as plt
import datetime

simulation_path = "../simulation_data/"

# birth,2.595,13,15,12,(255, 0, 0),3
# death,4.156,11,0

##### SET INDEXES OF BIRTH/DEATH STATS #####
TIME_INDEX = 1
ID_INDEX = 2
LENGTH_INDEX = 3
HEIGHT_INDEX = 4
MAX_VELOCITY_INDEX = 5
COLOR_INDEX = 6
PARENT_ID_INDEX = 7
#####
FOODS_EATEN_INDEX = 3


class Simulation:
    def __init__(self, day, data):
        self.day = day
        self.colors = ["red","green"] # parse this later
        self.init_data(data)
        self.parse_simulation()

        
    def init_data(self, data):
        header = []
        for i in range(len(data)):
            if data[i] == "":
                break
            header.append(data[i])
        self.header = header

        lines_o_data = []
        for i in range(len(header)+1,len(data)):
            if data[i] == "":
                break
            lines_o_data.append(data[i])
        self.data = lines_o_data

    def parse_header(self):
        print()

        
    def parse_simulation(self):
        self.num_lamps_0 = int(self.header[1])
        num_lamps_alive = self.num_lamps_0

        self.lengths = []
        self.heights = []
        self.max_velos = []
        
        self.lamps_alive = []
        self.times = []
        for i in range(len(self.data)):
            line = self.data[i].split(";")
            if line[0] == "death":
                num_lamps_alive -= 1
                self.lamps_alive.append(num_lamps_alive)
                time = line[TIME_INDEX]
                self.times.append(time)
                
            elif line[0] == "birth":
                num_lamps_alive += 1
                self.lamps_alive.append(num_lamps_alive)
                time = line[TIME_INDEX]
                self.times.append(time)

                if line[COLOR_INDEX] == "(0, 255, 0)": ## chNGe to if (canMutate)
                    length = line[LENGTH_INDEX]
                    height = line[HEIGHT_INDEX]
                    max_vel = line[MAX_VELOCITY_INDEX]
                    
                    self.lengths.append(int(length))
                    self.heights.append(int(height))
                    self.max_velos.append(float(max_vel)) 
                
                
    def plotPopulation(self):
        plt.plot(self.times, self.lamps_alive)
        plt.xlabel("time (s)")
        plt.ylabel("lamps")
        plt.show()

    def plotStats(self):
        print("AVG LEN GR ", sum(self.lengths)/len(self.lengths))
        print("AVG HEIGHT GR ", sum(self.heights)/len(self.heights))
        print("AVG LEN GR ", round( sum(self.max_velos)/len(self.max_velos), 3) )
        
        plt.hist(self.lengths)
        plt.ylabel("number of lamps")
        plt.xlabel("Length (pixels)")
        plt.title("Distribution of lenghts")
        plt.show()
        plt.ylabel("number of lamps")
        plt.xlabel("Height (pixels)")
        plt.title("Distribution of heights")
        plt.hist(self.heights)
        plt.show()
        plt.hist(self.max_velos)
        plt.ylabel("number of lamps")
        plt.xlabel("max velo")
        plt.title("Distribution of max velos")
        plt.show()
        
    def plotGreen2dHistogram(self):
        print()
        
        
class Day:
    def __init__(self, date):
        self.date = date
        self.datafile = open(simulation_path + str(self.date) + ".txt", "r")
        self.data  = self.datafile.readlines()
        for i in range(len(self.data)):
            self.data[i] = self.data[i].strip('\n')
        self.simulation_times = self.getTimes()
        
    def getTimes(self):
        sim_times = []
        for i in range(len(self.data)):
            line = self.data[i].strip('\n')
            if line == "Start of simulation":
                timeline = self.data[i+1]#.strip('\n')
                time = timeline.split()[1]
                sim_times.append(time)
        return sim_times
    
    def plotLastSimulation(self):
        """ plots a the last simulation """
        num_times = len(self.simulation_times)
        last_time = self.simulation_times[num_times-1]
        plotSimulation(last_time)

    def getSimulationData(self, time):
        sim_data = []
        i = 0
        while i < len(self.data):
            if(time in self.data[i]):
                break
            i += 1
            
        while i < len(self.data):
            if(self.data[i] == "Start of simulation"):
                break
            sim_data.append(self.data[i])
            i += 1
        return sim_data


    
date = datetime.date.today()
d = Day(date)
#simulation_data = d.getSimulationData(d.simulation_times[0])
simulation_data = d.getSimulationData(d.simulation_times[len(d.simulation_times)-1])

s = Simulation(d, simulation_data)

s.plotPopulation()

s.plotStats()
