# Ikarus Autopilot (Version 1.2)

import time
from threading import Thread
import threading
from gps import *
import os
import RPi.GPIO as gpio
import os

gpsd = None
autorunning = False
auto = None
checkrunning = True
i = 0
inp = True

os.system("sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock")
# bereitet GPS vor

class GpsPoller(threading.Thread):
    # holt aktuelle GPS Daten
    def __init__(self):
        threading.Thread.__init__(self)
        global gpsd
        gpsd = gps(mode=WATCH_ENABLE)
        self.current_value = None
        self.running = True
        print "GPS gestartet"

    def run(self):
        global gpsd
        while gpsp.running:
            gpsd.next()
            bgrad = gpsd.fix.latitude
            lgrad = gpsd.fix.longitude
            zeit = gpsd.fix.time
            alt = gpsd.fix.altitude
            speed = gpsd.fix.speed
            climb = gpsd.fix.climb
            time.sleep(1)



class AutoPilot(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global autorunning
        autorunning = True
        while autorunning:
            # autopilot ist on, do stuff!
            # k = open("koordinaten.txt", "r")
            print "Autopilot gestartet... VERNICHTEN"
            os.system('python o.py')
            time.sleep(1)
            os.system('python stopo.py')
            time.sleep(1)


def startgps():
    global gpsp
    try:
        gpsp.start()
    except (KeyboardInterrupt, SystemExit):
        gpsp.running = False
        gpsp.join()


def startautopilot():
    global i
    global autorunning
    global autoc
    try:
        auto.start()
    except Exception as e:
        log = open("autopilotfehler.txt", "a")
        log.write("Autopilot fehlerhaft, wurde beendet zum " + str(i) + ". Mal\n Exception: " + str(e))
        log.close()
        autorunning = False
        auto.join()
        i += 1
        time.sleep(1)


def koordinatenull():
    while True:
        print "koordinatenull wird ausgefuehrt"
        try:
            bgradnull = gpsd.fix.latitude
            lgradnull = gpsd.fix.longitude
            zeitnull = gpsd.fix.time
            altitudenull = gpsd.fix.altitude
            startlog = open("startkoordinaten.txt", "w+")
            startlog.write(str(bgradnull) + "\n" + str(lgradnull) + "\nStartzeit: " + str(zeitnull)
                           + "\nStart Alt: " + str(altitudenull))
            startlog.close()
            break
        except:
            time.sleep(2)

auto = AutoPilot()
gpsp = GpsPoller()
startgps()
time.sleep(15)
koordinatenull()

def checkcheckcon():
    global inp
    global autorunning
    global checkrunning
    while checkrunning:
        if inp == True:
            inp = False
            time.sleep(2)
        elif inp == False:
            time.sleep(3)
            if inp == False:
                if autorunning == True:
                    pass
                else:
                    if checkrunning == True:
                        print "autopilot wird gestartet"
                        autorunning = True
                        os.system('python o.py')
                        time.sleep(2)
                        os.system('python stopo.py')
                        startautopilot() # autopilot ein!
                    else:
                        pass
            elif inp == True:
                time.sleep(1)


t1 = Thread(target=checkcheckcon)
t1.start()
print "checkchekcon gestartet"
while True:
    try:
        while True:
            # checkcon
            a = int(input("pls input\n"))
            if a == 1:
                inp = True
                if autorunning == True:
                    time.sleep(1)
                    print "autopilot wird beendet weil wieder input vorhanden ist!"
                    autorunning = False
                    auto.join()
            elif a == 2:
                checkrunning = False
                if autorunning == True:
                    autorunning = False
                    auto.join()
                if gpsp.running == True:
                    gpsp.running = False
                    gpsp.join()
                print "Beendet"
                break
            time.sleep(1)
        break

    except (KeyboardInterrupt, SystemExit):
        gpsp.running = False
        gpsp.join()
        autorunning = False
        auto.join()
        break

    except Exception as e:
        print "Autopilot: Fehler: " + str(e)
