from gps import *
import time
import threading

gpsd = None

class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE)
    self.current_value = None
    self.running = True
 
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() 
 
gpsp = GpsPoller()
try:
    gpsp.start()
    while True:
        print [gpsd.fix.latitude, gpsd.fix.longitude, gpsd.fix.time, 
            gpsd.fix.altitude, gpsd.fix.speed, gpsd.fix.climb, gpsd.fix.track,
            gpsd.fix.eps, gpsd.fix.epx, gpsd.fix.epy,
            gpsd.fix.epv, gpsd.fix.ept, gpsd.fix.mode]
        time.sleep(2)

except (KeyboardInterrupt, SystemExit):
    gpsp.running = False
    gpsp.join()
