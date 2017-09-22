#!/usr/bin/env python

import time
import RPi.GPIO as io
from flask import Flask, request

app = Flask(__name__)

io.setmode(io.BCM)
openStop = 23
closeStop = 24
relayPin = 17

#io.setup(openStop, io.IN, pull_up_down=io.PUD_UP)
#io.setup(closeStop, io.IN, pull_up_down=io.PUD_UP)
#io.setup(relayPin, io.OUT)
#io.output(relayPin, io.HIGH)

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
    io.setup(relayPin, io.OUT)
    io.output(relayPin, io.HIGH)

    io.output(relayPin, io.LOW)
    time.sleep(1)
    io.output(relayPin, io.HIGH)
    doorState = getCurrentState()
    io.cleanup(relayPin)
    if doorState == 'open':
        return "Close Command Sent."
    elif doorState == 'closed':
        return "Open Command Sent."
    elif doorState == 'closing':
        return "Door Closing Stopped"
    elif doorState == 'opening':
        return "Door Opening Stopped"
    else:
        return "Error!"

def getDoorStatus():
    io.setup(openStop, io.IN, pull_up_down=io.PUD_UP)
    io.setup(closeStop, io.IN, pull_up_down=io.PUD_UP)
    doorState = getCurrentState()
    if io.input(openStop):
        ts = False
    else:
        ts = True
    time.sleep(0.5)
    if io.input(closeStop):
        bs = False
    else:
        bs = True
    io.cleanup(openStop)
    io.cleanup(closeStop)
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


def getCurrentState():
    f = open('doorState', 'r')
    doorState = f.readline().rstrip()
    f.close()
    return doorState

def writeFile(status):
    f = open('doorState', 'w')
    f.write(status)
    f.close()

if __name__=='__main__':
    app.run(host='0.0.0.0')
