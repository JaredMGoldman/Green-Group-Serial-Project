import appJar as aj
import numpy as np
import time
import Controller as ctrl

class Screen(aj.gui):
    
    def __init__(self, title=None, geom=None, handleArgs=True, language=None,startWindow=None, useTtk=False, useSettings=False, showIcon=True, **kwargs):
        self.initialTime = 0            # Changing value to track the progress of an instance of a behavior (i.e. periodic, exponential, etc.)
        
        self.colCtr = 0                 # Incrementing variable to ensure generalized positioning of widgets
        
        self.rowCtr = 1                 # Incrementing variable to ensure generalized positioning of widgets
        
        self.pressureSerial = 0         # Variable to ensure all widgets have unique names (esp. in cases with many possible combinations)
        
        self.cycles = 0                 # Saves total number of cycles to be completed
        
        self.lengthEach = 0             # Saves length of each cycle in minutes
        
        self.colList = []               # Designed to find the length of the longest column in order to ensure that the horizontal 
                                        # separator is long enough
        
        self.myDict = {                 # A binary representation of wether or not there is a gas assigned to the numbered port.
            1:0,2:0,3:0,4:0, 
            5:0,6:0,7:0,8:0
            }      
                                             
        self.gasCtr = 0                 # Ensures that the gas selection menu widgets have unique titles   

        self.gasDict = {                # The final dictionary matching the MFC port number with the name of the gas assigned to it 
            1:None, 2:None,             
            3:None, 4:None, 
            5:None, 6:None, 
            7:None, 8:None}                                         

        self.gasCtrDict = {             # For internal use. Saves the self.gasCtr number for a "Gas" option box entry. May not be the 
            1:None, 2:None,             # final number. self.gasDict saves the more useful information (final)
            3:None, 4:None, 
            5:None, 6:None, 
            7:None, 8:None}             
                                        
        self.gasIndex = []              # Stores the indexes of the ports that contain gases after confirmation
        
        self.iter = 0                   # Incrementing variable used in the gas behavior section to move through the final gasses 
        
        self.errflag = 0                # Several uses. Generally useful tool in choosing between two paths (0/1)              
        
        self.behavior = ""              # saves the type of behavior for internal and data saving applications

        self.data = ctrl.Controller()                # creates the object that will store all of the relevent data    

        self.slaveDict= {               # the dictionary of lists with keys coorresponding to port number
            1:[9,0.0, False, False],    # [master port, ratio, isSlave, is key port active]
            2:[9,0.0, False, False], 
            3:[9,0.0, False, False], 
            4:[9,0.0, False, False], 
            5:[9,0.0, False, False], 
            6:[9,0.0, False, False], 
            7:[9,0.0, False, False], 
            8:[9,0.0, False, False]} 
        
        super().__init__(
            title=None, geom=None, handleArgs=True, language=None, 
            startWindow=None, useTtk=False, useSettings=False, 
            showIcon=True, **kwargs
            )        
    
        
                                    #########################################
                                    ################ FLOW RATE ##############     
                                    ######################################### 
    def render2fc2(self):
        """
        input:
                none
        
        output:
                gas behvior selection screen

        This function is designed to produce a generic approach to 
        choosing the behavior of each gas controlled by the MFCs, given 
        by the previous page. The page will allow the user to select 
        different behaviors for the individual gases within the time 
        of one cycle (as given by self.lengthEach).
        """
        def newGasRow():
            """
            input:
                    none
            output:
                    new opportunity to select the flow rate behavior of 
                    a gas

            This function is designed to allow the user to determine the 
            behavior of a gas governed by an MFC.
            """
            self.colCtr = 0
            self.addLabel("l11" + str(self.pressureSerial), 
                "Port " + str(self.gasIndex[self.iter]), 
                row = self.rowCtr)
            self.addLabel("l12"+ str(self.pressureSerial), 
                "Gas: "+str(self.gasDict[self.gasIndex[self.iter]]), 
                row = self.rowCtr +1)
            self.colCtr += 1
            self.addVerticalSeparator(column = self.colCtr, 
                rowspan = 3, row = self.rowCtr)
            self.colCtr += 1
            self.addLabel("l13" + str(self.pressureSerial), 
                "Type of Flow Behavior: ", row= self.rowCtr, 
                column = self.colCtr)
            self.colCtr += 1
            self.addOptionBox("TB"+str(self.pressureSerial), 
                ["- Select an Option -", "Static", "Linear", 
                "Exponential", "Periodic"], 
                row = self.rowCtr, column=self.colCtr)
            self.rowCtr += 1
            self.setOptionBoxChangeFunction(
                "TB"+str(self.pressureSerial), myChangeFunc)
        
        def final(btn):
            my_entry = self.getEntry("File Location")
            my_name = self.getEntry("Filename")
            my_file = my_entry + "/" + my_name+ ".data"
            my_file.replace(" ", "_")
            self.data.saveData(my_file)
            self.stop()
            self.data.beginExperiment()

        
        def heave(btn):
            """
            input:
                    none
            output:
                    none
            
            This function occurs when the "start experiment" button is 
            clicked. It redirects the user to the experiment screen. 
            """
            save = self.yesNoBox("Save Experiment Information",
                "Would you like to save the current experimental setup?")
            if save:
                # self.removeAllWidgets()
                # self.addLabel('', 
                #     'Choose a destination for the experimental configuration')
                # self.addDirectoryEntry("File Location")
                # self.addButton("Finalize Location", final)
                self.errflag = 1
                self.removeAllWidgets()
                self.addLabel('', 
                    'Choose a destination for the experimental configuration', colspan = 2)
                self.addLabel("Intrusctions", "Pleasse enter a name for your setup:")
                self.addEntry("Filename", row = 1, column = 1)
                self.addDirectoryEntry("File Location", colspan = 2)
                self.addButton("Finalize Location", final, colspan = 2)
            else:
                self.stop()
                self.data.beginExperiment()


        def bigPush():
            """
            input:
                    none
            output:
                    either creates a new opportunity for the user to 
                    select the desired gas behavior or creates a "start 
                    experiment button"

            This function is designed to determine the progess of the gas
            selection process.  If it is complete (i.e. there are no more 
            gases to determine the behavior of and the cycle time limit 
            has been reached for the current gas) the function will give 
            the user the option to continue to the experiment display screen.

            * Thought * I could redirect the user directly to the final * Thought * 
            * Thought *  screen without the need for them to interact.  * Thought *
            """
            # initialize variables used here to preserve backstep functionality
            stop = int(self.getSpinBox("ET" + str(self.pressureSerial)))
            mag1 = 0
            oscillations = 0
            save_criteria = True
            mag0 = self.getEntry("DFR" + str(self.pressureSerial)) 
            
            # Save values to check validity
            if self.behavior == "Linear" or self.behavior == "Exponential":
                mag1 = self.getEntry("'DFR" + str(self.pressureSerial)) 
            
            elif self.behavior == "Periodic":
                mag1 = self.getEntry("'DFR" + str(self.pressureSerial))   
                oscillations =  int(self.getSpinBox("Oscillations" + str(self.pressureSerial)))

            # Check if user input is valid before saving local variables as instance variables
            if mag0 == None  or stop == 0 or mag1 == None :
                save_criteria = False
                self.warningBox("Invalid Entry",
                     "Please make sure you have entered a value for flow rate and end time." )
            elif mag0 < 0 or mag1 < 0:
                save_criteria = False
                self.warningBox("Invalid Entry", 
                    "Please make sure you have entered a positive value for flow rate." )
            elif ((self.behavior == "Linear" or self.behavior == "Exponential" or 
                self.behavior == "Periodic") and (mag1 == None )):
                save_criteria = False
                self.warningBox("Invalid Entry", 
                    "Please make sure you have entered a value for flow rate." )
            elif self.behavior == "Periodic" and oscillations == 1 :
                save_criteria = self.yesNoBox("Invalid Entry", 
                    "Are you sure you only want 1 oscillation?" )
            
            if save_criteria:
                self.pressureSerial += 1
                self.data.setMFCBehaviorList(
                    self.gasDict[self.gasIndex[self.iter]], self.gasIndex, 
                    self.behavior, self.initialTime, stop, mag0, 
                    mag1, oscillations)
                self.initialTime = stop
                self.removeButton("Okay")
                self.rowCtr += 1
                self.addHorizontalSeparator(row = self.rowCtr, 
                    column = 0,colspan=8, colour="black",)
                self.rowCtr += 1
                
                if self.initialTime == int(self.lengthEach):
                    self.iter += 1
                    if self.iter == len(self.gasIndex):
                        self.rowCtr -= 4
                        self.addButton("Start Experiment", heave, 
                        row = self.rowCtr, column = 8)
                    else:
                        self.gasIndex[self.iter]  
                        self.initialTime = 0
                        newGasRow()
                else:
                    newGasRow()
                        
        
        def flowSelecter():
            """
            input:
                    none
            output:
                    place to enter flow rate and means of selecting units
            
            This is a function of reused code, used to generate a way of 
            collecting data on flow rate including magnitude and units.
            """
            self.addNumericEntry("DFR" + str(self.pressureSerial), 
                row = self.rowCtr, column=self.colCtr)
            self.colCtr += 1
            self.addLabel(str(self.pressureSerial), "SCMM",
                row = self.rowCtr, column= self.colCtr)
            self.colCtr += 1

        def flowSelecter1():
            """
            input:
                    none
            output:
                    place to enter flow rate and means of selecting units
            
            This is a function of reused code, used to generate a way of 
            collecting data on flow rate including magnitude and units.
            (duplicate needed to keep widget names unique)
            """
            self.addNumericEntry("'DFR" + str(self.pressureSerial), 
                row = self.rowCtr, column=self.colCtr)
            self.colCtr += 1
            self.addLabel(str(self.pressureSerial)  + "'", "SCMM",
                row = self.rowCtr, column= self.colCtr)
            self.colCtr += 1

        def timeKeeper():
            """
            input:
                    none
            output:
                    start time and place to enter stop time for a behavior
            
            This is a function of reused code, used to generate a way of 
            collecting data on end time of a specific behavior.
            """
            self.addLabel("l4"+ str(self.pressureSerial), 
                "Start Time: "+str(self.initialTime),
                row=self.rowCtr,column=self.colCtr)
            self.colCtr += 1
            self.addLabel("l5"+ str(self.pressureSerial), 
                "End Time: ", row = self.rowCtr, column = self.colCtr)
            self.colCtr += 1
            self.addSpinBoxRange("ET"+str(self.pressureSerial), 
                int(self.initialTime), int(self.lengthEach),
                row = self.rowCtr, column = self.colCtr)
            self.colCtr += 1
            self.addButton("Okay", bigPush, row = self.rowCtr, column = self.colCtr)
            self.setButtonBg("Okay", "LimeGreen")
        
        def periodGetter(btn):
            """
            input:
                    button click during runtime
            output:
                    inforBox with the period of an oscillation based on
                    user input

            This function responds to the changing of a value in either 
            the End Time ("ET") spinBox or in the "Oscillation" spinBox 
            """
            end = int(self.getSpinBox("ET"+str(self.pressureSerial)))
            duration = end - int(self.initialTime)
            oscillations = int(self.getSpinBox(
                "Oscillations"+str(self.pressureSerial)))
            if oscillations is not None and duration != 0:
                period = duration / oscillations
                self.infoBox("Period", 
                    "The period of this configuration is "+str(period)+" minutes.")
        
        def periodic():
            """
            input:
                    none
            output:
                    means of entering data needed to perform periodic 
                    alteration of flow
            """
            self.colCtr = 2
            self.addLabel("l1"+str(self.pressureSerial), "Minimum:",
                row = self.rowCtr, column = self.colCtr)
            self.colCtr += 1
            flowSelecter()
            self.addLabel("l2"+str(self.pressureSerial), text="Maximum:",
                row = self.rowCtr, column = self.colCtr)
            self.colCtr += 1
            flowSelecter1()
            self.rowCtr += 1
            self.colCtr = 2
            self.addLabel("l3"+str(self.pressureSerial),"Number of Oscillations:", 
                row = self.rowCtr, column = self.colCtr)
            self.colCtr += 1
            self.addSpinBoxRange("Oscillations" + str(self.pressureSerial), 
                1, 10000, row = self.rowCtr, column = self.colCtr)
            self.setSpinBoxChangeFunction("Oscillations" + str(self.pressureSerial), 
                periodGetter)
            self.colCtr += 1
            timeKeeper()
        
        def exponential():
            """
            input:
                    none
            output:
                    means of entering data needed to perform exponential 
                    alteration of flow
            """
            linear()

        def linear():
            """
            input:
                    none
            output:
                    means of entering data needed to perform linear 
                    alteration of flow
            """
            self.colCtr = 2
            self.addLabel("l1"+str(self.pressureSerial), 
                "Initial Flow Rate: ",row = self.rowCtr, column = self.colCtr)
            self.colCtr += 1
            flowSelecter()
            self.addLabel("l2"+str(self.pressureSerial),  
                "Final Flow Rate: ",row = self.rowCtr, column = self.colCtr)
            self.colCtr += 1
            flowSelecter1()
            self.rowCtr += 1
            self.colCtr = 2
            timeKeeper()

        
        def static():
            """
            input:
                    none
            output:
                    means of entering data needed to perform static 
                    alteration of flow
            """
            self.colCtr = 2
            self.addLabel("l1"+ str(self.pressureSerial), 
                "Desired Flow Rate:", row = self.rowCtr, column = self.colCtr)
            self.colCtr += 1
            flowSelecter()
            self.rowCtr += 1
            self.colCtr = 2
            timeKeeper()

        def myChangeFunc(btn):
            """
            input: 
                    none
            output:
                    specified type of flow behavior, based on user input 
                    into optionBox

            This function occurs in response to the user selecting a 
            behavior entry from the option box and provides the 
            cooresponding data entry interface for the user to interact 
            with.

            * TO DO * Enable user to change their mind and select a * TO DO *
            * TO DO *             different option.                 * TO DO *
            """
            self.behavior = self.getOptionBox("TB" + str(self.pressureSerial))
            if self.behavior == "Static":
                static()
            elif self.behavior == "Linear":
                linear()
            elif self.behavior == "Exponential":
                exponential()
            elif self.behavior == "Periodic":
                periodic()

        def back(btn):
            """
            input:
                    user clicks back arrow
            output:
                    previous page
            """
            self.render2fc1()
        
        # Code for initializing the flow behavior selection screen
        self.removeAllWidgets()

        self.addButton("\u21A9", back)
        self.setButtonBg("\u21A9", "Red")
        self.initialTime = 0
        self.addLabel("l0",
            "Please select the desired behavior for each of the gasses in turn", 
            row = 0, column = 2)
        self.rowCtr = 1
        self.pressureSerial = 0
        newGasRow()
        


    def render2fc1(self):
        """
        input:
                none
        output:
                array of check-boxes that allow user to choose which 
                gases are loaded in MFC ports

        This function allows the user to select the port and type of gas 
        that the MFCs are connected to. This data is saved in 
        self.gasDict for later use.
        """
        # initialize backspace functionality variables
        
        self.myDict = {1:0, 2:0, 3:0,4:0, 5:0, 6:0,7:0, 8:0}
        self.gasCtrDict = {1:None, 2:None, 3:None, 4:None, 5:None, 6:None, 7:None, 8:None}
        self.gasCtr = 0
        self.gasDict = {1:None, 2:None, 3:None, 4:None, 5:None, 6:None, 7:None, 8:None}
        self.slaveDict = {1:[9,0.0, False, False], 2:[9,0.0, False, False], 
                        3:[9,0.0, False, False], 4:[9,0.0, False, False], 
                        5:[9,0.0, False, False], 6:[9,0.0, False, False], 
                        7:[9,0.0, False, False], 8:[9,0.0, False, False]} 
        self.gasIndex = []
        self.iter = 0
        
        def final(btn):
            my_entry = self.getEntry("File Location")
            my_name = self.getEntry("Filename")
            my_file = my_entry +  "/" + my_name+ ".data"
            my_file.replace(" ", "_")
            self.data.saveData(my_file)
            self.stop()
            self.data.beginExperiment()

        
        def push():
            save_bool = True
            for i in range(1,9):
                
                if self.myDict[i] == 1:
                    if self.getOptionBox("Gases"+str(self.gasCtrDict[i])) == None:
                        save_bool = False
                        self.warningBox("Invalid Entry", 
                            "Make sure that you have chosen a gas for each active port.")
                    
                    if self.errflag == 0 and self.slaveDict[i][2]:
                        master, ratio = self.getOptionBox("Master"+str(i)), self.getEntry("Ratio" + str(i))
                        if master == None or ratio == None:
                            save_bool = False
                            self.warningBox("Invalid Entry", 
                                "Make sure that you have chosen a master and ratio for each slave.")
                        else:
                            master = int(master[-1])
                            self.slaveDict[i][0], self.slaveDict[i][1] = master, ratio

            
            if save_bool:
                for i in range(1, 9):
                    if self.gasCtrDict[i] is not None:
                        self.gasDict[i] = self.getOptionBox("Gases"+str(self.gasCtrDict[i]))
                        if self.myDict[i] == 1 and not self.slaveDict[i][2]:
                            self.gasIndex.append(i)
                    self.data.setSlaveList(self.slaveDict[i][2], i,
                                            self.slaveDict[i][0],
                                            self.slaveDict[i][1])
                if self.errflag == 1:
                    for i in range(1,9):
                        self.data.setMFCBehaviorList(self.gasDict[i],i)

                    self.errflag = 0
                    save = self.yesNoBox("Save Experiment Information",
                        "Would you like to save the current experimental setup?")
                    if save:
                        self.errflag = 1
                        self.data.setActivePorts(self.gasDict)
                        self.removeAllWidgets()
                        self.addLabel('', 
                            'Choose a destination for the experimental configuration', colspan = 2)
                        self.addLabel("Intrusctions", "Pleasse enter a name for your setup:")
                        self.addEntry("Filename", row = 1, column = 1)
                        self.addDirectoryEntry("File Location", colspan = 2)
                        self.addButton("Finalize Location", final, colspan = 2)
                    else:
                        self.stop()
                        self.data.beginExperiment()

                else:
                    self.data.setActivePorts(self.gasDict)
                    self.render2fc2()
        

        def removeSlaveDetails(index):
            self.slaveDict[index][2] = False
            self.removeCheckBox("Slave"+str(index))
            self.removeLabel("M-name" + str(index))
            self.removeOptionBox("Master" + str(index))
            self.removeLabel(str(index))
            self.removeEntry("Ratio" + str(index))

        def slaveFunc(btn):
            for i in range(1,9):
                if self.slaveDict[i][3]:
                    self.slaveDict[i][2] = self.getCheckBox("Slave"+str(i))
        
        def myLittleFunc(change):
            """
            input:
                    none
            output:
                    displays or hides selection box for MFC ports 
                    depending upon value of corresponding check-box

            This function occurs when a check-box next to a port is 
            toggled.  The result is to hide or display the gas selection 
            optionBox, depending upon its previous visibility. 
            
            This function also updates self.myDict with the value 0/1 
            depending on whether there is (1) or is not (0) a gas present 
            at a particular port.

            Additionally, this function employs self.gasCtrDict to save 
            the gas serial number corresponding to the active MFC ports.
            In this way, it is possible to trace back the gas type to a 
            correspondingly labeled optionBox ("Gases(gas Serial)") as 
            accomplished upon completion of this page. 
            """
            
            if self.errflag == 1:
                rowRef = {1:2, 2:2, 3:4, 4:4, 5:6, 6:6, 7:8, 8:8}
            else:
                rowRef = {1:2, 2:2, 3:5, 4:5, 5:8, 6:8, 7:11, 8:11}
            
            for i in range(1,9):
                if self.errflag == 1:
                    if i % 2 == 1:  col = 1
                    else:           col = 4
                else:
                    if i % 2 == 1:  col = 1
                    else:           col = 7
                if self.getCheckBox("Port " + str(i)) and self.myDict.get(i) == 0:
                    self.myDict[i] = 1
                    rows = rowRef[i]
                    self.addOptionBox("Gases" + str(self.gasCtr), ["- Gases -", 
                    "- Commonly Used -", "Air", "Carbon Dioxide", "Helium", 
                    "Hydrogen", "Nitrogen", "Oxygen", "-Commonly Used -",
                    "Actylene", "Air", "Ammonia", "Argon", "Arsine", 
                    "Boron Trichloride", "Bromine", "Carbon Dioxide", 
                    "Carbon Monoxide", "Carbon Tetrachloride", 
                    "Carbon Tetraflouride", "Chlorine", "Chlorodifluoromethane", 
                    "Chloropentafluoroethane", "Cyanogen", "Deuterium", 
                    "Diborane", "Dibromane", "Dibromodifluoromethane", 
                    "Dichlorodifluoromethane", "Dichlorofluoromethane", 
                    "Dichloromethysilane", "Dichlorosilane", 
                    "Dichlorotetrafluoroethane", "Difluoroethylene", 
                    "Dimethylpropane", "Ethane", "Fluorine", "Fluoroform", 
                    "Freon - 11", "Freon - 12", "Freon - 13", "Freon - 14", 
                    "Freon - 21", "Freon - 22", "Freon - 23", "Freon - 113", 
                    "Freon - 114", "Freon - 115", "Freon - 116", "Freon - C318", 
                    "Freon - 1132A", "Helium", "Hexafluoroethane", "Hydrogen", 
                    "Hydrogen Bromide", "Hydrogen Chloride", "Hydrogen Fluoride", 
                    "Isobutylene", "Krypton", "Methane", "Methyl Fluoride", 
                    "Molybdenum Hexafluoride", "Neon", "Nitric Oxide", "Nitrogen", 
                    "Nitrogen Dioxide", "Nitrogen Trifluoride", "Nitrous Oxide", 
                    "Octafluorocyclobutane", "Oxygen", "Pentane", "Perfluoropropane", 
                    "Phosgene", "Phosphine", "Propane", "Propylene", "Silane", 
                    "Silicon Tetrachloride", "Silicon Tetrafluoride", "Sulfur Dioxide", 
                    "Sulfur Hexafluoride", "Trichlorofluoromethane", "Trichlorosilane", 
                    "Tungsten Hexafluoride", "Xenon"], row = rows, column = col)                    
                    self.gasCtrDict[i] = self.gasCtr
                    self.gasCtr += 1
                    
