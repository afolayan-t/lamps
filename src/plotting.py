import matplotlib.pyplot as plt
import datetime

simulation_path = "../simulation_data/"

# birth green 4.78020977973938
# birth red 5.061302900314331
# birth green 5.430384874343872
# death green 5.9920477867126465
# death red 6.09492301940918
# death red 6.13077187538147
# birth red 6.8851330280303955
# birth green 7.54793381690979
# birth green 8.059895038604736
# birth green 9.479753971099854

class Simulation:
    def __init__(self, day, data):
        self.day = day
        self.time = time
        self.data = data
        self.header = getHeader()
        
    def plotPopulation():
        print()
    def plotGreen2dHistogram():
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
simulation_data = d.getSimulationData(d.simulation_times[0])
print(simulation_data)

