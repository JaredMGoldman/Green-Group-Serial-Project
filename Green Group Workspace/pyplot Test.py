# import appJar as aj
# import numpy as np
# import random
# import time


# # app = aj.gui()

# # x = range(0,10)
# # y = np.multiply(3,x)

# # axes = app.addPlot("P", 0,0)
# # fuck = axes.plot(x,y,label = "Fuck")
# # this = axes.plot(x, np.sin(x), label = "This")
# # shit = axes.plot(x, np.cos(y), label = "Shit")
# # axes.legend()

# # def grr(btn):
# #     axes.cla()
# #     app.refreshPlot("P")
# #     sleep(3)
# #     axes.plot(x, np.sin(x), label = "This")
# #     axes.legend()
# #     app.refreshPlot("P")

# # app.addButton("GAAAAAA", grr)
# # app.go()

# app = aj.gui()

# app.setFullscreen()
# myRate = "SLM"
# units = "Torr"


# def reP(axes):
#     x = np.arange(0,10,0.1)
#     axes.plot(x,x)
#     axes.cla()
#     axes.set_xlabel("Time (min)")
#     axes.set_ylabel("Pressure (" + str(units)+")")
#     axes.plot(x, np.cos(x))
#     app.refreshPlot("pressure")

# def reFC(axes):
#     x = np.arange(0,10,0.1)
#     axes.cla()
#     axes.set_xlabel("Time (min)")
#     axes.set_ylabel("Flow Rate (" + str(myRate) + ")")
#     for i in range(0,2):
#         axes.scatter(x, np.multiply(x,np.sin(x))+i, label = str("Hello"))
#     axes.legend()
#     app.refreshPlot("flow rates")

# def PU(btn):
#     global units
#     units = app.getOptionBox("Pressure Units")
#     axes0.set_ylabel("Pressure (" + str(units)+")")
#     app.refreshPlot("pressure")

# def FU(btn):
#     global myRate
#     myRate = app.getOptionBox("Flow Units")
#     axes1.set_ylabel("Flow Rate (" + str(myRate) + ")")
#     app.refreshPlot("flow rates")




# app.addLabel("l0", "Pressure vs. Time", row = 0, column = 0, colspan = 2)

# axes0 = app.addPlot("pressure", 0, 0, row = 1, column = 1, width = 1, height= 0.91803398875 )
# axes0.set_xlabel("Time (min)")
# axes0.set_ylabel("Pressure (" + str(units)+")")
# app.refreshPlot("pressure")
# app.addOptionBox("Pressure Units", 
# ["- Units -", "mTorr", "Torr", "kTorr", 
# "\u03BC"+"Bar", "mBar", "Bar", 
# "Pa", "kPa", "Mpa",
# "\u03BC"+"bar", "mbar", "bar"]
# , row = 1, column = 0 )

# app.addLabel("k0", "Flow Rates vs. Time", row = 2, column = 0, colspan = 2)
# axes1 = app.addPlot("flow rates", 0,0, row = 3, column = 1, width = 1, height= 0.91803398875 )
# mine = app.addOptionBox("Flow Units", 
# ["- Units -", "SLM", "SCCM", "SLM", 
# "SCMM", "SCFH", "SCFM"]
# , row = 3, column = 0)


# reFC(axes1)
# reP(axes0)


# app.setOptionBoxChangeFunction("Flow Units", FU)
# app.setOptionBoxChangeFunction("Pressure Units", PU)
# start = time.time()
# app.go()
# while(time.time()-start <= (60*int(15)*int(30))):
#     time.sleep(2)
#     # reP(axes0)
#     reFC(axes1)

sample = []

if type(sample) == list:
    print("Right")
if type(sample) != list:
    print("Wrong")
    print(str(type(sample)))