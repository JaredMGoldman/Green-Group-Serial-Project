import appJar as aj
import pickle

class Controller:
    def __init__(self, pressure_bool):
        self.__behaviorTypeDict = {
                        "Static" : 0, "Linear":1, 
                        "Exponential":2, "Periodic":3
                        }
            
        self.__behaviorInfoDict = {
                    0: "behavior", 1:"Start Time", 2:"End Time", 
                    3:"Magnitude Value 1", 4:"Unit Value 1", 
                    5:"Magnitude Value 2", 6:"Unit Value 2", 
                    7:"Oscillation Value"
                    }

        self.__MFCBehaviorList = list()

        self.__pressureBehaviorList = list()

        self.__cycle = 0

        self.__save_list = list()

        self.__errflag = 1

        self.__cycleLength = 0

        self.__slaveBehaviorList = list()

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
        
        self.pressureCtrlBool = pressure_bool
        
    def setNumberOfCycles(self, cycle):
        self.__cycle = cycle

    def setCycleLength(self, duration):
        self.__cycleLength = duration

    def setMFCBehaviorList( self,gas=None,port=None,behavior=None,start_time=None, 
                            end_time = None, magnitude0 = None, units0 = None, 
                            magnitude1= None, units1= None, oscillations= None
                        ):
        self.__MFCBehaviorList.append([port,gas,behavior, 
            start_time, end_time, magnitude0, units0, 
            magnitude1, units1, oscillations])

    def setPressureBehaviorList(self, behavior, start_time, end_time, 
                                magnitude0, units0, magnitude1, 
                                units1, oscillations):
        self.__pressureBehaviorList.append([behavior, start_time, 
            end_time, magnitude0, units0, magnitude1, units1, 
            oscillations])

    def setSlaveList(self, slave_bool, port_id, master_id, ratio):
        self.__slaveBehaviorList.append([slave_bool, port_id, master_id, ratio])

    
    def beginExperiment(self):
        print("Big Work")

    def createSaveList(self):
        self.__save_list = [[self.pressureCtrlBool, self.__cycle, self.__cycleLength]]
        self.__save_list.append(self.__pressureBehaviorList)
        self.__save_list.append(self.__MFCBehaviorList)
        self.__save_list.append(self.__slaveBehaviorList)

    def parseData(self):
        pressureCtrlBool = self.__save_list[0][0]
        cycle = self.__save_list[0][1]
        cycleLength = self.__save_list[0][2]
        pressureBehaviorList = self.__save_list[1]     
        MFCBehaviorList = self.__save_list[2]
        slaveBehaviorList = self.__save_list[3]

    def saveData(self, location):
        self.createSaveList()
        with open(location, 'wb') as filehandle:  
            pickle.dump(self.__save_list, filehandle)
        print(self.__save_list)

    def loadData(self, location):
        with open(location, 'wb') as filehandle:  
            save_data = pickle.load(self.__save_list, filehandle)