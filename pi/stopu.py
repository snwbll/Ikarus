import RPi.GPIO as gpio

x = 38
gpio.setmode(gpio.BOARD)
gpio.setup(x, gpio.OUT)
gpio.output(x, gpio.LOW)
gpio.cleanup()
