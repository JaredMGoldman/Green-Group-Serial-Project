import appJar as aj
import numpy as np
import time
import controller as ctrl

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
        
        self.myDict = {1:0, 2:0, 3:0,4:0, 5:0, 6:0,7:0, 8:0}      
                                         # A binary representation of wether or not there is a gas assigned to the numbered port.
                  
        self.gasCtr = 0                 # Ensures that the gas selection menu widgets have unique titles   

        self.gasDict = {1:None, 2:None, 3:None, 4:None, 5:None, 6:None, 7:None, 8:None}                 
                                        # The final dictionary matching the MFC port number with the name of the gas assigned to it

        self.gasCtrDict = {1:None, 2:None, 3:None, 4:None, 5:None, 6:None, 7:None, 8:None}             
                                        # For internal use. Saves the self.gasCtr number for a "Gas" option box entry. May not be the 
                                        # final number. self.gasDict saves the more useful information (final)
        
        self.gasIndex = []              # Stores the number of the ports that contain gases after confirmation
        
        self.iter = 0                   # Incrementing variable used in the gas behavior section to move through the final gasses 
        
        self.errflag = 0                # Several uses. Generally useful tool in choosing between two paths (0/1)              
        
        self.units = "Torr"             # Label for units of pressure for graph on experimental page
        
        self.start = None               # Beginning of experiment for self replicating process (I hope!) 
                                        # Actual process has yet to be tested. Actual feasibility unknown.         
        
        self.myRate = "SLM"             # Label for units of flow rate for graph on experimental page

        self.behavior = ""              # saves the type of behavior for internal and data saving applications

        self.data = ctrl.Controller()

        self.slaveDict = {1:9, 2:9, 3:9, 4:9, 5:9, 6:9, 7:9, 8:9}

        self.slaveBool = {1:False, 2:False, 3:False, 4:False, 5:False, 6:False, 7:False, 8:False}

        self.saveSerial = 0
        
        super().__init__(title=None, geom=None, handleArgs=True, language=None, startWindow=None, useTtk=False, useSettings=False, showIcon=True, **kwargs)
    
    def backstep(self):

        self.addButton("\u21A9")
        
    
    def finalDestination(self):
        """
        input:
                none
        output: 
                experimental screen
        
        This function creates the display for the experimental screen including the labels for the pressure 
        versus time and flow rate versus time graph, the two graphs themselves, and selector optionBoxs for 
        the user to select the units they want to display the data in on the screen.
        """
        def reP(axes):
            """
            input:
                    axes - a matplotlib axes figure object representing the graph of pressure versus time

            output:
                    updated pressure versus time graph

            This function should update the pressure versus time graph with data from the machine.
            
            * It will require a function call init that gathers the data from the machine (to be built in controller.) *
            """

            x = np.arange(0,10,0.1) #Filler code
            axes.cla()
            axes0.set_ylabel("Pressure (" + str(self.units)+")")
            axes0.set_xlabel("Time (min)")
            axes.plot(x, np.cos(x)) # Filler function
            self.refreshPlot("pressure")
        
        def reFC(axes):
            """
            input:
                    axes - a matplotlib axes figure object representing the graph of flow rate versus time

            output:
                    none

            This function updates the flow rate versus time graph with data from the machine.
            
            * It will require a function call init that gathers the data from the machine (to be built in controller.) *
            """

            x = np.arange(0,10,0.1)
            axes.cla()
            axes1.set_ylabel("Flow Rate (" + str(self.myRate) + ")")
            axes1.set_xlabel("Time (min)")
            for i in range(0,len(self.gasIndex)):
                axes.scatter(x, np.multiply(x,np.sin(x))+i, label = str(self.gasDict[self.gasIndex[i]]))
            axes.legend()
            self.refreshPlot("flow rates")

        def PU(btn):
            """
            input:
                    none

            output:
                    none
            
            This function occurs when the units of pressure have been selected by the user from the "Pressure Units" optionBox object.
            It will change the y-axis label on the pressure versus time graph and update the data input function in order to reflect 
            the new units of pressure on the graph.
            """
            self.units = self.getOptionBox("Pressure Units")
            axes0.set_ylabel("Pressure (" + str(self.units)+")")
            self.refreshPlot("pressure")

        def FU(btn):
            """
            input:
                    none

            output:
                    none
            
            This function occurs when the units of flow rate have been selected by the user from the "Flow Units" optionBox object.
            It will change the y-axis label on the flow rate versus time graph and update the data input function in order to reflect 
            the new units of flow rate on the graph.
            """
            self.myRate = self.getOptionBox("Flow Units")
            axes1.set_ylabel("Flow Rate (" + str(self.myRate) + ")")
            self.refreshPlot("flow rates")

        ########## The startup protocol of the experimental screen when coming from a custom experimental setup. ###########
        #       The widgets are all destroyed despite throwing an unknown error. This error is not fatal, so the show goes on.
        if self.errflag == 0:
            self.removeAllWidgets()


        ########### The startup protocol of the experimental screen when coming from a saved experimental setup. ###########
        #       Labels are added over the widgets as removal of a fileEntry widget object does not work  well.
        else:
            self.addLabel("1", "")
            self.addLabel("2", "")
            self.addLabel("3", "")    

        # Creating the backbone of the pressure versus time graph (label, plot, unit selector.)
        self.addLabel("l0", "Pressure vs. Time", row = 0, column = 0, colspan = 2)                      
        axes0 = self.addPlot("pressure", 0, 0, row = 1, column = 1,  width = 1, height= 0.91803398875 )
        self.addOptionBox("Pressure Units", 
        ["- Units -", "mTorr", "Torr", "kTorr", 
        "\u03BC"+"Bar", "mBar", "Bar", 
        "Pa", "kPa", "Mpa",
        "\u03BC"+"bar", "mbar", "bar"]
        , row = 1, column = 0)

        # Creating the backbone of the flow rate versus time graph (label, plot, unit selector.)
        self.addLabel("k0", "Flow Rates vs. Time", row = 2, column = 0, colspan = 2)
        axes1 = self.addPlot("flow rates", 0,0, row = 3, column = 1, width = 1, height= 0.91803398875 )
        self.addOptionBox("Flow Units", 
        ["- Units -", "SCCM", "SLM", 
        "SCMM", "SCFH", "SCFM", "SLM"]
        , row = 3, column = 0)
        

        # Provide initial values for the two graphs (to be deleted when the automatic update functionality is in full effect.)
        reP(axes0)
        reFC(axes1)
        
        # Create responsive behavior for the unit selection optionBoxes.
        self.setOptionBoxChangeFunction("Flow Units", FU)
        self.setOptionBoxChangeFunction("Pressure Units", PU)
        
        # Start time of experiment for internal puposes. Start time of experimental data will be recieved through machine.
        self.data.beginExperiment()
        self.start = time.time()
        
        # First attempt at automatic update functionality.
        while(time.time()-self.start <= (60*int(self.cycles)*int(self.lengthEach))):
            time.sleep(2)
            reP(axes0)
            reFC(axes1)
        
                                    #########################################
                                    ################ FLOW RATE ##############     
                                    ######################################### 
    def render2fc2(self):
        """
        input:
                none
        
        output:
                gas behvior selection screen

        This function is designed to produce a generic approach to choosing the behavior of each gas controlled by the MFCs, given by
        the previous page. The page will allow the user to select different behaviors for the individual gases within the time of one 
        cycle (as given by self.lengthEach).
        """
        def newGasRow():
            """
            input:
                    none
            output:
                    new opportunity to select the flow rate behavior of a gas

            This function is designed to allow the user to determine the behavior of a gas governed by an MFC.
            """
            self.colCtr = 0
            self.addLabel("l11" + str(self.pressureSerial), "Port " + str(self.gasIndex[self.iter]), row = self.rowCtr)
            self.addLabel("l12"+ str(self.pressureSerial), "Gas: " +  str(self.gasDict[self.gasIndex[self.iter]]), row = self.rowCtr +1)
            self.colCtr += 1
            self.addVerticalSeparator(column = self.colCtr, rowspan = 3, row = self.rowCtr)
            self.colCtr += 1
            self.addLabel("l13" + str(self.pressureSerial), "Type of Flow Behavior: ", row= self.rowCtr, column = self.colCtr)
            self.colCtr += 1
            self.addOptionBox("TB"+str(self.pressureSerial), ["- Select an Option -", "Static", "Linear", "Exponential", "Periodic"], row = self.rowCtr, column=self.colCtr)
            self.rowCtr += 1
            self.setOptionBoxChangeFunction("TB"+str(self.pressureSerial), myChangeFunc)
        
        def heave(btn):
            """
            input:
                    none
            output:
                    none
            
            This function occurs when the "start experiment" button is clicked. It redirects the user to the experiment screen. 
            """
            self.finalDestination()
            

        def bigPush():
            """
            input:
                    none
            output:
                    either creates a new opportunity for the user to select the desired gas behavior or creates a "start experiment button"

            This function is designed to determine the progess of the gas selection process.  If it is complete (i.e. there are no more gases
            to determine the behavior of and the cycle time limit has been reached for the current gas,) the function will give the user the 
            option to continue to the experiment display screen.

            * Thought * I could redirect the user directly to the experimental screen without the need for them to interact. * Thought *
            """
            stop = int(self.getSpinBox("ET" + str(self.pressureSerial)))
            mag1 = 0
            units1 = ""
            oscillations = 0
            save_criteria = True
            mag0 = self.getEntry("DFR" + str(self.pressureSerial)) 
            units0 = self.getOptionBox("Units" + str(self.pressureSerial))
            

            if self.behavior == "Linear" or self.behavior == "Exponential":
                mag1 = self.getEntry("'DFR" + str(self.pressureSerial)) 
                units1 = self.getOptionBox("'Units" + str(self.pressureSerial))

            elif self.behavior == "Periodic":
                mag1 = self.getEntry("'DFR" + str(self.pressureSerial)) 
                units1 = self.getOptionBox("'Units" + str(self.pressureSerial))
                oscillations =  int(self.getSpinBox("Oscillations" + str(self.pressureSerial)))

            if mag0 == None or units0 == None or stop == 0:
                save_criteria = False
                self.warningBox("Invalid Entry", "Please make sure you have entered a value for pressure, units, and end time." )
            elif (self.behavior == "Linear" or self.behavior == "Exponential" or self.behavior == "Periodic") and (mag1 == None or units1 == None):
                save_criteria = False
                self.warningBox("Invalid Entry", "Please make sure you have entered a value for pressure and units." )
            elif self.behavior == "Periodic" and oscillations == 1 :
                save_criteria = self.yesNoBox("Invalid Entry", "Are you sure you only want 1 oscillation?" )

            self.saveSerial += 1
            
            if save_criteria:
                self.pressureSerial += 1
                self.initialTime = stop
                self.data.setMFCBehaviorDict(self.gasDict[self.gasIndex], self.gasIndex, self.behavior, self.initialTime, stop, mag0, units0, mag1, units1, oscillations)
                self.removeButton("Okay")
                self.rowCtr += 1
                self.addHorizontalSeparator(row = self.rowCtr, column = 0,colspan=8, colour="black",)
                self.rowCtr += 1
                if self.initialTime == self.lengthEach:
                    try:
                        self.iter += 1
                        self.gasIndex[self.iter]  
                        self.initialTime = 0
                        newGasRow()
                    except IndexError:
                        self.rowCtr -= 4
                        self.data.updateMaster()
                        self.addButton("Start Experiment", heave, row = self.rowCtr, column = 8)
                    else:
                        newGasRow()
        
        def flowSelecter():
            """
            input:
                    none
            output:
                    place to enter flow rate and means of selecting units
            
            This is a function of reused code, used to generate a way of collecting data on flow rate including magnitude and units.
            """
            self.addNumericEntry("DFR" + str(self.pressureSerial), row = self.rowCtr, column=self.colCtr)
            # self.addOptionBox("DFR" + str(self.pressureSerial) , [ "- Magnitude -", "1", "2", "5", "10", "100", "200", "500", "1000", "5000"],row = self.rowCtr,column = self.colCtr)
            self.colCtr += 1
            self.addOptionBox("Units" + str(self.pressureSerial), ["- Units -", "SCCM", "SLM", "SCMM", "SCFH", "SCFM", "SLM"],row = self.rowCtr, column= self.colCtr)
            self.colCtr += 1

        def flowSelecter1():
            """
            input:
                    none
            output:
                    place to enter flow rate and means of selecting units
            
            This is a function of reused code, used to generate a way of collecting data on flow rate including magnitude and units.
            (duplicate needed to keep widget names unique)
            """
            self.addNumericEntry("'DFR" + str(self.pressureSerial), row = self.rowCtr, column=self.colCtr)
            # self.addOptionBox("'DFR" + str(self.pressureSerial) , [ "- Magnitude -", "1", "2", "5", "10", "100", "200", "500", "1000", "5000"],row = self.rowCtr,column = self.colCtr)
            self.colCtr += 1
            self.addOptionBox("'Units" + str(self.pressureSerial), ["- Units -", "SCCM", "SLM", "SCMM", "SCFH", "SCFM", "SLM"],row = self.rowCtr, column= self.colCtr)
            self.colCtr += 1

        def timeKeeper():
            """
            input:
                    none
            output:
                    start time and place to enter stop time for a behavior
            
            This is a function of reused code, used to generate a way of collecting data on end time of a specific behavior.
            """
            self.addLabel("l4"+ str(self.pressureSerial), "Start Time: "  + str(self.initialTime),row = self.rowCtr, column = self.colCtr)
            self.colCtr += 1
            self.addLabel("l5"+ str(self.pressureSerial), "End Time: ", row = self.rowCtr, column = self.colCtr)
            self.colCtr += 1
            self.addSpinBoxRange("ET" + str(self.pressureSerial), int(self.initialTime), int(self.lengthEach),row = self.rowCtr, column = self.colCtr)
            self.colCtr += 1
            self.addButton("Okay", bigPush, row = self.rowCtr, column = self.colCtr)
            self.setButtonBg("Okay", "LimeGreen")
        
        def periodic():
            """
            input:
                    none
            output:
                    means of entering data needed to perform periodic alteration of flow
            """
            self.colCtr = 2
            self.addLabel("l1"+str(self.pressureSerial), "Minimum:",row = self.rowCtr, column = self.colCtr)
            self.colCtr += 1
            flowSelecter()
            self.addLabel("l2"+str(self.pressureSerial), text="Maximum:",row = self.rowCtr, column = self.colCtr)
            self.colCtr += 1
            flowSelecter1()
            self.rowCtr += 1
            self.colCtr = 2
            self.addLabel("l3"+str(self.pressureSerial),"Number of Oscillations:", row = self.rowCtr, column = self.colCtr)
            self.colCtr += 1
            self.addSpinBoxRange("Oscillations" + str(self.pressureSerial), 1, 10000, row = self.rowCtr, column = self.colCtr)
            self.colCtr += 1
            timeKeeper()
        
        def exponential():
            """
            input:
                    none
            output:
                    means of entering data needed to perform exponential alteration of flow
            """
            linear()

        def linear():
            """
            input:
                    none
            output:
                    means of entering data needed to perform linear alteration of flow
            """
            self.colCtr = 2
            self.addLabel("l1"+str(self.pressureSerial), "Initial Flow Rate: ",row = self.rowCtr, column = self.colCtr)
            self.colCtr += 1
            flowSelecter()
            self.addLabel("l2"+str(self.pressureSerial),  "Final Flow Rate: ",row = self.rowCtr, column = self.colCtr)
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
                    means of entering data needed to perform static alteration of flow
            """
            self.colCtr = 2
            self.addLabel("l1"+ str(self.pressureSerial), "Desired Flow Rate:", row = self.rowCtr, column = self.colCtr)
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
                    specified type of flow behavior, based on user input into optionBox

            This function occurs in response to the user selecting a behavior entry from the option box and provides the 
            cooresponding data entry interface for the user to interact with.

            * TO DO * Enable user to change their mind and select a different option. * TO DO *
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
            self.render2fc1()
        
        # Code for initializing the flow behavior selection screen #
        self.removeAllWidgets()

        self.addButton("\u21A9", back)
        self.setButtonBg("\u21A9", "Red")

        self.addLabel("l0","Please select the desired behavior for each of the gasses in turn", row = 0, column = 2)
        self.rowCtr = 1
        self.pressureSerial = 0
        newGasRow()
        


    def render2fc1(self):
        """
        input:
                none
        output:
                array of check-boxes that allow user to choose which gases are loaded in MFC ports

        This function allows the user to select the port and type of gas that the MFCs are connected to. This data is saved in 
        self.gasDict for later use.
        """
        self.myDict = {1:0, 2:0, 3:0,4:0, 5:0, 6:0,7:0, 8:0}
        self.gasCtrDict = {1:None, 2:None, 3:None, 4:None, 5:None, 6:None, 7:None, 8:None}
        self.gasCtr = 0
        self.gasDict = {1:None, 2:None, 3:None, 4:None, 5:None, 6:None, 7:None, 8:None}
        self.slaveBool = {1:False, 2:False, 3:False, 4:False, 5:False, 6:False, 7:False, 8:False}
        self.slaveDict = {1:9, 2:9, 3:9, 4:9, 5:9, 6:9, 7:9, 8:9}
        self.gasIndex = []
        self.iter = 0
        
        def push():
            save_bool = True
            for i in range(1,9):
                if self.myDict[i] == 1:
                    if self.getOptionBox("Gases"+str(self.gasCtrDict[i])) == None:
                        save_bool = False
                        self.warningBox("Invalid Entry", "Make sure that you have chosen a gas for each active port.")
                    if save_bool:
                        self.gasDict[i] = self.getOptionBox("Gases"+str(self.gasCtrDict[i]))
            if save_bool:
                for i in range(1, 9):
                    if self.myDict[i] == 1:
                        self.gasIndex.append(i)
                if self.errflag == 1:
                    self.errflag = 0
                    self.finalDestination()
                else:
                    self.render2fc2()
        
        def myLittleFunc(change):
            """
            input:
                    none
            output:
                    displays or hides selection box for MFC ports depending upon value of corresponding check-box

            This function occurs when a check-box next to a port is toggled.  The result is to hide or display the gas selection 
            optionBox, depending upon its previous visibility. 
            
            This function also updates self.myDict with the value 0/1 dpending on whether there is (1) or is not (0) a gas present 
            at a particular port.

            Additionally, this function employs self.gasCtrDict to save the gas serial number corresponding to the active MFC ports.
            In this way, it is possible to trace back the gas type to a correspondingly labeled optionBox ("Gases(gas Serial)") as 
            accomplished upon completion of this page. 
            """
            rowRef = {1:2, 2:2, 3:3, 4:3, 5:4, 6:4, 7:5, 8:5}
            col = 4
            for i in range(1,9):
                if self.getCheckBox("Port " + str(i)) and self.myDict.get(i) == 0:
                    self.myDict[i] = 1
                    if i % 2 == 1:
                        col = 2
                    rows = rowRef[i]
                    self.addOptionBox("Gases" + str(self.gasCtr), ["- Gases -", "- Commonly Used -", "Air", "Carbon Dioxide", "Helium", "Hydrogen", "Nitrogen", "Oxygen", "-Commonly Used -","Actylene", "Air", "Ammonia", "Argon", "Arsine", "Boron Trichloride", "Bromine", "Carbon Dioxide", "Carbon Monoxide", "Carbon Tetrachloride", "Carbon Tetraflouride", "Chlorine", "Chlorodifluoromethane", "Chloropentafluoromethane", "Cyanogen", "Deuterium", "Diborane", "Dibromane", "Dibromodifluoromethane", "Dichlorodifluoromethane", "Dichlorofluoromethane", "Dichloromethysilane", "Dichlorosilane", "Dichlorotetrafluoroethane", "Difluoroethylene", "Dimethylpropane", "Ethane", "Fluorine", "Fluoroform", "Freon - 11", "Freon - 12", "Freon - 13", "Freon - 14", "Freon - 21", "Freon - 22", "Freon - 23", "Freon - 113", "Freon - 114", "Freon - 115", "Freon - 116", "Freon - C318", "Freon - 1132A", "Helium", "Hexafluoroethane", "Hydrogen", "Hydrogen Bromide", "Hydrogen Chloride", "Hydrogen Fluoride", "Isobutylene", "Krypton", "Methane", "Methyl Fluoride", "Molybdenum Hexafluoride", "Neon", "Nitric Oxide", "Nitrogen", "Nitrogen Dioxide", "Nitrogen Trifluoride", "Nitrous Oxide", "Octafluorocyclobutane", "Oxygen", "Pentane", "Perfluoropropane", "Phosgene", "Phosphine", "Propane", "Propylene", "Silane", "Silicon Tetrachloride", "Silicon Tetrafluoride", "Sulfur Dioxide", "Sulfur Hexafluoride", "Trichlorofluoromethane", "Trichlorosilane", "Tungsten Hexafluoride", "Xenon"], row = rows, column = col)
                    self.gasCtrDict[i] = self.gasCtr
                    self.gasCtr += 1
                elif self.getCheckBox("Port " + str(i)) != True and self.myDict.get(i) == 1:
                    self.myDict[i] = 0
                    if i % 2 == 1:
                        col = 2
                    rows = rowRef[i]
                    self.addLabel(str(self.gasCtr), "", row= rows, column = col)
                    self.gasCtrDict[i] = None
                    self.gasCtr += 1
        
        def back(btn):
            if self.errflag == 0:
                self.render2fc()
            else:
                self.render2p1() 
            
        
        # Initialize the widgets of the window
        self.removeAllWidgets()

        self.addButton("\u21A9", back)
        self.setButtonBg("\u21A9", "Red")

    
        self.addLabel("title", "Select the Working MFCs", row = 0, column = 1, colspan=3)
        self.addCheckBox("Port 1", row = 2, column = 1)
        self.addCheckBox("Port 3", row = 3, column = 1)
        self.addCheckBox("Port 5", row = 4, column = 1)
        self.addCheckBox("Port 7", row = 5, column = 1)
        self.addCheckBox("Port 2", row = 2, column = 3)
        self.addCheckBox("Port 4", row = 3, column = 3)
        self.addCheckBox("Port 6", row = 4, column = 3)
        self.addCheckBox("Port 8", row = 5, column = 3)
        self.addButton("Submit", push, row = 6, column = 2)
        self.setButtonBg("Submit", "LimeGreen")

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
            
            This function serves the primary purpose of saving the cycle data while also advancing the user interface to the next page.
            """
            self.cycles = self.getSpinBox("Number of Cycles")
            self.lengthEach = self.getSpinBox("Duration of One Cycle (minutes)")
            entry_bool = True

            if self.cycles == '1' and self.lengthEach == '1':
                entry_bool = self.yesNoBox("Consider Revising", "Are you sure you want " + self.cycles + " cycle for " + self.lengthEach + " minute?")
                self.saveSerial += 1
            elif self.cycles != '1' and self.lengthEach == '1':
                entry_bool = self.yesNoBox("Consider Revising", "Are you sure you want " + self.cycles + " cycles for " + self.lengthEach + " minute each?")
                self.saveSerial += 1
            elif self.cycles == '1' and self.lengthEach != '1':
                entry_bool = self.yesNoBox("Consider Revising", "Are you sure you want " + self.cycles + " cycle for " + self.lengthEach + " minutes each?")
                self.saveSerial += 1

            if entry_bool:
                self.render2fc1()
            
        
        
        self.removeAllWidgets()
        def back(btn):
            self.render1()

        self.addButton("\u21A9", back)
        self.setButtonBg("\u21A9", "Red")

        self.addLabel("Select the number of cycles and the duration of each one.", row = 0, column = 1)
        self.addLabel("", "Number of Cycles")
        self.addSpinBoxRange("Number of Cycles",1,100, row = 1, column= 1)
        self.addLabel("1", "Duration of one Cycle (minutes")
        self.addSpinBoxRange("Duration of One Cycle (minutes)",1, 100, row = 2, column = 1)
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
                    either creates a new opportunity for the user to select the desired gas behavior or creates a "start experiment button"

            This function is designed to determine the progess of the gas selection process.  If it is complete (i.e. there are no more gases
            to determine the behavior of and the cycle time limit has been reached for the current gas,) the function will give the user the 
            option to continue to the experiment display screen.

            * Thought * I could redirect the user directly to the experimental screen without the need for them to interact. * Thought *
            """
            
            stop = int(self.getSpinBox("ET" + str(self.pressureSerial)))
            mag1 = 0
            units1 = ""
            oscillations = 0
            mag0 = self.getEntry("DFR" + str(self.pressureSerial)) 
            units0 = self.getOptionBox("Units" + str(self.pressureSerial))
            save_criteria = True

            if self.behavior == "Linear" or self.behavior == "Exponential":
                mag1 = self.getEntry("'DFR" + str(self.pressureSerial)) 
                units1 = self.getOptionBox("'Units" + str(self.pressureSerial))

            elif self.behavior == "Periodic":
                mag1 = self.getEntry("'DFR" + str(self.pressureSerial)) 
                units1 = self.getOptionBox("'Units" + str(self.pressureSerial))
                oscillations =  int(self.getSpinBox("Oscillations" + str(self.pressureSerial)))

            if mag0 == None or units0 == None or stop == 0:
                save_criteria = False
                self.warningBox("Invalid Entry", "Please make sure you have entered a value for pressure, units, and end time." )
            elif (self.behavior == "Linear" or self.behavior == "Exponential" or self.behavior == "Periodic") and (mag1 == None or units1 == None):
                save_criteria = False
                self.warningBox("Invalid Entry", "Please make sure you have entered a value for pressure and units." )
            elif self.behavior == "Periodic" and oscillations == 1 :
                save_criteria = self.yesNoBox("Consider Revising", "Are you sure you only want 1 oscillation?" )
                
            self.saveSerial += 1

            if save_criteria:
                self.pressureSerial += 1
                self.data.setPressureBehaviorList(self.behavior, self.initialTime, stop, mag0, units0, mag1, units1, oscillations)
                self.initialTime = stop
                self.removeButton("Okay")
                if self.initialTime == self.lengthEach:
                    self.data.updateMaster()
                    self.addButton("Select MFCs", press)
                else:
                    self.rowCtr += 1
                    self.colList.append(self.colCtr)
                    self.addHorizontalSeparator(self.rowCtr,0,str(max(self.colList)), colour="black")
                    self.rowCtr += 1
                    newRow()

        def back(btn):
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
            
            This is a function of reused code, used to generate a way of collecting data on pressure including magnitude and units.
            """
            # self.addOptionBox("DFR" + str(self.pressureSerial) , [ "- Magnitude -", "1", "2", "5", "10", "100", "200", "500", "1000", "5000"],row = self.rowCtr,column = self.colCtr)
            self.addNumericEntry("DFR" + str(self.pressureSerial),row = self.rowCtr, column = self.colCtr)
            self.colCtr += 1
            self.addOptionBox("Units" + str(self.pressureSerial), ["- Units -", "mTorr", "Torr", "kTorr", "\u03BC"+"Bar", "mBar", "Bar", "Pa", "kPa", "Mpa","\u03BC"+"bar", "mbar", "bar"],row = self.rowCtr, column= self.colCtr)
            self.colCtr += 1

        def pressureSelecter1():
            """
            input:
                    none
            output:
                    place to enter pressure and means of selecting units
            
            This is a function of reused code, used to generate a way of collecting data on pressure including magnitude and units.
            (duplicate needed to keep widget names unique)
            """
            # self.addOptionBox("'DFR" + str(self.pressureSerial) , [ "- Magnitude -", "1", "2", "5", "10", "100", "200", "500", "1000", "5000"],row = self.rowCtr,column = self.colCtr)
            self.addNumericEntry("'DFR" + str(self.pressureSerial),row = self.rowCtr, column = self.colCtr)
            self.colCtr += 1
            self.addOptionBox("'Units" + str(self.pressureSerial), ["- Units -", "mTorr", "Torr", "kTorr", "\u03BC"+"Bar", "mBar", "Bar", "Pa", "kPa", "Mpa","\u03BC"+"bar", "mbar", "bar"],row = self.rowCtr, column= self.colCtr)
            self.colCtr += 1

        def timeKeeper():
            """
            input:
                    none
            output:
                    start time and place to enter stop time for a behavior
            
            This is a function of reused code, used to generate a way of collecting data on end time of a specific behavior.
            """
            self.addLabel("l4"+ str(self.pressureSerial), "Start Time: "  + str(self.initialTime),row = self.rowCtr, column = self.colCtr)
            self.colCtr += 1
            self.addLabel("l5"+ str(self.pressureSerial), "End Time: ", row = self.rowCtr, column = self.colCtr)
            self.colCtr += 1
            self.addSpinBoxRange("ET" + str(self.pressureSerial), int(self.initialTime), int(self.lengthEach),row = self.rowCtr, column = self.colCtr)
            self.colCtr += 1
            self.addButton("Okay", bigPush, row = self.rowCtr, column = self.colCtr)
            self.setButtonBg("Okay", "LimeGreen")
        
        def periodic():
            """
            input:
                    none
            output:
                    means of entering data needed to perform periodic alteration of pressure
            """
            self.colCtr = 0
            self.addLabel("l1"+str(self.pressureSerial), "Minimum:",row = self.rowCtr, column = self.colCtr)
            self.colCtr += 1
            pressureSelecter()
            self.addLabel("l2"+str(self.pressureSerial), text="Maximum:",row = self.rowCtr, column = self.colCtr)
            self.colCtr += 1
            pressureSelecter1()
            self.rowCtr += 1
            self.colCtr = 0
            self.addLabel("l3"+str(self.pressureSerial),"Number of Oscillations:", row = self.rowCtr, column = self.colCtr)
            self.colCtr += 1
            self.addSpinBoxRange("Oscillations" + str(self.pressureSerial), 1, 10000, row = self.rowCtr, column = self.colCtr)
            self.colCtr += 1
            timeKeeper()
        
        def exponential():
            """
            input:
                    none
            output:
                    means of entering data needed to perform exponential alteration of pressure
            """
            linear()

        def linear():
            """
            input:
                    none
            output:
                    means of entering data needed to perform linear alteration of pressure
            """
            self.colCtr = 0
            self.addLabel("l1"+str(self.pressureSerial), "Initial Pressure: ",row = self.rowCtr, column = self.colCtr)
            self.colCtr += 1
            pressureSelecter()
            self.addLabel("l2"+str(self.pressureSerial),  "Final Pressure: ",row = self.rowCtr, column = self.colCtr)
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
                    means of entering data needed to perform static alteration of pressure
            """
            self.colCtr = 0
            self.addLabel("l1"+ str(self.pressureSerial), "Desired Pressure:", row = self.rowCtr, column = self.colCtr)
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

        This function creates the screen in which the user can enter the data about the number of cycles and the time of each cycle.
        This data is saved as self.cycles and self.lengthEach, respectively.
        """
        def push(btn):
            """
            input:
                    none
            output:
                    moves to pressure behavior screen
            
            This function occurs when the user presses the "Okay" button after selecting the desired number and duration of cycles and
            serves the purpose of saving this data while advancing the user interface to the next page.
            """
            self.cycles = self.getSpinBox("Number of Cycles")
            self.lengthEach = self.getSpinBox("Duration of One Cycle (minutes)")
            entry_bool = True

            if self.cycles == '1' and self.lengthEach == '1':
                entry_bool = self.yesNoBox("Consider Revising", "Are you sure you want " + self.cycles + " cycle for " + self.lengthEach + " minute?")
                self.saveSerial += 1
            elif self.cycles != '1' and self.lengthEach == '1':
                entry_bool = self.yesNoBox("Consider Revising", "Are you sure you want " + self.cycles + " cycles for " + self.lengthEach + " minute each?")
                self.saveSerial += 1
            elif self.cycles == '1' and self.lengthEach != '1':
                entry_bool = self.yesNoBox("Consider Revising", "Are you sure you want " + self.cycles + " cycle for " + self.lengthEach + " minutes each?")
                self.saveSerial += 1

            if entry_bool:
                self.removeAllWidgets(current = False)
                self.render2p1()
            
        def back(btn):
            self.render1()
        
        # Cycle information input initialization
        self.removeAllWidgets()

        self.addButton("\u21A9", back)
        self.setButtonBg("\u21A9", "Red")

        self.addLabel("Select the number of cycles and the duration of each one.", row = 0, column = 1)
        self.addLabel("", "Number of Cycles")
        self.addSpinBoxRange("Number of Cycles",1,100, row = 1, column= 1)
        self.addLabel("1", "Duration of one Cycle (minutes")
        self.addSpinBoxRange("Duration of One Cycle (minutes)",1, 100, row = 2, column = 1)
        self.addButton("Okay", push, colspan = 2)
        self.setButtonBg("Okay", "LimeGreen")

        
        

    def render1(self):
        """
        input:
                none
        output:
                depending on the user's selection of experiment type, the output will vary

        This function is designed to provide the user with an interface with which to select the type of experiment they are performing,
        whether it is dependent upon pressure or flow rate.
        """
        self.data.setPressureCtrlBoolean(False)
        
        def press(btn):
            """
            input:
                    none
            output:
                    the user's selection of experiment

            This function is designed to provide the user with an interface with which to select the type of experiment they are performing,
            whether it is dependent upon pressure or flow rate. 
            """
            selection = self.getRadioButton("options")
            if selection == "Pressure":
                self.data.setPressureCtrlBoolean(True)
                self.render2p()
            else:
                self.data.setPressureCtrlBoolean(False)
                self.render2fc()
        
        def back(btn):
            self.removeAllWidgets()
            self.render0()
        
        self.removeAllWidgets()

        self.addButton("\u21A9", back)
        self.setButtonBg("\u21A9", "Red")

        self.addLabel("title", "What is the independent variable in this experiment", row = 0, column = 1)
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

        This function is designed to give the user a place to submit a previously used experimental setup and avoid the hassel of 
        creating a custom experiment every time they use this program.

        This section is seperate, as the removal of a fileEntry widget proved challenging. 
        """
        def heave(btn):
            """
            input:
                    none
            output:
                    experiment interface
            
            This function occurs after the user selects the "Start Experiment" button.  This function is designed to redirect the user
            to the experiment interface.

            The errflag is set to 1 to denote that the gui object require careful handling as it will have a fileEntry widget which I
            do not know how to remove.
            """
            self.errflag = 1
            self.removeAllWidgets()
            self.finalDestination()
        
        self.removeAllWidgets()

        self.addLabel("tit", "Select The Experimental Setup", row = 0, column = 1)
        self.addLabel("", "Saved Experiment", row = 1, column = 0)
        entry = self.addFileEntry("Saved Experiment", row = 1, column = 1)
        self.addButton("Start Experiment", heave, row = 2, column = 0)
        self.setButtonBg("Start Experiment", "LimeGreen", colspan = 2)


    
    
    def render0(self):
        """
        input:
                none
        output:
                depending on the user's selection of experiment type, the output will vary

        This function is designed to provide the user with an interface with which to select the type of experiment they are performing.
        
        The choice is between a custom and saved experiment with custom experiments being created piece by piece and saved experiments 
        accessed though a file saved on the computer.
        """
        def press(btn):
            """
            input:
                    none
            output:
                    depending on the user's selection of experiment type, the output will vary

            This function is designed to provide the user with an interface with which to select the type of experiment they are performing.
            
            The choice is between a custom and saved experiment with custom experiments being created piece by piece and saved experiments 
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
        self.addLabel("title", "Welcome to the Experimental Setup Menu")
        self.addLabel("subtitle", "Please select the experiment you wish to perform.")
        self.addRadioButton("option", "Custom Experiment")
        self.addRadioButton("option", "Saved Experiment")
        self.addButton("Start", press)
        self.setButtonBg("Start", "LimeGreen")
        
        self.go()