import appJar as aj

from time import sleep

self = aj.gui()


def back(btn):
            print("Back it up")  

def push(btn):
    print("Push it to the limit")      
self.setFont(30)
self.setFullscreen()
self.removeAllWidgets()
# self.setSticky("n")
# self.setStretch("both")
self.addButton("\u21A9", back,colspan = 1)
# self.setStretch("none")
# self.setSticky("sew")
self.setButtonBg("\u21A9", "red")
self.addLabel("Select the number of cycles and the duration of each one.", row = 0, column = 1)
self.addLabel("", "Number of Cycles")
self.addSpinBoxRange("Number of Cycles",1,100, row = 1, column= 1)
self.addLabel("1", "Duration of one Cycle (minutes")
self.addSpinBoxRange("Duration of One Cycle (minutes)",1, 100, row = 2, column = 1)
self.setSticky("sew")
self.addButton("Okay", push, colspan = 2)
self.setButtonBg("Okay", "LimeGreen")
self.go()

# self.setSticky("")
# self.setStretch("column")
# # self.setSticky("sew")

# 



