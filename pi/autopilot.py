# Ikarus Autopilot (Version 2.0)

import os
import sys
import time
import subprocess
from threading import Thread
import threading
from gps import *
import RPi.GPIO as gpio

hostname = sys.argv[1]  # einfacheres optparser, im Terminal >python skript.py "argument"< (in diesem Fall Host IP)
gpsd = None
autorunning = False
i = 0

os.system("sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock")  # bereitet GPS vor


class GpsPoller(threading.Thread):
    # holt aktuelle GPS Daten
    def __init__(self):
        threading.Thread.__init__(self)
        global gpsd
        gpsd = gps(mode=WATCH_ENABLE)
        self.current_value = None
        self.running = True

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


# TODO entfernen
os.system("python o.py")
time.sleep(1)
os.system("python stopo.py")


class AutoPilot(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global autorunning
        autorunning = True
        while autorunning:
            # autopilot ein, do stuff!
            # k = open("koordinaten.txt", "r")
            print "Autopilot gestartet... VERNICHTEN!"
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
            startlog.write(str(bgradnull) + "\n" + str(lgradnull) + "\n" + str(altitudenull)
                           + "\n" + str(zeitnull))
            startlog.close()
            break
        except Exception as e:
            log = open("autopilotfehler.txt", "a")
            log.write("Startkoordinaten konnten nicht festgelegt werden. Exception: " + str(e))
            log.close()
            time.sleep(2)


auto = AutoPilot()
gpsp = GpsPoller()
startgps()
time.sleep(15)  # wartet t Sekunden damit das GPS Modul eine Verbindung zum Satelliten herstellen kann
koordinatenull()


def pingrouter():
    global autorunning
    global hostname
    host = hostname  # IP des steuernden Hosts (der Laptop)
    while True:
        try:
            # pingt den Router an
            pipe = subprocess.Popen("ping -c 1 " + host, stdout=subprocess.PIPE, shell=True,
                                    universal_newlines=True)
            response = pipe.wait()  # gibt 0 bei Verbindung und 1 bei keiner Verbindung aus
            if response == 0:
                # Host up
                pass
            else:
                # Host down, Autopilot ein
                autorunning = True
                startautopilot()
                while True:
                    # pingt weiterhin den Router an, um den Autopiloten bei Verbindung wieder auszuschalten
                    pipe = subprocess.Popen("ping -c 1 " + host, stdout=subprocess.PIPE, shell=True,
                                            universal_newlines=True)
                    response = pipe.wait()
                    if response == 0:
                        # Host up, Autopilot aus
                        autorunning = False
                        auto.join()
                        break
                    else:
                        pass
                    time.sleep(3)
            time.sleep(2)

        except (KeyboardInterrupt, SystemExit):
            # beendet alle laufenden Threads
            gpsp.running = False
            gpsp.join()
            autorunning = False
            auto.join()
            break


p1 = Thread(target=pingrouter)
p1.start()
