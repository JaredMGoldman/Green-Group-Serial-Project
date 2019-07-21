import appJar as aj
import pickle
from enum import Enum
import numpy as np
import time
import csv

class Controller:
    """
    Controller of MVC format

    Saves user data, runs experiment and downloads files
    """
    def __init__(self):
        
        self.__activePorts = {}         # Active MFC ports (1,2,3,...)
        
        self.__time_points = []         # Time measurements to be saved in csv

        self.__pressure_points = []     # Pressure measurements to be saved in csv

        self.__flow_points = []         # Flow rate measurements to be saved in csv

        self.__save_list = list()       # Used when loading or saving experiemental setup

        self.__gas_dex = {}
        #### Experimental Information ####
        
        self.__pressureCtrlBool = False
        
        self.__MFCBehaviorList = list() 

        self.__pressureBehaviorList = list()

        self.__cycle = 0

        self.__cycleLength = 0

        self.__slaveBehaviorList = list()

        #### Experimental Information ####

        self.__start = 0.0

        self.__correctionKey = {
            "Actylene": 0.58, "Air": 1.00, "Ammonia": 0.73, 
            "Argon": 1.39, "Arsine": 0.67, "Boron Trichloride": 0.41, 
            "Bromine": 0.81, "Carbon Dioxide": 0.70, 
            "Carbon Monoxide": 1.00, "Carbon Tetrachloride": 0.31, 
            "Carbon Tetraflouride": 0.42, "Chlorine": 0.86, 
            "Chlorodifluoromethane": 0.46, "Chloropentafluoroethane": 0.24, 
            "Cyanogen": 0.61, "Deuterium": 1.00, "Diborane": 0.44, 
            "Dibromodifluoromethane": 0.19, "Dichlorodifluoromethane": 0.35, 
            "Dichlorofluoromethane": 0.42, "Dichloromethysilane": 0.25, 
            "Dichlorosilane": 0.40, "Dichlorotetrafluoroethane": 0.22, 
            "Difluoroethylene": 0.43, "Dimethylpropane": 0.22, 
            "Ethane": 0.50, "Fluorine": 0.98, "Fluoroform": 0.50, 
            "Freon - 11": 0.33, "Freon - 12": 0.35, "Freon - 13": 0.38, 
            "Freon - 14": 0.42, "Freon - 21": 0.42, "Freon - 22": 0.46, 
            "Freon - 23": 0.50, "Freon - 113": 0.20, "Freon - 114": 0.22, 
            "Freon - 115":0.24 , "Freon - 116":0.24, "Freon - C318":0.164, 
            "Freon - 1132A":0.43, "Helium":1.45, "Hexafluoroethane":0.24,
            "Hydrogen": 1.01, "Hydrogen Bromide":1.00, 
            "Hydrogen Chloride":1.00, "Hydrogen Fluoride":1.00, 
            "Isobutylene":0.29, "Krypton":1.54, "Methane":0.72, 
            "Methyl Fluoride":0.56, "Molybdenum Hexafluoride":0.21, 
            "Neon":1.46, "Nitric Oxide":0.99, "Nitrogen":1.00, 
            "Nitrogen Dioxide":0.74, "Nitrogen Trifluoride":0.48, 
            "Nitrous Oxide":0.71, "Octafluorocyclobutane":0.164, 
            "Oxygen":1.00, "Pentane":0.21, "Perfluoropropane":0.17, 
            "Phosgene":0.44, "Phosphine":0.76, "Propane":0.36, 
            "Propylene":0.41, "Silane":0.60, 
            "Silicon Tetrachloride": 0.28, "Silicon Tetrafluoride":0.035,
            "Sulfur Dioxide":0.69, "Sulfur Hexafluoride":0.26, 
            "Trichlorofluoromethane":0.33, "Trichlorosilane":0.33, 
            "Tungsten Hexafluoride":0.25, "Xenon":1.32}
        
        
    def setActivePorts(self, dictionary):
        self.__activePorts = dictionary

    def setNumberOfCycles(self, cycle):
        """
        conventional setter for number of cycles in experiment
        """
        self.__cycle = cycle

    def setCycleLength(self, duration):
        """
        conventional setter for length of cycles in experiment in minutes
        """
        self.__cycleLength = duration

    def setPressureBool(self, bool):
        """
        conventional setter for independent experimental variable
        """
        self.__pressureCtrlBool = bool

    def setMFCBehaviorList( 
        self,gas=None,port=None,behavior=None,start_time=None, 
        end_time = None, magnitude0 = None, 
        magnitude1= None, oscillations= None
        ):
        """
        conventional setter for behavior of a gas
        """
        [port] = port
        self.__MFCBehaviorList.append([port,gas,behavior, 
            start_time, end_time, magnitude0, 
            magnitude1, oscillations])

    def setPressureBehaviorList(
        self, behavior, start_time, end_time, 
        magnitude0, magnitude1, oscillations
        ):
        """
        conventional setter for behavior of pressure in experiment
        """
        self.__pressureBehaviorList.append([behavior, start_time, 
            end_time, magnitude0, magnitude1, 
            oscillations])

    def setSlaveList(self, slave_bool, port_id, master_id, ratio):
        """
        conventional setter for  slave status and behavior
        """
        self.__slaveBehaviorList.append([slave_bool, port_id, master_id, ratio])

    
    def beginExperiment(self):
        """
        experimental start

        determines slave status to ensure proper experimental setup of instument
        designed to update setpoints and datapoints every 5 seconds
        """
        for port in self.__activePorts.keys():
            if self.__activePorts[port] != None:
                self.__gas_dex[len(self.__flow_points)] = port
                self.__flow_points.append([])
        
        # for port in self.__slaveBehaviorList:
        #     if port[0]:
        #         make port = port[1] a slave with ratio and master id given

        #         print('slave functionality')
        
        self.__start = time.time()
        total_time = time.time()-self.__start
        while total_time <= self.__cycle * self.__cycleLength * 60:
            time.sleep(0.5)
            self.dataUpdate()
            self.setpointUpdate()
            total_time = time.time()-self.__start
            minutes = int(total_time/60)
            seconds = int(total_time % 60)
            print("Total time: " + str(minutes) +":" + str(seconds))
            print(str(int(total_time*10/(self.__cycle * self.__cycleLength * 6))) + " percent complete\n")
        print("Big Work")
        self.endExperiment()


    def __createSaveList(self):
        """
        prepares experimental setup information to be exported
        """
        self.__save_list = [[self.__pressureCtrlBool, self.__cycle, self.__cycleLength]]
        self.__save_list.append(self.__pressureBehaviorList)
        self.__save_list.append(self.__MFCBehaviorList)
        self.__save_list.append(self.__slaveBehaviorList)
        self.__save_list.append(self.__activePorts)

    def __parseData(self):
        """
        reads experimental setup information from a file 
        and translates it into usable info
        """
        self.__pressureCtrlBool = self.__save_list[0][0]
        self.__cycle = self.__save_list[0][1]
        self.__cycleLength = self.__save_list[0][2]
        self.__pressureBehaviorList = self.__save_list[1]     
        self.__MFCBehaviorList = self.__save_list[2]
        self.__slaveBehaviorList = self.__save_list[3]
        self.__activePorts = self.__save_list[4]

    def saveData(self, location):
        """
        Saves experimental setup created through 'Custom' UI
        """
        self.__createSaveList()
        with open(location, 'wb') as filehandle:  
            pickle.dump(self.__save_list, filehandle)


    def loadData (self, location):
        """
        Loads experimental setup previously created through 'Custom' UI
        """
        with open(location, 'rb') as filehandle:  
            self.__save_list = pickle.load(filehandle)
        self.__parseData()

    def static (self, magnitude):
        """
        Constant relationship of gas flow/pressure as a function of time 
        used to set next setpoint
        """
        return magnitude

    def linear (self, start, end, mag0, mag1, t):
        """
        Linear relationship of gas flow/pressure as a function of time 
        used to set next setpoint
        """
        
        p0 = mag0 
        p1 = mag1 


        slope = ((p1 - p0)/ ((end-start)*60.0))* t
        y_int = p0 - ((p1-p0)/((end-start)*60.0)) * start

        return slope + y_int

    def exponential (self, start, end, mag0, mag1, t):
        """
        Exponential relationship of gas flow/pressure as a function of time 
        used to set next setpoint
        """
        p0 = mag0 
        p1 = mag1 
    
        tot = (end-start)*60.0
        r = (np.log(p1)-np.log(p0))/(tot)
        a = p0*np.exp(-r*tot)

        return a*np.exp(r*t)

    def periodic (self, start, end, mag0, mag1, oscl, t):
        """
        Periodic relationship of gas flow/pressure as a function of time 
        used to set next setpoint
        """
        p0 = mag0
        p1 = mag1

        amp = (p1 - p0) / 2.0
        per = ((2.0 * np.pi * oscl) / ((end-start)*60.0)) * t
        disp = (p1 + p0) / 2.0

        return amp * np.sin(per) + disp

    def dataUpdate(self):
        """
        near-simultanious instantiation of time, flow rate and pressure readings
        """
        self.__time_points.append(time.time() - self.__start)
        # self.__pressure_points.append( Figure out how to get actual pressure from machine )
        # for port_index in range(len(self.__activePorts)):
            # self.__flow_points[port_index].append( Figure out how to get flow rate of specific port from machine) for self.activePorts[port_index]
        # print('Update Data')
        
    
    
    def setpointUpdate(self):
        """
        Modifies setpoint of machine based on the designated behavior
        """
        t = time.time() - self.__start
        t = t % (self.__cycleLength*60)
        if self.__pressureCtrlBool:
            for behave in self.__pressureBehaviorList:
                if t > behave[1]*60.0 and t < behave[2]*60.0:
                    if behave[0] == 'Static':
                        pressure_setpoint = self.static(behave[3])
                    
                    elif behave[0] == 'Linear':
                        pressure_setpoint = self.linear(
                            behave[1], behave[2], behave[3],
                            behave[4], t)
                    
                    elif behave[0] == 'Exponential':
                        pressure_setpoint = self.exponential(behave[1], 
                            behave[2], behave[3],behave[4], t)
                    
                    elif behave[0] == 'Periodic':
                        pressure_setpoint = self.periodic(behave[1], 
                            behave[2], behave[3],behave[4], behave[5], t)
                    self.__pressure_points.append(pressure_setpoint)
                    for port in self.__flow_points:
                        port.append(2)
                    # enter setpoint to machine once I figure out how
        else:
            self.__pressure_points.append(1)
            for behave in self.__MFCBehaviorList:
                port = behave[0]

                if t > behave[3]*60.0 and t < behave[4]*60.0:
                    # slave = False

                    # for p in self.__slaveBehaviorList:
                    #     if port == p[1] and not p[0]:
                    #         slave = True
                    #         break
                    if behave[2] == 'Static':
                        flow_setpoint = self.static(behave[5])
                    
                    elif behave[2] == 'Linear':
                        flow_setpoint = self.linear(
                            behave[3], behave[4], behave[5],
                            behave[6], t)
                    
                    elif behave[2] == 'Exponential':
                        flow_setpoint = self.exponential(
                            behave[3], behave[4], behave[5], 
                            behave[6], t)
                    
                    elif behave[2] == 'Periodic':
                        flow_setpoint = self.periodic(
                            behave[3], behave[4], behave[5], 
                            behave[6], behave[7], t)
                    self.__flow_points[port-1].append(flow_setpoint)
                    
                    # enter setpoint to machine once I figure out how
            for i in self.__gas_dex.keys():
                slave = self.__slaveBehaviorList[self.__gas_dex[i]-1]
                if slave[0]:
                    master = slave[2]
                    for j in self.__gas_dex.keys():
                        if master == self.__gas_dex[j]:
                            break
                    self.__flow_points[i] = np.multiply(self.__flow_points[j],slave[3])
    
    def endExperiment(self):
        def push(btn):
            my_entry = app.getEntry("Data Location")
            my_name = app.getEntry("File Name")
            my_file = my_entry + "/" + my_name+ ".csv"
            my_file.replace(" ", "_")
            # app.stop()
            
            header = ["Time (s)", "Pressure (Torr)"]
            for i in self.__activePorts.keys():
                if self.__activePorts[i] != None:
                    header.append(str(self.__activePorts[i]) + " Flow Rate (SCCM)")
            
            
            if len(self.__flow_points) == 1:
                var0 = self.__flow_points[0]
                flow_rows = zip(self.__time_points, self.__pressure_points, var0)

            elif len(self.__flow_points) == 2:
                var0 = self.__flow_points[0]
                var1 = self.__flow_points[1]
                flow_rows = zip(self.__time_points, self.__pressure_points, var0, var1)

            elif len(self.__flow_points) == 3:
                var0 = self.__flow_points[0]
                var1 = self.__flow_points[1]
                var2 = self.__flow_points[2]
                flow_rows = zip(self.__time_points, self.__pressure_points, var0, var1, var2)
                
            elif len(self.__flow_points) == 4:
                var0 = self.__flow_points[0]
                var1 = self.__flow_points[1]
                var2 = self.__flow_points[2]
                var3 = self.__flow_points[3]
                flow_rows = zip(self.__time_points, self.__pressure_points, var0, var1, var2,var3)
                      
            elif len(self.__flow_points) == 5:
                var0 = self.__flow_points[0]
                var1 = self.__flow_points[1]
                var2 = self.__flow_points[2]
                var3 = self.__flow_points[3]
                var4 = self.__flow_points[4]
                flow_rows = zip(self.__time_points, self.__pressure_points, var0, var1, var2,var3,var4)
                
            elif len(self.__flow_points) == 6:
                var0 = self.__flow_points[0]
                var1 = self.__flow_points[1]
                var2 = self.__flow_points[2]
                var3 = self.__flow_points[3]
                var4 = self.__flow_points[4]
                var5 = self.__flow_points[5]
                flow_rows = zip(self.__time_points, self.__pressure_points, var0, var1, var2,var3,var4,var5)

            elif len(self.__flow_points) == 7:
                var0 = self.__flow_points[0]
                var1 = self.__flow_points[1]
                var2 = self.__flow_points[2]
                var3 = self.__flow_points[3]
                var4 = self.__flow_points[4]
                var5 = self.__flow_points[5]
                var6 = self.__flow_points[6]
                flow_rows = zip(self.__time_points, self.__pressure_points, var0, var1, var2,var3,var4,var5,var6)

            elif len(self.__flow_points) == 8:
                var0 = self.__flow_points[0]
                var1 = self.__flow_points[1]
                var2 = self.__flow_points[2]
                var3 = self.__flow_points[3]
                var4 = self.__flow_points[4]
                var5 = self.__flow_points[5]
                var6 = self.__flow_points[6]
                var7 = self.__flow_points[7]
                flow_rows = zip(self.__time_points, self.__pressure_points, var0, var1, var2,var3,var4,var5,var6,var7)

            with open(my_file, 'w') as filehandle:  
                writer = csv.writer(filehandle, dialect = 'excel', quoting=csv.QUOTE_NONNUMERIC)
                writer.writerow(header)
                for row in flow_rows:
                    writer.writerow(row)

            app.stop()
            
            
        app = aj.gui()
        app.setFont(size = 24, family = "Times")
        app.addLabel ("", "Provide a location and a name for the experimental data file")
        app.addLabelEntry("File Name")
        app.addLabelDirectoryEntry("Data Location")
        app.addButton("Submit", push)
        app.go()