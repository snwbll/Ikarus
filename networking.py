# -*- coding: utf-8 -*-

import os
import sys
import time
import select
import socket
import paramiko
from threading import Thread
from datetime import datetime

getgpsdatarunning = True
host = "192.168.1.120"  # dynamischer: raw_input("\ninet Adresse des Hosts: "), pi muss so eine statische IP haben
username = "pi"
password = "Snowball"
nodata = "Keine Daten"
gpsdata = [nodata, nodata, nodata, nodata, nodata, nodata, nodata, nodata, nodata, nodata, nodata, nodata]
sshverbindung = None
sshverbindung2 = None
sshverbindung3 = None
gpsverbindung = None


def initconnection():
    counter = 1
    while True:
        print("Verbindung mit %s wird aufgebaut..." % host)
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, username=username, password=password)
            ssh2 = paramiko.SSHClient()
            ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh2.connect(host, username=username, password=password)
            ssh3 = paramiko.SSHClient()
            ssh3.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh3.connect(host, username=username, password=password)
            paramiko.util.log_to_file("paramikolog.log")
            print("Verbunden mit %s\n" % host)
            global sshverbindung
            global sshverbindung2
            global sshverbindung3
            sshverbindung = ssh
            sshverbindung2 = ssh2
            sshverbindung3 = ssh3
            execute("sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock")  # GPS wird aktiviert
            gpscon = Thread(target=gpsconnection)
            gpscon.start()  # GPS - Verbindung wird aufgebaut, sobald eine normale Verbindung besteht
            break
        except paramiko.AuthenticationException:
            print("Authentifizierung fehlgeschalagen bei Verbindung mit " + host)
            sys.exit(1)
        except Exception as e:
            print("Verbindung fehlgeschlagen, warten auf " + host + " (Exception: " + str(e) + ")")
            counter += 1
            time.sleep(2)
        if counter > 10:
            print("Verbindung wiederholt fehlgeschlagen. Wird abgebrochen.")
            sys.exit(1)


def execute(command):
    try:
        stdin, stdout, stderr = sshverbindung.exec_command(command)
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
                if len(rl) > 0:
                    return stdout.channel.recv(1024)  # Output
    except Exception as e:
        print("Fehler in execute: " + str(e))


def gpsconnection():
    while True:
        print("GPS - Verbindung mit %s wird aufgebaut..." % host)
        try:
            gpsssh = paramiko.SSHClient()
            gpsssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            gpsssh.connect(host, username=username, password=password)
            print("GPS Verbunden mit %s\n" % host)
            global gpsverbindung
            gpsverbindung = gpsssh
            break
        except paramiko.AuthenticationException:
            print("Authentifizierung fehlgeschlagen bei GPS - Verbindung mit %s." % host)
            sys.exit(1)
        except Exception as e:
            print("GPS - Verbindung fehlgeschlagen, warten auf %s (Exception: " + str(e) % host)
            time.sleep(2)
    getgpsdata()


def getgpsdata():
    global getgpsdatarunning
    global gpsdata
    global gpsverbindung
    try:
        stdin, stdout, stderr = gpsverbindung.exec_command("python gpsdata.py", get_pty=True)  # Output lesen
        while True:
            while not stdout.channel.exit_status_ready():
                if stdout.channel.recv_ready():
                    rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
                    if len(rl) > 0:
                        a = stdout.channel.recv(1024)  # GPS Daten werden gelesen und in gpsdata[] gespeichert
                        a = a.replace("[", "")  # die [] der erhaltenen Liste der GPS Daten werden entfernt
                        a = a.replace("]\r\n", "")
                        gpsdata = a.split(", ")
                    if not getgpsdatarunning:
                        break
            break
    except Exception as e:
        print("Fehler in getgpsdata: " + str(e))
    print("Getgpsdata beendet.")


def execute_nooutput(command):
    try:
        # stdin, stdout, stderr =
        sshverbindung.exec_command(command)
    except Exception as e:
        print("Fehler in execute_nooutput: " + str(e))


def mtest():
    print("Motorentest: t = 3 Sekunden\nLinks\nRechts\nZurueck\nOben\nUnten\n")
    execute_nooutput("python mtest.py")


def startautopilot():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('google.com', 0))
    myip = s.getsockname()[0]  # die IP des Laptops
    execute_nooutput("python autopilot.py '" + myip + "'")  # übergibt die IP an den Autopiloten für Pingabfragen


def ping():
    os.system("ping ")
    a = str(datetime.now())
    response = execute("./ping")  # gibt "Pong!" zurück
    b = datetime.now()
    print response
    a = str(a)[17:19] + str(b)[20:23]
    b = str(b)[17:19] + str(b)[20:23]
    print str(int(b) - int(a)) + " ms\n"


def closessh():
    global sshverbindung
    global sshverbindung2
    global sshverbindung3
    sshverbindung.close()
    sshverbindung2.close()
    sshverbindung3.close()
    print("Verbindungen beendet.")


# startet Verbindung auf neuem Thread
incon = Thread(target=initconnection)
incon.start()
