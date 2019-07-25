import appJar as aj
import pickle
from SerialController import SerialController
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

        self.__serialController = None
        #### Experimental Information ####
        
        self.__pressureCtrlBool = False
        
        self.MFCBehaviorList = list() 

        self.__pressureBehaviorList = list()

        self.__cycle = 0

        self.__cycleLength = 0

        self.__slaveBehaviorList = list()

        #### Experimental Information ####

        self.__start = 0.0

        
        
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
        self.MFCBehaviorList.append([port,gas,behavior, 
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
        self.__serialController = SerialController()
        self.__serialController.default()
        for port in self.__activePorts.keys():
            if self.__activePorts[port] != None:
                self.__gas_dex[len(self.__flow_points)] = port
                self.__serialController.openPort(port, self.__activePorts[port])
                self.__flow_points.append([])
        
        self.__start = time.time()
        total_time = time.time()-self.__start
        while total_time <= self.__cycle * self.__cycleLength * 60:
            self.setpointUpdate()
            total_time = time.time()-self.__start
            self.__time_points.append(total_time)
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
        self.__save_list.append(self.MFCBehaviorList)
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
        self.MFCBehaviorList = self.__save_list[2]
        self.__slaveBehaviorList = self.__save_list[3]
        self.__activePorts = self.__save_list[4]
        for behave in  self.MFCBehaviorList:
            if behave[0] is list:
                behave[0] = behave[0][0]

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
        y_int = p1 - ((p1-p0)/((end-start)*60.0)) * end * 60.0

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

        return a*np.exp(r*t)/2.0

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
                    pressure_setpoint = self.__serialController.pressureSendAndReceive(pressure_setpoint)
                    self.__pressure_points.append(pressure_setpoint)
                    for key in self.__gas_dex.keys():
                        self.__flow_points[key].append(self.__serialController.receiveFlow(self.__gas_dex[key]))
                    # enter setpoint to machine once I figure out how
        else:
            self.__pressure_points.append(self.__serialController.receivePressure())
            for behave in  self.MFCBehaviorList:
                port = behave[0]

                if t > behave[3]*60.0 and t < behave[4]*60.0:
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
                    for key in self.__gas_dex.keys():
                        if self.__gas_dex[key] == port:
                            self.__flow_points[key].append(self.__serialController.flowSendAndReceive(flow_setpoint, port))

            for i in self.__gas_dex.keys():
                slave = self.__slaveBehaviorList[self.__gas_dex[i]-1]
                if slave[0]:
                    master = slave[2]
                    for j in self.__gas_dex.keys():
                        if master == self.__gas_dex[j]:
                            break
                    setpoint = self.__serialController.flowSendAndReceive(np.multiply(self.__flow_points[j][-1],slave[3]), slave[1])
                    self.__flow_points[i].append(setpoint)
                     
    
    def endExperiment(self):
        def push(btn):
            my_entry = app.getEntry("Data Location")
            my_name = app.getEntry("File Name")
            my_file = my_entry + "/" + my_name+ ".csv"
            my_file.replace(" ", "_")
            
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

        self.__serialController.close()    
        app = aj.gui()
        app.setFont(size = 24, family = "Times")
        app.addLabel ("", "Provide a location and a name for the experimental data file")
        app.addLabelEntry("File Name")
        app.addLabelDirectoryEntry("Data Location")
        app.addButton("Submit", push)
        app.go()