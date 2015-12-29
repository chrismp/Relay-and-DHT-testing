#!/usr/bin/python

import RPi.GPIO as GPIO
import Adafruit_DHT
import time

# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
sensor = Adafruit_DHT.DHT22
dht22Pin = 4

# Pin Definitons:
coolPin = 18
heatPin = 23
fanPin = 22
hvacPinArray = [
    coolPin,
    heatPin,
    fanPin
]

# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
for pin in hvacPinArray:
    GPIO.setup(pin, GPIO.OUT) # When Pi interacts with pin, it is to send data from Pi to whatever is attached to pin
    GPIO.output(pin,GPIO.HIGH) # Set pin to 'HIGH', which means 'off'

print 'Here we go! Press CTRL+C to exit'
try:
        while 1:
                # Try to grab a sensor reading.  Use the read_retry method which will retry up
                # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
                humidity, temperature = Adafruit_DHT.read_retry(sensor, dht22Pin)
                tempF = temperature * 9/5.0 + 32
                coolF = 75
                heatF = 70
                fan = 1
                tempFBuffer = 1 # Example of how this is used: If COOL is set to 75, it will not turn on if tempF is 75.01, but only when it reaches 76 (75 + 1)

                # Note that sometimes you won't get a reading and
                # the results will be null (because Linux can't
                # guarantee the timing of calls to read the sensor).  
                # If this happens try again!
                if humidity is not None and temperature is not None:
                        print 'Temp={0:0.1f}*C/{1:0.1f}*F  Humidity={2:0.1f}% -- {3}'.format(temperature, tempF, humidity, time.ctime())

                        # FAN
                        if fan==0:
                                GPIO.output(fanPin, GPIO.HIGH)
                                print 'FAN off'
                        else:
                                GPIO.output(fanPin, GPIO.LOW)
                                print 'FAN on'

                        # COOL
                        # Comment this section out to 'turn off' cool while testing DHT22 with relay
                        if tempF > (coolF + tempFBuffer):
                                GPIO.output(coolPin, GPIO.LOW)
                                print 'COOL on'
                        elif tempF < coolF:
                                GPIO.output(coolPin, GPIO.HIGH)
                                print 'COOL off'
                        
                        # HEAT
                        if tempF < (heatF - tempFBuffer):
                                GPIO.output(heatPin, GPIO.LOW)
                                print 'HEAT on'
                        elif tempF > heatF:
                                GPIO.output(heatPin, GPIO.HIGH)
                                print 'HEAT off'

                        time.sleep(2)
                else:
                        print 'Failed to get reading. Try again!'
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
        print 'Nice knowin ya!'
        GPIO.cleanup() # cleanup all GPIO
