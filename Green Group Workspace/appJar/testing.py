import appJar as aj
from time import sleep

app = aj.gui()

app.addLabel("", "Test")

app.go()

app.addLabel("ye", "Sleep")
sleep(3)

app.widgetManager.reset()
app.addLabel("ye", "Wake")