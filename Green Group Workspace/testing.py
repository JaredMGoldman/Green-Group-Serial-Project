# import appJar as aj

# from time import sleep

# self = aj.gui()

# def finalDestination():
#     print("Experiment Screen")

# def render2fc2():
#     print("Flow control")

# def push(btn):
#     save_bool = True
#     for i in range(1,9):
#         if myDict[i] == 1:
#             if self.getOptionBox("Gases"+str(gasCtrDict[i])) == None:
#                 save_bool = False
#                 self.warningBox("Invalid Entry", "Make sure that you have chosen a gas for each active port.")
#             elif slaveDict[i][2] and slaveDict[i][0] == None:
#                 save_bool = False
#                 self.warningBox("Invalid Entry", "Make sure that you have chosen a master for each slave port.")
#             elif slaveDict[i][2] and slaveDict[i][0] == None:
#                 save_bool = False
#                 self.warningBox("Invalid Entry", "Make sure that you have chosen a master for each slave port.")
#             if save_bool:
#                 gasDict[i] = self.getOptionBox("Gases"+str(gasCtrDict[i]))
#     if save_bool:
#         for i in range(1, 9):
#             if slaveDict[i][2]:
#                 slaveDict[i][0] = self.getOptionBox("Master"+str(i))
#                 slaveDict[i][1] = self.getEntry("Ratio" + str(i))
#             if myDict[i] == 1:
#                 gasIndex.append(i)
#         if errflag == 1:
#             errflag = 0
#             finalDestination()
#         else:
#             render2fc2()


# def removeSlaveDetails(index):
#     slaveDict[index][2] = False
#     self.removeCheckBox("Slave"+str(index))
#     self.removeLabel("M-name" + str(i))
#     self.removeOptionBox("Master" + str(index))
#     self.removeLabel(str(index))
#     self.removeEntry("Ratio" + str(index))

# def slaveFunc(btn):
#     for i in range(1,9):
#         if not slaveDict[i][2] and slaveDict[i][3]:
#             slaveDict[i][2] = True
#             slaveDict[i][3] = True
#             if i % 2 == 1:
#                 col = 1
#             else:
#                 col = 7
            
#             self.addLabel("M-name" + str(i), "Master Port:", row = rowRef[i]+1, column = col)
#             self.addOptionBox("Master" + str(i), portList, row = rowRef[i]+1, column = col+1)
#             self.addLabel(str(i), "Ratio:", row = rowRef[i]+1, column = col +2)
#             self.addNumericEntry("Ratio" + str(i), row = rowRef[i]+1, column = col +3)
#         elif slaveDict[i][2] and not slaveDict[i][3]:
#             removeSlaveDetails(i)



# def myLittleFunc(change):
#     """
#     input:
#             none
#     output:
#             displays or hides selection box for MFC ports depending upon value of corresponding check-box

#     This function occurs when a check-box next to a port is toggled.  The result is to hide or display the gas selection 
#     optionBox, depending upon its previous visibility. 
    
#     This function also updates self.myDict with the value 0/1 dpending on whether there is (1) or is not (0) a gas present 
#     at a particular port.

#     Additionally, this function employs self.gasCtrDict to save the gas serial number corresponding to the active MFC ports.
#     In this way, it is possible to trace back the gas type to a correspondingly labeled optionBox ("Gases(gas Serial)") as 
#     accomplished upon completion of this page. 
#     """

#     for i in range(1,9):
#         if self.getCheckBox("Port " + str(i)) and myDict.get(i) == 0:
#             myDict[i] = 1
#             if i % 2 == 1: col = 1
#             else: col = 7
#             rows = rowRef[i]
#             self.addOptionBox("Gases" + str(self.gasCtr), ["- Gases -", 
#             "- Commonly Used -", "Air", "Carbon Dioxide", "Helium", 
#             "Hydrogen", "Nitrogen", "Oxygen", "-Commonly Used -",
#             "Actylene", "Air", "Ammonia", "Argon", "Arsine", 
#             "Boron Trichloride", "Bromine", "Carbon Dioxide", 
#             "Carbon Monoxide", "Carbon Tetrachloride", 
#             "Carbon Tetraflouride", "Chlorine", "Chlorodifluoromethane", 
#             "Chloropentafluoromethane", "Cyanogen", "Deuterium", 
#             "Diborane", "Dibromane", "Dibromodifluoromethane", 
#             "Dichlorodifluoromethane", "Dichlorofluoromethane", 
#             "Dichloromethysilane", "Dichlorosilane", 
#             "Dichlorotetrafluoroethane", "Difluoroethylene", 
#             "Dimethylpropane", "Ethane", "Fluorine", "Fluoroform", 
#             "Freon - 11", "Freon - 12", "Freon - 13", "Freon - 14", 
#             "Freon - 21", "Freon - 22", "Freon - 23", "Freon - 113", 
#             "Freon - 114", "Freon - 115", "Freon - 116", "Freon - C318", 
#             "Freon - 1132A", "Helium", "Hexafluoroethane", "Hydrogen", 
#             "Hydrogen Bromide", "Hydrogen Chloride", "Hydrogen Fluoride", 
#             "Isobutylene", "Krypton", "Methane", "Methyl Fluoride", 
#             "Molybdenum Hexafluoride", "Neon", "Nitric Oxide", "Nitrogen", 
#             "Nitrogen Dioxide", "Nitrogen Trifluoride", "Nitrous Oxide", 
#             "Octafluorocyclobutane", "Oxygen", "Pentane", "Perfluoropropane", 
#             "Phosgene", "Phosphine", "Propane", "Propylene", "Silane", 
#             "Silicon Tetrachloride", "Silicon Tetrafluoride", "Sulfur Dioxide", 
#             "Sulfur Hexafluoride", "Trichlorofluoromethane", "Trichlorosilane", 
#             "Tungsten Hexafluoride", "Xenon"], row = rows, column = col)
            