#                   Add Slave buttons
                    if self.errflag == 0:
                        portList = ["- Master -"]
                        for j in range(1, 9):
                            if j != i:
                                portList.append("Port " + str(j))
                        self.addNamedCheckBox(title = ("Slave"+str(i)), name = "Slave", row = rows+1, column = col-1)
                        self.addLabel("M-name" + str(i), "Master Port:", row = rowRef[i]+1, column = col)
                        self.addOptionBox("Master" + str(i), portList, row = rowRef[i]+1, column = col+1)
                        self.addLabel(str(i), "Ratio:", row = rowRef[i]+1, column = col +2)
                        self.addNumericEntry("Ratio" + str(i), row = rowRef[i]+1, column = col +3)
                        self.setCheckBoxChangeFunction("Slave" + str(i), slaveFunc)
                        self.slaveDict[i][3] = True

                elif self.getCheckBox("Port " + str(i)) != True and self.myDict.get(i) == 1:
                    self.myDict[i] = 0
                    
                    if self.errflag == 1:
                        if i % 2 == 1: col = 1
                        else: col = 4
                    else:
                        if i % 2 == 1: col = 1
                        else: col = 7
                    rows = rowRef[i]
                    self.addLabel("gas ctr" + str(self.gasCtr), "", row= rows, column = col)
                    self.gasCtrDict[i] = None
                    self.gasCtr += 1

                    self.slaveDict[i][3] = False
                    removeSlaveDetails(i)
        
        def back(btn):
            """
            input:
                    user clicks back arrow
            output:
                    previous page
            """
            if self.errflag == 0:
                self.render2fc()
            else:
                self.render2p1() 
            
        
        # Initialize the widgets of the window
        self.removeAllWidgets()
        self.addButton("\u21A9", back)
        self.setButtonBg("\u21A9", "Red")
        
        # The baseline widgets of a pressure-dependent setup
        if self.errflag == 1:
            self.addLabel("title", "Select the Working MFCs", row = 0, column = 1, colspan=3)
            self.addCheckBox("Port 1", row = 2)
            self.addCheckBox("Port 3", row = 4)
            self.addCheckBox("Port 5", row = 6)
            self.addCheckBox("Port 7", row = 8)
            self.addCheckBox("Port 2", row = 2, column = 3)
            self.addCheckBox("Port 4", row = 4, column = 3)
            self.addCheckBox("Port 6", row = 6, column = 3)
            self.addCheckBox("Port 8", row = 8, column = 3)
            self.addButton("Submit", push, row = 10, colspan = 4)
            self.setButtonBg("Submit", "LimeGreen")
            self.addHorizontalSeparator(row = 1, column = 0, colspan = 8)
            self.addHorizontalSeparator(row = 3, column = 0, colspan = 8)
            self.addHorizontalSeparator(row = 5, column = 0, colspan = 8)
            self.addHorizontalSeparator(row = 7, column = 0, colspan = 8)
            self.addHorizontalSeparator(row = 9, column = 0, colspan = 8)
            self.addVerticalSeparator(row = 1, column = 2, rowspan = 8)
        
        # baseline widgets for a flow rate dependent setup
        else:
            self.addLabel("title", "Select the Working MFCs", 
                row = 0, column = 1, colspan=11)
            self.addCheckBox("Port 1", row = 2, column = 0)
            self.addCheckBox("Port 3", row = 5, column = 0)
            self.addCheckBox("Port 5", row = 8, column = 0)
            self.addCheckBox("Port 7", row = 11, column = 0)
            self.addCheckBox("Port 2", row = 2, column = 6)
            self.addCheckBox("Port 4", row = 5, column = 6)
            self.addCheckBox("Port 6", row = 8, column = 6)
            self.addCheckBox("Port 8", row = 11, column = 6)
            self.addButton("Submit", push, row = 12, colspan = 11 )
            self.setButtonBg("Submit", "LimeGreen")
            self.addHorizontalSeparator(row = 4, column = 0, colspan = 10)
            self.addHorizontalSeparator(row = 1, column = 0, colspan = 10)
            self.addHorizontalSeparator(row = 7, column = 0, colspan = 10)
            self.addHorizontalSeparator(row = 10, column = 0, colspan = 10)
            self.addVerticalSeparator(row = 1, column = 5, rowspan = 11)

        for i in range(1,9):
            self.setCheckBoxChangeFunction("Port " + str(i), myLittleFunc)
    
    def render2fc(self):
        """
        input:
                none
        output:
                cycle info selection page for flow rate dependent experiment

        This function creates the screen in which the user can enter the data about the number of cycles and the time of each cycle.
        This data is saved as self.cycles and self.lengthEach, respectively.
        """
        self.cycles = ""
        self.lengthEach = "" 

        def push(btn):
            """
            input:
                    none
            output:
                    moves to MFC port + gas selection screen
            
            This function serves the primary purpose of saving the cycle 
            data while also advancing the user interface to the next page.
            """
            self.cycles = self.getSpinBox("Number of Cycles")
            self.lengthEach = self.getSpinBox("Duration of One Cycle (minutes)")
            entry_bool = True

            if self.cycles == '1' and self.lengthEach == '1':
                entry_bool = self.yesNoBox("Consider Revising", 
                    "Are you sure you want "+self.cycles+" cycle for "+self.lengthEach+" minute?")
            elif self.cycles != '1' and self.lengthEach == '1':
                entry_bool = self.yesNoBox("Consider Revising", 
                    "Are you sure you want "+self.cycles+" cycles for "+self.lengthEach+" minute each?")
            elif self.cycles == '1' and self.lengthEach != '1':
                entry_bool=self.yesNoBox("Consider Revising", 
                "Are you sure you want "+self.cycles+" cycle for "+self.lengthEach+" minutes?")

            if entry_bool:
                self.data.setCycleLength(int(self.lengthEach))
                self.data.setNumberOfCycles(int(self.cycles))
                self.render2fc1()

        self.removeAllWidgets()
        def back(btn):
            """
            input:
                    user clicks back arrow
            output:
                    previous page
            """
            self.render1()

        self.addButton("\u21A9", back)
        self.setButtonBg("\u21A9", "Red")

        self.addLabel("Select the number of cycles and the duration of each one.", 
            row = 0, column = 1)
        self.addLabel("", "Number of Cycles")
        self.addSpinBoxRange("Number of Cycles",1,100, row = 1, column= 1)
        self.addLabel("1", "Duration of one Cycle (minutes")
        self.addSpinBoxRange("Duration of One Cycle (minutes)",1, 100, 
            row = 2, column = 1)
        self.addButton("Okay", push, colspan = 2)
        self.setButtonBg("Okay", "LimeGreen")


                  
                                    #########################################
                                    ################ PRESSURE ###############     
                                    ######################################### 

    
    def render2p1(self):
        """
        input:
                none
        
        output:
                pressure behavior selection screen

        This function is designed to produce a generic approach to choosing the pressure in the system.
        The page will allow the user to select different pressure behaviors within the time of one 
        cycle (as given by self.lengthEach).
        """
        def myChangeFunc(optionBox):
            """
            input: 
                    none
            output:
                    specified type of pressure behavior, based on user input into optionBox

            This function occurs in response to the user selecting a behavior entry from the option box and provides the 
            cooresponding data entry interface for the user to interact with.

            * TO DO * Enable user to change their mind and select a different option. * TO DO *
            """
            self.behavior = self.getOptionBox("TPB" + str(self.pressureSerial))
            if self.behavior == "Static":
                static()
            elif self.behavior == "Linear":
                linear()
            elif self.behavior == "Exponential":
                exponential()
            elif self.behavior == "Periodic":
                periodic()
        
        def newRow():
            """
            input:
                    none
            output:
                    new opportunity to select the flow rate behavior of a gas

            This function is designed to allow the user to determine the behavior of pressure for an undefined 
            time increment of the cycyle.
            """
            self.colCtr = 0
            self.addLabel("l0" + str(self.pressureSerial), "Type of Pressure Behavior: ", row= self.rowCtr, column = self.colCtr)
            self.colCtr += 1
            self.addOptionBox("TPB"+str(self.pressureSerial), ["- Select an Option -", "Static", "Linear", "Exponential", "Periodic"], row = self.rowCtr, column=self.colCtr)
            self.rowCtr += 1
            self.setOptionBoxChangeFunction("TPB"+str(self.pressureSerial), myChangeFunc)

        def press(btn):
            """
            input:
                    none
            output:
                    MFC port selection screen
            
            This function occurs when the time of a cycle is completely accounted for. It will
            display the MFC/gas selection screen so that the program can collect the necessary 
            data to proceed with the experiment.

            errflag is given a value of 1 so that the program knows to proceed directly to the 
            experiment screen after completing MFC/gas selection.
            """
            self.errflag = 1
            self.render2fc1()
        
        def bigPush():
            """
            input:
                    none
            output:
                    either creates a new opportunity for the user to 
                    select the desired gas behavior or creates a "start 
                    experiment button"

            This function is designed to determine the progess of the gas
            selection process.  If it is complete (i.e. there are no more 
            gases to determine the behavior of and the cycle time limit 
            has been reached for the current gas) the function will give 
            the user the option to continue to the experiment display screen.

            * Thought * I could redirect the user directly to the final * Thought * 
            * Thought *  screen without the need for them to interact.  * Thought *
            """
            # initializes variable in order to enable backstep functionality
            stop = int(self.getSpinBox("ET" + str(self.pressureSerial)))
            mag1 = 0

            oscillations = 1
            mag0 = self.getEntry("DFR" + str(self.pressureSerial)) 
            save_criteria = True

            if self.behavior == "Linear" or self.behavior == "Exponential":
                mag1=self.getEntry("'DFR"+str(self.pressureSerial)) 

            elif self.behavior == "Periodic":
                mag1=self.getEntry("'DFR" + str(self.pressureSerial)) 
                oscillations=int(self.getSpinBox("Oscillations" + str(self.pressureSerial)))
            
            # Checks possible user errors
            if mag0 == None or stop == 0:
                save_criteria = False
                self.warningBox("Invalid Entry",
                     "Please make sure you have entered a value for pressure and end time." )
            elif mag0 < 0 or mag1 < 0:
                save_criteria = False
                self.warningBox("Invalid Entry", 
                    "Please make sure you have entered a positive value for pressure." )
            elif (self.behavior == "Linear" or self.behavior == "Exponential" or self.behavior == "Periodic") and (mag1 == None ):
                save_criteria = False
                self.warningBox("Invalid Entry", 
                    "Please make sure you have entered a value for pressure." )
            elif self.behavior == "Periodic" and oscillations == 1 :
                save_criteria = self.yesNoBox("Consider Revising", 
                    "Are you sure you only want 1 oscillation?" )

            # Test passed
            if save_criteria:
                self.pressureSerial += 1
                self.data.setPressureBehaviorList(self.behavior, 
                    self.initialTime, stop, mag0, mag1, oscillations)
                self.initialTime = stop
                self.removeButton("Okay")
                if self.initialTime == int(self.lengthEach):
                    self.addButton("Select MFCs", press)
                    self.setButtonBg("Select MFCs", "LimeGreen")
                else:
                    self.rowCtr += 1
                    self.colList.append(self.colCtr)
                    self.addHorizontalSeparator(self.rowCtr,0,
                        str(max(self.colList)), colour="black")
                    self.rowCtr += 1
                    newRow()

        def back(btn):
            """
            input:
                    user clicks back arrow
            output:
                    previous page
            """
            self.render2p()
        
        self.removeAllWidgets()

        self.addButton("\u21A9", back)
        self.setButtonBg("\u21A9", "Red")

        self.addLabel("title", "Select the type of pressure behavior for each cycle.", row = 0, column = 1)
        newRow()


        def pressureSelecter():
            """
            input:
                    none
            output:
                    place to enter pressure and means of selecting units
            
            This is a function of reused code, used to generate a way of 
            collecting data on pressure including magnitude and units.
            """
            self.addNumericEntry("DFR" + str(self.pressureSerial),
                row = self.rowCtr, column = self.colCtr)
            self.colCtr += 1
            self.addLabel(str(self.pressureSerial), "Pa", 
                row = self.rowCtr, column= self.colCtr)
            self.colCtr += 1

        def pressureSelecter1():
            """
            input:
                    none
            output:
                    place to enter pressure and means of selecting units
            
            This is a function of reused code, used to generate a way of 
            collecting data on pressure including magnitude and units.
            (duplicate needed to keep widget names unique)
            """
            self.addNumericEntry("'DFR" + str(self.pressureSerial),
                row = self.rowCtr, column = self.colCtr)
            self.colCtr += 1
            self.addOptionBox(str(self.pressureSerial) + "'", 
                "Pa",row = self.rowCtr, 
                column= self.colCtr)
            self.colCtr += 1

        def timeKeeper():
            """
            input:
                    none
            output:
                    start time and place to enter stop time for a behavior
            
            This is a function of reused code, used to generate a way of 
            collecting data on end time of a specific behavior.
            """
            self.addLabel("l4"+ str(self.pressureSerial), 
                "Start Time: "  + str(self.initialTime),row = self.rowCtr, 
                column = self.colCtr)
            self.colCtr += 1
            self.addLabel("l5"+ str(self.pressureSerial), "End Time: ", 
                row = self.rowCtr, column = self.colCtr)
            self.colCtr += 1
            self.addSpinBoxRange("ET" + str(self.pressureSerial), 
                int(self.initialTime), int(self.lengthEach),row = self.rowCtr, 
                column = self.colCtr)
            self.colCtr += 1
            self.addButton("Okay",bigPush,row=self.rowCtr,column=self.colCtr)
            self.setButtonBg("Okay", "LimeGreen")
        
        def periodGetter(btn):
            """
            input:
                    button click during runtime
            output:
                    inforBox with the period of an oscillation based on
                    user input

            This function responds to the changing of a value in either 
            the End Time ("ET") spinBox or in the "Oscillation" spinBox 
            """
            end = int(self.getSpinBox("ET"+str(self.pressureSerial)))
            duration = end - int(self.initialTime)
            oscillations=int(self.getSpinBox("Oscillations"+str(self.pressureSerial)))
            if oscillations is not None and duration != 0:
                period = duration / oscillations
                self.infoBox("Period",
                    "The period of this configuration is "+str(period)+" minutes.")
        
        def periodic():
            """
            input:
                    none
            output:
                    means of entering data needed to perform periodic 
                    alteration of pressure
            """
            self.colCtr = 0
            self.addLabel("l1"+str(self.pressureSerial), "Minimum:",
                row = self.rowCtr, column = self.colCtr)
            self.colCtr += 1
            pressureSelecter()
            self.addLabel("l2"+str(self.pressureSerial),"Maximum:",
            row = self.rowCtr, column = self.colCtr)
            self.colCtr += 1
            pressureSelecter1()
            self.rowCtr += 1
            self.colCtr = 0
            self.addLabel("l3"+str(self.pressureSerial),"Number of Oscillations:", 
                row = self.rowCtr, column = self.colCtr)
            self.colCtr += 1
            self.addSpinBoxRange("Oscillations" + str(self.pressureSerial), 
                1, 10000, row = self.rowCtr, column = self.colCtr)
            self.setSpinBoxChangeFunction("Oscillations" + str(self.pressureSerial), 
                periodGetter)
            self.colCtr += 1
            timeKeeper()
        
        def exponential():
            """
            input:
                    none
            output:
                    means of entering data needed to perform exponential 
                    alteration of pressure
            """
            linear()

        def linear():
            """
            input:
                    none
            output:
                    means of entering data needed to perform linear 
                    alteration of pressure
            """
            self.colCtr = 0
            self.addLabel("l1"+str(self.pressureSerial), "Initial Pressure: ",
                row = self.rowCtr, column = self.colCtr)
            self.colCtr += 1
            pressureSelecter()
            self.addLabel("l2"+str(self.pressureSerial),  "Final Pressure: ",
                row = self.rowCtr, column = self.colCtr)
            self.colCtr += 1
            pressureSelecter1()
            self.rowCtr += 1
            self.colCtr = 0
            timeKeeper()

        
        def static():
            """
            input:
                    none
            output:
                    means of entering data needed to perform static alteration 
                    of pressure
            """
            self.colCtr = 0
            self.addLabel("l1"+ str(self.pressureSerial), "Desired Pressure:", 
                row = self.rowCtr, column = self.colCtr)
            self.colCtr += 1
            pressureSelecter()
            self.rowCtr += 1
            self.colCtr = 0
            timeKeeper()

    
    
    def render2p(self):
        """
        input:
                none
        output:
                cycle info selection page for pressure dependent experiment

        This function creates the screen in which the user can enter the 
        data about the number of cycles and the time of each cycle.  This 
        data is saved as self.cycles and self.lengthEach, respectively.
        """
        def push(btn):
            """
            input:
                    none
            output:
                    moves to pressure behavior screen
            
            This function occurs when the user presses the "Okay" button 
            after selecting the desired number and duration of cycles and
            serves the purpose of saving this data while advancing the user 
            interface to the next page.
            """
            self.cycles = int(self.getSpinBox("Number of Cycles"))
            self.lengthEach = int(self.getSpinBox("Duration of One Cycle (minutes)"))
            entry_bool = True

            if self.cycles == 1 and self.lengthEach == 1:
                entry_bool = self.yesNoBox("Consider Revising", 
                    "Are you sure you want " + str(self.cycles) + " cycle for " + str(self.lengthEach) + " minute?")

            elif self.cycles != 1 and self.lengthEach == 1:
                entry_bool = self.yesNoBox("Consider Revising", 
                    "Are you sure you want " + str(self.cycles) + " cycles for " + str(self.lengthEach) + " minute each?")

            elif self.cycles == 1 and self.lengthEach != 1:
                entry_bool = self.yesNoBox("Consider Revising", 
                    "Are you sure you want " + str(self.cycles) + " cycle for " + str(self.lengthEach) + " minutes?")


            if entry_bool:
                self.data.setCycleLength(int(self.lengthEach))
                self.data.setNumberOfCycles(int(self.cycles))
                self.removeAllWidgets()
                self.render2p1()
            
        def back(btn):
            """
            input:
                    user clicks back arrow
            output:
                    previous page
            """
            self.render1()
        
        # Cycle information input initialization
        self.removeAllWidgets()

        self.addButton("\u21A9", back)
        self.setButtonBg("\u21A9", "Red")

        self.addLabel("Select the number of cycles and the duration of each one.", 
            row = 0, column = 1)
        self.addLabel("", "Number of Cycles")
        self.addSpinBoxRange("Number of Cycles",1,100, row = 1, column= 1)
        self.addLabel("1", "Duration of one Cycle (minutes")
        self.addSpinBoxRange("Duration of One Cycle (minutes)",1, 100, 
            row = 2, column = 1)
        self.addButton("Okay", push, colspan = 2)
        self.setButtonBg("Okay", "LimeGreen")

            

    def render1(self):
        """
        input:
                none
        output:
                depending on the user's selection of experiment type, the 
                output will vary

        This function is designed to provide the user with an interface 
        with which to select the type of experiment they are performing,
        whether it is dependent upon pressure or flow rate.
        """
        self.data.setPressureBool(False)
        
        def press(btn):
            """
            input:
                    none
            output:
                    the user's selection of experiment

            This function is designed to provide the user with an interface 
            with which to select the type of experiment they are performing,
            whether it is dependent upon pressure or flow rate. 
            """
            selection = self.getRadioButton("options")
            if selection == "Pressure":
                self.data.setPressureBool(True)
                self.render2p()
            else:
                self.data.setPressureBool(False)
                self.render2fc()
        
        def back(btn):
            """
            input:
                    user clicks back arrow
            output:
                    previous page
            """
            self.removeAllWidgets()
            self.render0()
        
        self.removeAllWidgets()

        self.addButton("\u21A9", back)
        self.setButtonBg("\u21A9", "Red")

        self.addLabel("title", 
            "What is the independent variable in this experiment", 
            row = 0, column = 1)
        self.addRadioButton("options", "Pressure", colspan= 2)
        self.addRadioButton("options", "Flow Rate", colspan = 2)
        self.addButton("Select", press, colspan = 2)
        self.setButtonBg("Select", "LimeGreen")

    def render01(self):
        """
        input:
                none
        output:
                interface for user to select a saved experimental setup

        This function is designed to give the user a place to submit a 
        previously used experimental setup and avoid the hassel of 
        creating a custom experiment every time they use this program.

        This section is seperate, as the removal of a fileEntry widget 
        proved challenging. 
        """
        def heave(btn):
            """
            input:
                    none
            output:
                    experiment interface
            
            This function occurs after the user selects the 
            "Start Experiment" button.  This function is designed to 
            redirect the user to the experiment interface.

            The errflag is set to 1 to denote that the gui object require 
            careful handling as it will have a fileEntry widget which I
            do not know how to remove.
            """
            self.errflag = 1
            my_setup = self.getEntry("Saved Experiment")
            self.data.loadData(my_setup)
            self.stop()
            self.data.beginExperiment()
        
        self.removeAllWidgets()

        self.addLabel("tit", "Select The Experimental Setup:", row = 0, 
            column = 0)
        self.addFileEntry("Saved Experiment", row = 0, column = 1)
        self.addButton("Start Experiment", heave, row = 1, colspan = 2)
        self.setButtonBg("Start Experiment", "LimeGreen")


    
    
    def render0(self):
        """
        input:
                none
        output:
                depending on the user's selection of experiment type, the 
                output will vary

        This function is designed to provide the user with an interface 
        with which to select the type of experiment they are performing.
        
        The choice is between a custom and saved experiment with custom 
        experiments being created piece by piece and saved experiments 
        accessed though a file saved on the computer.
        """
        def press(btn):
            """
            input:
                    none
            output:
                    depending on the user's selection of experiment type, 
                    the output will vary

            This function is designed to provide the user with an interface 
            with which to select the type of experiment they are performing.
            
            The choice is between a custom and saved experiment with custom 
            experiments being created piece by piece and saved experiments 
            accessed though a file saved on the computer.
            """
            selection = self.getRadioButton("option")
            if selection == "Custom Experiment":
                self.render1()
            else:
                self.render01()
        
        # GUI setup
        self.setTitle("647c Flow Ratio/Pressure Controller Controller")
        self.setSize("Fullscreen")
        self.setFont(size = 24, family = "Times")
        
        # Initial page setup
        self.addLabel("title", 
            "Welcome to the Experimental Setup Menu")
        self.addLabel("subtitle", 
            "Please select the experiment you wish to perform.")
        self.addRadioButton("option", 
            "Custom Experiment")
        self.addRadioButton("option", 
            "Saved Experiment")
        self.addButton("Start", 
            press)
        self.setButtonBg("Start", 
            "LimeGreen")
        
        self.go()