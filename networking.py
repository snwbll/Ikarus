# -*- coding: utf-8 -*-

import paramiko
import sys
import time
import select
from threading import Thread
from datetime import datetime

getgpsdatarunning = True
pilotrunning = True
autopiloton = False
host = "192.168.1.120"  # dynamischer: raw_input("\ninet Adresse des Hosts: "), pi muss aber eine statische IP haben
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
            pilott = Thread(target=pilot)
            pilott.start()  # Pilot wird aktiviert, der mit dem Autopiloten kommuniziert
            gpscon = Thread(target=gpsconnection)
            gpscon.start()  # GPS - Verbindung wird aufgebaut, sobald eine normale Verbindung besteht
            break
        except paramiko.AuthenticationException:
            print("Authentifizierung fehlgeschalagen bei Verbindung mit " + host)
            sys.exit(1)
        except:
            print("Verbindung fehlgeschlagen, warten auf " + host)
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
        print ("Fehler in execute: " + str(e))


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
            print("Authentifizierung fehlgeschalagen bei GPS - Verbindung mit %d." % host)
            sys.exit(1)
        except:
            print("GPS - Verbindung fehlgeschlagen, warten auf %s" % host)
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
                    if getgpsdatarunning == False:
                        break
            break
    except Exception as e:
        print("Fehler in getgpsdata: " + str(e))
    print "Getgpsdata beendet."


def execute_nooutput(command):
    try:
        stdin, stdout, stderr = sshverbindung.exec_command(command)
    except Exception as e:
        print("Fehler in execute_nooutput: " + str(e))


def pilot():
    global sshverbindung3
    ssh3 = sshverbindung3.invoke_shell()
    stdin = ssh3.makefile('wb')
    stdout = ssh3.makefile('rb')
    print "pilot beginnt nun mit der shellverbindung"
    while True:
        print "printed"
        stdin.write("echo 123")
        print "written"
        
        time.sleep(2)

"""
    global pilotrunning
    try:
        stdin, stdout, stderr = sshverbindung3.exec_command("python autopilot.py")
        while pilotrunning == True:
            try:
                if autopiloton == True:
                    time.sleep(4)
                    print "Autopilot ein"
                else:
                    # autopiloton == False
                    stdin.write('1\n')
                    time.sleep(2)
            except Exception as e:
                time.sleep(3)  # Verbindung unterbrochen, einfach weiterversuchen
                print "Die Exception für Pilot bei Verbindung ist nicht vorhanden: " + str(e)  # if e == blablabla

        # pilotrunning == False, Pilot ist also ausgeschalten. Um den Autopiloten zu beenden wird der Input 2 gegeben.
        i = 0
        while True:
            try:
                for i in range(1, 3):
                    stdin.write('2\n')
                    time.sleep(1)
                print "Autopilot ausgeschalten"
                break
            except Exception as e:
                print "Pilot: Excception2 lautet: " + str(e)
                time.sleep(2)
                i += 1
                if i > 5:
                    print "Autopilot konnte nicht abgeschalten werden..."
                    break

    except Exception as e:
        print "Fehler in pilot: " + str(e)

    # Pilot ist fertig, der Autopilot wurde beendet
    print "Pilot beendet"
"""

def mtest():
    print "Motorentest: t = 3 Sekunden\nLinks\nRechts\nZurueck\nOben\nUnten\n"
    execute_nooutput("python mtest.py")


def ping():
    print "Ping!"
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