#             portList = ["- Master -"]
#             for j in range(1, 9):
#                 if j != i:
#                     portList.append("Port " + str(j))
            
#             self.addCheckBox("Slave"+str(i), row = rows+1, column = col-1)
#             self.addLabel("M-name" + str(i), "Master Port:", row = rowRef[i]+1, column = col)
#             self.addOptionBox("Master" + str(i), portList, row = rowRef[i]+1, column = col+1)
#             self.addLabel(str(i), "Ratio:", row = rowRef[i]+1, column = col +2)
#             self.addNumericEntry("Ratio" + str(i), row = rowRef[i]+1, column = col +3)
#             # self.setCheckBoxChangeFunction("Slave" + str(i), slaveFunc)
#             slaveDict[i][3] = True
#             gasCtrDict[i] = gasCtr
#             gasCtr += 1
#         elif self.getCheckBox("Port " + str(i)) != True and myDict.get(i) == 1:
#             myDict[i] = 0
#             if i % 2 == 1:
#                 col = 1
#             else:
#                 col = 7
#             rows = rowRef[i]
#             slaveDict[i][3] = False
#             removeSlaveDetails(i)
#             self.addLabel(str(self.gasCtr), "", row= rows, column = col)
#             gasCtrDict[i] = None
#             gasCtr += 1


# def back(btn):
#             print("Back it up")  

# self.setFont(30)
# self.setFullscreen()
# self.removeAllWidgets()
# self.addCheckBox("Port 1", row = 2, column = 0)
# self.addCheckBox("Port 3", row = 5, column = 0)
# self.addCheckBox("Port 5", row = 8, column = 0)
# self.addCheckBox("Port 7", row = 11, column = 0)
# self.addCheckBox("Port 2", row = 2, column = 6)
# self.addCheckBox("Port 4", row = 5, column = 6)
# self.addCheckBox("Port 6", row = 8, column = 6)
# self.addCheckBox("Port 8", row = 11, column = 6)
# # self.setStretch("both")
# self.addButton("Submit", push, row = 12, colspan = 11 )
# # self.setStretch("none")

# for i in [1,2,3,4,7,8,9,10]:
#     for j in [2,3,5,6,8,9,11,12]:
#         self.addLabel("Placeholder" + str(i) +str(j), "     ", row = j, column = i)

# self.addLabel("Big Title", "MFC Configuration Menu", row = 0, colspan = 10)

# self.addHorizontalSeparator(row = 4, column = 0, colspan = 10)
# self.addHorizontalSeparator(row = 1, column = 0, colspan = 10)
# self.addHorizontalSeparator(row = 7, column = 0, colspan = 10)
# self.addHorizontalSeparator(row = 10, column = 0, colspan = 10)
# self.addVerticalSeparator(row = 2, column = 5, rowspan = 10)

# self.setButtonBg("Submit", "LimeGreen")

# for i in range(1,9):
#     self.setCheckBoxChangeFunction("Port " + str(i), myLittleFunc)

# global errflag 
# errflag = 0
# global myDict 
# myDict = {1:0, 2:0, 3:0,4:0, 5:0, 6:0,7:0, 8:0}
# global gasCtrDict 
# gasCtrDict = {1:None, 2:None, 3:None, 4:None, 5:None, 6:None, 7:None, 8:None}
# global gasCtr 
# gasCtr= 0
# global gasDict 
# gasDict = {1:None, 2:None, 3:None, 4:None, 5:None, 6:None, 7:None, 8:None}
# global slaveDict 
# slaveDict= {1:[9,0.0, False, False], 2:[9,0.0, False, False], 
#             3:[9,0.0, False, False], 4:[9,0.0, False, False], 
#             5:[9,0.0, False, False], 6:[9,0.0, False, False], 
#             7:[9,0.0, False, False], 8:[9,0.0, False, False]}       # Add Master/Ratio info at the end of this screen.  
#                                                                     # It's more efficient anyhow
# global gasIndex 
# gasIndex = []
# global iter 
# iter = 0
# global rowRef 
# rowRef = {1:2, 2:2, 3:5, 4:5, 5:8, 6:8, 7:11, 8:11}
# global col 
# col = 7

# self.go()

# # def push(btn):
# #     print("Push it to the limit")      



# # self.setSticky("")
# # self.setStretch("column")
# # # self.setSticky("sew")

myList = [[1,2,3], [4,5,6]]

print(len(myList))