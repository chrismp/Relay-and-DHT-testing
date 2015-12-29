# External module imports
import RPi.GPIO as GPIO
import time



# Pin Definitons:
coolPin = 18
heatPin = 23
fanPin = 22
pinArray = [
    coolPin,
    heatPin,
    fanPin
]

# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
for pin in pinArray:
    GPIO.setup(pin, GPIO.OUT) # When Pi interacts with pin, it is to send data from Pi to whatever is attached to pin
    GPIO.output(pin,GPIO.HIGH) # Set pin to 'HIGH', which means 'off'

print "Here we go! Press CTRL+C to exit"
try:
    while 1:
        for pin in pinArray:
            GPIO.output(pin, GPIO.LOW) # 'LOW' means 'on' in this case
            time.sleep(2)
            GPIO.output(pin, GPIO.HIGH)
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup() # cleanup all GPIO
