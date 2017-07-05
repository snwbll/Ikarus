import os
import time

l = ["links", "rechts", "zurueck", "oben", "unten"]
lpy = ["l.py", "r.py", "z.py", "o.py", "u.py"]
lpy2 = ["stopl.py", "stopr.py", "stopz.py", "stopo.py", "stopu.py"]

t = 3.5

print("Beginne Motortest mit t = " + str(t) + " Sekunden.\n")
time.sleep(3)

n = 0

for i in range(0,5):
    os.system("python " + lpy[i])
    print("Output: " + l[n] + "\n")
    time.sleep(t)
    os.system("python " + lpy2[i])
    n += 1

print("Beendet!")
