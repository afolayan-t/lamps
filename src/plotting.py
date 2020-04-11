import matplotlib.pyplot as plt
import datetime

simulation_path = "../simulation_data/"

# birth,45,16,12,(0, 255, 0),50.5944619178772
# birth,46,15,12,(255, 0, 0),52.92004895210266
# death,7,53.164345026016235

class Simulation:
    def __init__(self, day, data):
        self.day = day
#        self.time = time
#        self.data = data
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
        #        while#
        
    def parse_simulation(self):
        num_lamps_alive  = int(self.header[2])
        self.num_lamps_alive = 0
        
        for i in range(len(self.data)):
            if 



            
                
    def plotPopulation(self):
        print()
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
print(s.header)
print(s.data)
B
