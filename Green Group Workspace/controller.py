import appJar as aj

class Controller:
    def __init__(self):
        self.behaviorTypeDict = {"Static" : 0, "Linear":1, "Exponential":2, "Periodic":3}
        
        self.behaviorInfoDict = {0: "behavior", 1:"Start Time", 2:"End Time", 3:"Magnitude Value 1", 4:"Unit Value 1", 5:"Magnitude Value 2", 6:"Unit Value 2", 7:"Oscillation Value"}

        self.MFCBehaviorDict = {}

        self.pressureBehaviorList = list()

        self.cycle = 0

        self.cycleLength = 0

        self.pressureCtrlBool = False
        
        self.masterDict = {}

    def updateMaster(self):
        self.masterDict = {0:self.cycle, 1:self.cycleLength, 2: self.MFCBehaviorDict, 3:self.pressureCtrlBool, 4:self.pressureBehaviorList}
    
    def setNumberofCycles(self, cycle):
        self.cycle = cycle
        self.updateMaster()

    def set_cycle_length(self, duration):
        self.cycleLength = duration
        self.updateMaster()

    def setMFCBehaviorDict(self, gas, port, behavior, start_time, end_time, magnitude0, units0, magnitude1, units1, oscillations):
        sample = []
        if type(self.MFCBehaviorDict[(gas, port)]) != list:
            self.MFCBehaviorDict[(gas, port)] = sample
        self.MFCBehaviorDict[(gas, port)].append([[behavior, start_time, end_time, magnitude0, units0, magnitude1, units1, oscillations]])

    def setPressureCtrlBoolean(self, my_bool):
        self.pressureCtrlBool = my_bool
        if not my_bool:
            self.pressureBehaviorList = None
        else:
            self.pressureBehaviorList = list()
        self.updateMaster()

    def setPressureBehaviorList(self, behavior, start_time, end_time, magnitude0, units0, magnitude1, units1, oscillations):
        self.pressureBehaviorList.append([[behavior, start_time, end_time, magnitude0, units0, magnitude1, units1, oscillations]])


    def beginExperiment(self):
        print("Big Work")