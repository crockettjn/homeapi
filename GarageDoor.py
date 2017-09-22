import time
import RPi.GPIO as io
from flask import Flask, request, session

app = Flask(__name__)
io.cleanup()
io.setmode(io.BCM)
openStop = 5
closeStop = 6
relayPin = 4

io.setup(openStop, io.IN, pull_up_down=io.PUD_UP)
io.setup(closeStop, io.IN, pull_up_down=io.PUD_UP)
io.setup(relayPin, io.OUT)
io.output(relayPin, io.HIGH)

@app.route("/")
def index():
    return "API Home!"

@app.route("/garage/status")
def status():
    print('Get door status called')
    ds = getDoorStatus()
    print(ds)
    return "The door is " + ds

@app.route("/garage/toggle")
def toggle():
    toggleRelay(relayPin)
    return "Door Toggled"

def toggleRelay(relayPin):
    io.output(relayPin, io.LOW)
    time.sleep(1)
    io.output(relayPin, io.HIGH)

def getDoorStatus():
    f = open('doorState', 'r')
    doorState = f.readline()
    f.close()
    if io.input(openStop):
        ts = False
    else:
        ts = True
    time.sleep(0.5)
    if io.input(closeStop):
        bs = False
    else:
        bs = True

    if ts == True:
        writeFile('open')
        return('open')
    elif bs == True:
        writeFile('closed')
        return('closed')
    else:
        if doorState == 'open':
            return('closing')
        else:
            return('opening')

def writeFile(status):
    f = open('doorState', 'w')
    f.write(status)
    f.close()
