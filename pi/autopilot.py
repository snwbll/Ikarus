# Ikarus Autopilot (Version 2.0)

import sys
import time
from threading import Thread
import threading
from gps import *
import RPi.GPIO as gpio
import os

hostname = sys.argv[1]  # einfacheres optparser, im Terminal "python skript.py "argument" (in diesem Fall Host IP)
print "Verbindung mit " + hostname
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
            """
            bgrad = gpsd.fix.latitude
            lgrad = gpsd.fix.longitude
            zeit = gpsd.fix.time
            alt = gpsd.fix.altitude
            speed = gpsd.fix.speed
            climb = gpsd.fix.climb
            """
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
            print "Autopilot gestartet... VERNICHTEN!"
            os.system('python o.py')
            time.sleep(1)
            os.system('python stopo.py')
            print "Breitengrad? " + str(gpsd.fix.latitude)
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


def pingrouter():
    global autorunning
    global hostname
    host = hostname  # IP des steuernden Laptops
    while True:
        try:
            # pingt den Router an
            response = os.system("ping -c 1 " + host)
            if response == 0:
                # Host up
                os.system('python u.py')
                time.sleep(0.5)
                os.system('python stopu.py')
                pass
            else:
                # Host down, Autopilot einschalten
                autorunning = True
                startautopilot()  # Autopilot ein
                print "Autopilot wurde eingeschalten... Suche eine Verbindung."
                while True:
                    # pingt weiterhin den Router an, um den Autopiloten bei Verbindung wieder auszuschalten
                    response = os.system("ping -c 1 " + host)
                    if response == 0:
                        # Host up, Autopilot aus
                        autorunning = False
                        auto.join()
                        print "Autopilot wurde wieder ausgeschalten, beende"
                        sys.exit(1)
                        break

                    else:
                        pass
                    time.sleep(1)
            time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            gpsp.running = False
            gpsp.join()
            autorunning = False
            auto.join()
            break

p1 = Thread(target=pingrouter)
p1.start()


"""
   except (KeyboardInterrupt, SystemExit):
        gpsp.running = False
        gpsp.join()
        autorunning = False
        auto.join()
        break
"""