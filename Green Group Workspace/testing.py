# import serial

# print(1)
# ser = serial.Serial(
#     port='/dev/cu.usbserial-AM00HUNS',
#     baudrate=9600,
#     parity=serial.PARITY_EVEN,
#     stopbits=serial.STOPBITS_ONE,
#     bytesize=serial.EIGHTBITS
# )
# print(2)
# ser.isOpen()
# myString = 'PU R <cr>'
# b = myString.encode('ascii')
# ser.write(b)
# print(3)
# ret = ser.read(4)
# ret = ret.decode('ascii')
# print(4)

# print(ret)



# Experimental Screen Cache

 # def finalDestination(self):
    #     """
    #     input:
    #             none
    #     output: 
    #             experimental screen
        
    #     This function creates the display for the experimental screen 
    #     including the labels for the pressure versus time and flow rate 
    #     versus time graph, the two graphs themselves, and selector 
    #     optionBoxs for the user to select the units they want to display 
    #     the data in on the screen.
    #     """
    #     def reP(axes):
    #         """
    #         input:
    #                 axes - a matplotlib axes figure object representing 
    #                 the graph of pressure versus time

    #         output:
    #                 updated pressure versus time graph

    #         This function should update the pressure versus time graph 
    #         with data from the machine.
            
    #         * It will require a function call init that gathers the *
    #         *   data from the machine (to be built in controller.)  *
    #         """

    #         x = np.arange(0,10,0.1) #Filler code
    #         axes.cla()
    #         axes0.set_ylabel("Pressure (" + str(self.units)+")")
    #         axes0.set_xlabel("Time (min)")
    #         axes.plot(x, np.cos(x)) # Filler function
    #         self.refreshPlot("pressure")
        
    #     def reFC(axes):
    #         """
    #         input:
    #                 axes - a matplotlib axes figure object representing 
    #                 the graph of flow rate versus time

    #         output:
    #                 none

    #         This function updates the flow rate versus time graph with 
    #         data from the machine.
            
    #         * It will require a function call init that gathers the *
    #         *   data from the machine (to be built in controller.)  *
    #         """

    #         x = np.arange(0,10,0.1)
    #         axes.cla()
    #         axes1.set_ylabel("Flow Rate (" + str(self.myRate) + ")")
    #         axes1.set_xlabel("Time (min)")
    #         for i in range(0,len(self.gasIndex)):
    #             axes.scatter(x, np.multiply(x,np.sin(x))+i, label = str(self.gasDict[self.gasIndex[i]]))
    #         axes.legend()
    #         self.refreshPlot("flow rates")

    #     def PU(btn):
    #         """
    #         input:
    #                 none

    #         output:
    #                 none
            
    #         This function occurs when the units of pressure have been 
    #         selected by the user from the "Pressure Units" optionBox 
    #         object. It will change the y-axis label on the pressure 
    #         versus time graph and update the data input function in 
    #         order to reflect the new units of pressure on the graph.
    #         """
    #         self.units = self.getOptionBox("Pressure Units")
    #         axes0.set_ylabel("Pressure (" + str(self.units)+")")
    #         self.refreshPlot("pressure")

    #     def FU(btn):
    #         """
    #         input:
    #                 none

    #         output:
    #                 none
            
    #         This function occurs when the units of flow rate have been 
    #         selected by the user from the "Flow Units" optionBox object.
    #         It will change the y-axis label on the flow rate versus time 
    #         graph and update the data input function in order to reflect 
    #         the new units of flow rate on the graph.
    #         """
    #         self.myRate = self.getOptionBox("Flow Units")
    #         axes1.set_ylabel("Flow Rate (" + str(self.myRate) + ")")
    #         self.refreshPlot("flow rates")

    #     ########## The startup protocol of the experimental screen when coming from a custom experimental setup. ###########
    #     #       The widgets are all destroyed despite throwing an unknown error. This error is not fatal, so the show goes on.
    #     if self.errflag == 0:
    #         self.removeAllWidgets()


    #     ########### The startup protocol of the experimental screen when coming from a saved experimental setup. ###########
    #     #       Labels are added over the widgets as removal of a fileEntry widget object does not work  well.
    #     else:
    #         self.addLabel("1", "")
    #         self.addLabel("2", "")
    #         self.addLabel("3", "")    

    #     # Creating the backbone of the pressure versus time graph (label, plot, unit selector.)
    #     self.addLabel("l0", "Pressure vs. Time", row = 0, column = 0, colspan = 2)                      
    #     axes0 = self.addPlot("pressure", 0, 0, row = 1, column = 1,  width = 1, height= 0.91803398875 )
    #     self.addOptionBox("Pressure Units", 
    #     ["- Units -", "mTorr", "Torr", "kTorr", 
    #     "\u03BC"+"Bar", "mBar", "Bar", 
    #     "Pa", "kPa", "Mpa",
    #     "\u03BC"+"bar", "mbar", "bar"]
    #     , row = 1, column = 0)

    #     # Creating the backbone of the flow rate versus time graph (label, plot, unit selector.)
    #     self.addLabel("k0", "Flow Rates vs. Time", row = 2, column = 0, colspan = 2)
    #     axes1 = self.addPlot("flow rates", 0,0, row = 3, column = 1, width = 1, height= 0.91803398875 )
    #     self.addOptionBox("Flow Units", 
    #     ["- Units -", "SCCM", "SLM"]
    #     , row = 3, column = 0)
        

    #     # Provide initial values for the two graphs (to be deleted when the automatic update functionality is in full effect.)
    #     reP(axes0)
    #     reFC(axes1)
        
    #     # Create responsive behavior for the unit selection optionBoxes.
    #     self.setOptionBoxChangeFunction("Flow Units", FU)
    #     self.setOptionBoxChangeFunction("Pressure Units", PU)
        
    #     # Start time of experiment for internal puposes. Start time of experimental data will be recieved through machine.
    #     self.stop()
    #     self.data.beginExperiment()

        
    #     # First attempt at automatic update functionality.
    #     while(time.time()-self.start <= (60*self.cycles*self.lengthEach)):
    #         self.iter += 1
    #         time.sleep(2)
    #         reP(axes0)
    #         reFC(axes1)
    #         print("Update Number: " + str(self.iter))