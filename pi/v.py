import RPi.GPIO as gpio

x = 16
y = 18

gpio.setmode(gpio.BOARD)
gpio.setup(x, gpio.OUT)
gpio.setup(y, gpio.OUT)
gpio.output(x, gpio.HIGH)
gpio.output(y, gpio.HIGH)
