import RPi.GPIO as gpio

x = 18

gpio.setmode(gpio.BOARD)
gpio.setup(x, gpio.OUT)
gpio.output(x, gpio.HIGH)
