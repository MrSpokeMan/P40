import time
import pigpio
import RPi.GPIO as GPIO

pi = pigpio.pi()
if not pi.connected:
    exit()
    
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)    

# Initilize 4 leds
for i in [12, 13, 18, 19]:
    GPIO.setup(i, GPIO.OUT)


sensor = pi.spi_open(1, 1000000, 0)  # CE1, 1Mbps, main SPI
stop = time.time() + 600
while time.time() < stop:
    c, d = pi.spi_read(sensor, 2)
    if c == 2:
        sign = (d[0] & 0x80) >> 7
        value = (((d[0] & 0x7f) << 8) | d[1]) >> 5
        temp = value * 0.125
        if sign == 1:
            temp = temp * -1
        print("{:.6f}".format(temp))
    time.sleep(0.25)  # Don’t try to read more often than 4 times a second.

    for i in [12, 13, 18, 19]:
        GPIO.output(i, GPIO.LOW)
    
    if temp >= 24:
        GPIO.output(12, GPIO.HIGH)
    if temp > 26:
        GPIO.output(13, GPIO.HIGH)
    if temp > 27:
        GPIO.output(18, GPIO.HIGH)
    if temp > 29:
        GPIO.output(19, GPIO.HIGH)

pi.spi_close(sensor)
pi.stop()
