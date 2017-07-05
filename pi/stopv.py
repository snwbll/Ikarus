import RPi.GPIO as gpio

x = 16
y = 18

gpio.setmode(gpio.BOARD)
gpio.setup(x, gpio.OUT)
gpio.setup(y, gpio.OUT)
gpio.output(x, gpio.LOW)
gpio.output(y, gpio.LOW)
gpio.cleanup()
