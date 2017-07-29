# -*- coding: utf-8 -*-

import Tkinter as tk
import time
from threading import Thread
import webbrowser
from datetime import datetime

import networking

##################################################################### Info

ikarusVersion = "0.9"

# log 0.1: Verbindung
# log 0.2: Verbindungsprobleme behoben
# log 0.3: UI
# log 0.4: Multithreading
# log 0.5: UI und Verbindung verbessert
# log 0.6: Leistungsverbesserungen
# log 0.7: UI und Verbindung verbessert
# log 0.8: Fehlerbehebungen
# log 0.9: Unterstützung für Autopilot integriert

##################################################################### Running Variables

autopingrunning = True
getthegpsdatarunning = True

##################################################################### Root


class GUI():
    def __init__(self):
        root = tk.Tk()
        root.title("Ikarus (Version " + ikarusVersion + ")")
        w, h = (root.winfo_screenwidth()), root.winfo_screenheight()
        root.geometry("%dx%d" % (w, h))
        root.configure(background="white")
        root.bind('<KeyPress>', self.key_input)
        root.bind('<KeyRelease>', self.key_release)

        ##### Verbindung

        self.verbindungslabel = tk.Label(root, text="Ikarus", bg="white", font=('Arial, 18'))
        self.vst = tk.Label(root, text="Status: ", bg="white")
        self.vstanzeige = tk.Label(root, text="Noch keine Verbindung", bg="white", width=30)

        self.verbindungslabel.pack()
        self.vst.pack()
        self.vstanzeige.pack()

        self.verbindungslabel.place(x=30, y=10)
        self.vst.place(x=30, y=50)
        self.vstanzeige.place(x=200, y=50)

        # Autoping auf neuem Thread
        vsthread = Thread(target=self.autoping)
        vsthread.start()

        ##### Daten

        self.blabel = tk.Label(root, text="Breitengrad:", bg="white")
        self.llabel = tk.Label(root, text="Längengrad:", bg="white")
        self.hlabel = tk.Label(root, text="Höhe:", bg="white")
        self.glabel = tk.Label(root, text="Geschwindigkeit:", bg="white")
        self.slabel = tk.Label(root, text="Steigung:", bg="white")
        self.alabel = tk.Label(root, text="Ausrichtung:", bg="white")  # ?
        self.zlabel = tk.Label(root, text="Strecke:", bg="white")
        self.tlabel = tk.Label(root, text="Flugzeit:", bg="white")
        self.elabel = tk.Label(root, text="Entfernung:", bg="white")

        self.blabel.pack()
        self.llabel.pack()
        self.hlabel.pack()
        self.glabel.pack()
        self.slabel.pack()
        self.alabel.pack()
        self.zlabel.pack()
        self.tlabel.pack()
        self.elabel.pack()

        self.blabel.place(x=30, y=80)
        self.llabel.place(x=30, y=110)
        self.hlabel.place(x=30, y=140)
        self.glabel.place(x=30, y=170)
        self.slabel.place(x=30, y=200)
        self.alabel.place(x=30, y=230)
        self.zlabel.place(x=30, y=260)
        self.tlabel.place(x=30, y=290)
        self.elabel.place(x=30, y=320)

        ##### Daten 2

        self.bd = tk.Label(root, text='', bg="white")  # Breitengrad
        self.ld = tk.Label(root, text='', bg="white")  # Längengrad
        self.hd = tk.Label(root, text='', bg="white")  # Höhe
        self.gd = tk.Label(root, text='', bg="white")  # Geschwindigkeit
        self.sd = tk.Label(root, text='', bg="White")  # Steigung
        self.td = tk.Label(root, text='', bg="White")  # Zeit gerade

        self.bd.pack()
        self.ld.pack()
        self.hd.pack()
        self.gd.pack()
        self.sd.pack()
        self.td.pack()

        self.bd.place(x=180, y=90)
        self.ld.place(x=180, y=120)
        self.hd.place(x=180, y=150)
        self.gd.place(x=180, y=180)
        self.sd.place(x=180, y=210)
        self.td.place(x=180, y=300)
        g = Thread(target=self.getthegpsdata)
        g.start()

        ##### Daten 3 (Offset)

        self.bdoff = tk.Label(root, text='', bg="white")  # Breitengrad
        self.ldoff = tk.Label(root, text='', bg="white")  # Längengrad
        self.hdoff = tk.Label(root, text='', bg="white")  # Höhe
        self.gdoff = tk.Label(root, text='', bg="white")  # Geschwindigkeit
        self.sdoff = tk.Label(root, text='', bg="white")  # Steigung
        self.starttim = tk.Label(root, text="Start: " + str(datetime.now())[11:16] + " Uhr", bg="white")  # Startzeit

        self.bdoff.pack()
        self.ldoff.pack()
        self.hdoff.pack()
        self.gdoff.pack()
        self.starttim.pack()

        self.bdoff.place(x=300, y=90)
        self.ldoff.place(x=300, y=120)
        self.hdoff.place(x=300, y=150)
        self.gdoff.place(x=300, y=180)
        self.starttim.place(x=300, y=300)

        ##### Steuerung

        self.a = False
        self.s = False
        self.d = False
        self.w = False
        self.o = False
        self.u = False

        self.buttonpresseda = tk.Label(root, text='a', bg="white", font='Arial, 25', width=2)
        self.buttonpresseds = tk.Label(root, text='s', bg="white", font='Arial, 25', width=2)
        self.buttonpressedd = tk.Label(root, text='d', bg="white", font='Arial, 25', width=2)
        self.buttonpressedw = tk.Label(root, text='w', bg="white", font='Arial, 25', width=2)
        self.buttonpressedp = tk.Label(root, text='p', bg="white", font='Arial, 25', width=2)
        self.buttonpressedl = tk.Label(root, text='l', bg="white", font='Arial, 25', width=2)

        self.buttonpresseda.pack()
        self.buttonpresseds.pack()
        self.buttonpressedd.pack()
        self.buttonpressedw.pack()
        self.buttonpressedp.pack()
        self.buttonpressedl.pack()

        self.buttonpresseda.place(x=30, y=560)
        self.buttonpresseds.place(x=80, y=560)
        self.buttonpressedd.place(x=130, y=560)
        self.buttonpressedw.place(x=80, y=510)
        self.buttonpressedp.place(x=200, y=510)
        self.buttonpressedl.place(x=190, y=560)

        self.linkbutton = tk.Button(root, text="Position in Google Maps ansehen", command=self.openlink)
        self.linkbutton.pack()
        self.linkbutton.place(x=30, y=380)

        self.mtestbutton = tk.Button(root, text="Motorentest", command=networking.mtest)
        self.mtestbutton.pack()
        self.mtestbutton.place(x=30, y=410)

        self.pingbutton = tk.Button(root, text="Ping", command=networking.ping)
        self.pingbutton.pack()
        self.pingbutton.place(x=30, y=440)

        self.pilotbutton = tk.Button(root, text="Autopilot einschalten", command=self.switchpilot)
        self.pilotbutton.pack()
        self.pilotbutton.place(x=30, y=470)

        ###### mainloop

        root.mainloop()

    def switchpilot(self):
        if networking.autopiloton == False:
            networking.autopiloton = True
            self.pilotbutton['text'] = "Autopilot ausschalten"
        else:
            networking.autopiloton = False
            self.pilotbutton['text'] = "Autopilot einschalten"

    def autoping(self):
        time.sleep(3)
        global autopingrunning
        autopingrunning = True
        try:
            while autopingrunning == True:
                a = str(datetime.now())
                response = networking.execute("./ping")  # gibt "Pong!" zurück
                if str(response) == "Pong!":
                    b = datetime.now()
                    a = str(a)[17:19] + str(b)[20:23]
                    b = str(b)[17:19] + str(b)[20:23]
                    pingstat = str(int(b) - int(a))
                    connectedstat = "Verbunden"
                    connectedcolor = "green"
                    time.sleep(2)
                else:
                    print "Keine Verbindung... (Output bei ./ping: " + response + ")"
                    connectedstat = "Nicht Verbunden"
                    connectedcolor = "red"
                    pingstat = str(0)
                    time.sleep(2)
                    networking.initconnection()

                self.vstanzeige['text'] = connectedstat + " (" + pingstat + " ms)"
                self.vstanzeige['bg'] = connectedcolor
            print "Autoping beendet."

        except Exception as e:
            e = str(e)
            if e[0:20] == 'invalid command name':
                pass  # rootwindow ist beendet
            else:
                print "Fehler in autoping: " + str(e)
                time.sleep(3)

    def getthegpsdata(self):
        starttime = str(datetime.now())[11:16]
        i = 30
        global getthegpsdatarunning
        getthegpsdatarunning = True
        while getthegpsdatarunning == True:
            try:
                # Daten
                self.bd['text'] = str(networking.gpsdata[0]) + " N"  # Breitengrad
                self.ld['text'] = str(networking.gpsdata[1]) + " E"  # Längengrad
                self.hd['text'] = str(networking.gpsdata[3]) + " m"  # Höhe
                self.gd['text'] = str(networking.gpsdata[4]) + " m/s"  # Geschwindigkeit
                self.sd['text'] = str(networking.gpsdata[5]) + " m/s"  # Steigung

                if i == 30:  # Jede Minute und das erste Mal
                    timenow = str(datetime.now())[11:16]
                    if int(timenow[3:5]) > int(starttime[3:5]):
                        tdif = (int(timenow[3:5]) - int(starttime[3:5]))
                    elif int(timenow[3:5]) == int(starttime[3:5]):
                        tdif = 0
                    else:
                        tdif = (int(timenow[3:5]) - int(starttime[3:5]))
                    if int(timenow[0:2]) > int(starttime[0:2]):
                        tdif += 60  # 1 Stunde ist vergangen
                    self.td['text'] = str(tdif) + " min"
                    if tdif > 20:  # maximale Flugzeit (tmax)
                        self.td['bg'] = "orangered"  # bei t > 20 min wird gewarnt
                    i = 0

                # Abweichungen
                self.bdoff['text'] = "+/- " + str(networking.gpsdata[9]) + " m"
                self.ldoff['text'] = "+/- " + str(networking.gpsdata[8]) + " m"
                self.hdoff['text'] = "+/- " + str(networking.gpsdata[10]) + " m"
                self.gdoff['text'] = "+/- " + str(networking.gpsdata[7]) + " m/s"
                i += 1
                time.sleep(2)

            except Exception as e:
                e = str(e)
                if e[0:20] == 'invalid command name':
                    break  # rootwindow ist beendet, Thread beenden
                elif e == "list index out of range":
                    i += 2
                else:
                    print "Fehler in getgpsdata: " + str(e)
                    time.sleep(1.5)
        print "Getthegpsdata beendet."

    def pressed(self, button):
        if button == "a":
            self.buttonpresseda['bg'] = "red"
        elif button == "d":
            self.buttonpressedd['bg'] = "red"
        elif button == "w":
            self.buttonpressedw['bg'] = "red"
        elif button == "s":
            self.buttonpresseds['bg'] = "red"
        elif button == "p":
            self.buttonpressedp['bg'] = "red"
        elif button == "l":
            self.buttonpressedl['bg'] = "red"
        else:
            pass

    def released(self, button):
        if button == "a":
            self.buttonpresseda['bg'] = "white"
        elif button == "d":
            self.buttonpressedd['bg'] = "white"
        elif button == "w":
            self.buttonpressedw['bg'] = "white"
        elif button == "s":
            self.buttonpresseds['bg'] = "white"
        elif button == "p":
            self.buttonpressedp['bg'] = "white"
        elif button == "l":
            self.buttonpressedl['bg'] = "white"
        else:
            pass

    def key_input(self, event):
        # alle Skripte zum Steuern der Motoren werden über execute_nooutput ausgeführt, damit das Programm
        # nicht auf das Beenden des Prozessed warten muss, und pressed() / released() gleich ausführen kann.
        key_press = event.char.lower()
        if key_press == "a":
            if self.a == False:
                networking.execute_nooutput("python l.py")
                self.pressed("a")
                self.a = True
        elif key_press == "d":
            if self.d == False:
                networking.execute_nooutput("python r.py")
                self.pressed("d")
                self.d = True
        elif key_press == "w":
            if self.w == False:
                networking.execute_nooutput("python v.py")
                self.pressed("w")
                self.w = True
        elif key_press == "s":
            if self.s == False:
                networking.execute_nooutput("python z.py")
                self.pressed("s")
                self.s = True
        elif key_press == "o" or key_press.lower() == "p":
            if self.o == False:
                networking.execute_nooutput("python o.py")
                self.pressed("p")
                self.o = True
        elif key_press == "k" or key_press.lower() == "l":
            if self.u == False:
                networking.execute_nooutput("python u.py")
                self.pressed("l")
                self.u = True
        else:
            pass

    def key_release(self, event):
        key_release = event.char.lower()
        if key_release == "a":
            networking.execute_nooutput("python stopl.py")
            self.released("a")
            self.a = False
        elif key_release == "d":
            networking.execute_nooutput("python stopr.py")
            self.released("d")
            self.d = False
        elif key_release == "w":
            networking.execute_nooutput("python stopv.py")
            self.released("w")
            self.w = False
        elif key_release == "s":
            networking.execute_nooutput("python stopz.py")
            self.released("s")
            self.s = False
        elif key_release == "o" or key_release.lower() == "p":
            networking.execute_nooutput("python stopo.py")
            self.released("p")
            self.o = False
        elif key_release == "k" or key_release.lower() == "l":
            networking.execute_nooutput("python stopu.py")
            self.released("l")
            self.u = False
        else:
            pass

    def openlink(self):
        # öffnet Koordinaten in Google Maps
        webbrowser.open("https://www.google.it/maps/search/" + str(networking.gpsdata[0]) + "+N++" +
                        str(networking.gpsdata[1]) + "+E?sa=X&ved=0ahUKEwiArPqFuZLUAhWBPRQKHUAtB7MQ8gEIJTAA")


myGUI = GUI()

# beendet alle Threads und schließt alle Verbindungen
networking.pilotrunning = False
networking.getgpsdatarunning = False
autopingrunning = False
getthegpsdatarunning = False
time.sleep(5)
networking.closessh()
