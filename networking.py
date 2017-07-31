# -*- coding: utf-8 -*-
# im readme: Eingehende Echorequests müssen in den Firewallregeln erlaubt sein
import os
import sys
import time
import select
import socket
import paramiko
from threading import Thread

getgpsdatarunning = True
host = "192.168.1.99"  # dynamischer: raw_input("\ninet Adresse des Hosts: "), Pi muss dann keine statische IP haben
username = "pi"
password = "Snowball"
nodata = "Keine Daten"
gpsdata = [nodata, nodata, nodata, nodata, nodata, nodata, nodata, nodata, nodata, nodata, nodata, nodata]
sshverbindung = None
sshverbindung2 = None
sshverbindung3 = None
gpsverbindung = None
firsttime = True


def initconnection():
    counter = 1
    global firsttime
    while True:
        if firsttime:
            print("Verbindung mit %s wird aufgebaut..." % host)
        else:
            print("Erneute Verbindung mit %s wird aufgebaut..." % host)
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
            if firsttime:
                execute("sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock")  # GPS wird aktiviert
                startautopilot()  # Autopilot wird gestartet
            gpscon = Thread(target=gpsconnection)
            gpscon.start()  # GPS - Verbindung wird aufgebaut, sobald eine normale Verbindung besteht
            break
        except paramiko.AuthenticationException:
            print("Authentifizierung fehlgeschlagen bei Verbindung mit " + host)
            sys.exit(1)
        except Exception as e:
            print("Verbindung fehlgeschlagen, warten auf " + host + " (Exception: " + str(e) + ")")
            counter += 1
            time.sleep(2)
        if counter > 10:
            if firsttime:
                print("Verbindung wiederholt fehlgeschlagen. Wird abgebrochen.")
                sys.exit(1)
            else:
                counter = -10
    firsttime = False


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
    print "Autopilot gestartet."


def ping():
    global host
    os.system("ping " + host)


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
