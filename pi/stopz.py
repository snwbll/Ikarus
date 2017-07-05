import RPi.GPIO as gpio

x = 22
gpio.setmode(gpio.BOARD)
gpio.setup(x, gpio.OUT)
gpio.output(x, gpio.LOW)
gpio.cleanup()
