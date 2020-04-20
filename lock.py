# /etc/init.d/lock.py
### BEGIN INIT INFO
# Provides:          lock.py
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon at boot time
# Description:       Enable service provided by daemon.
### END INIT INFO
#! /usr/bin/env python
import sys
import RPi.GPIO as gpio
import time
import serial

gpio.setwarnings(False)
ser = serial.Serial(

    port='/dev/ttyUSB0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

gpio.setmode(gpio.BOARD)
gpio.setup(11, gpio.OUT)
gpio.setup(13, gpio.OUT)
gpio.setup(18, gpio.OUT)
gpio.setup(5, gpio.IN, pull_up_down=gpio.PUD_DOWN)
counter = 0

while 1:
    x=ser.readline()
    if x.decode('ascii')=="1E0078B272A6":
        print ("tag detected.")
        gpio.output(11, True)
        time.sleep(0.5)
        counter = 1
        gpio.output(11, False)
    if x.decode('ascii')=="5500E4A7FDEB":
        print ("card detected.")
        gpio.output(13, True)
        time.sleep(0.5)
        counter = 1
        gpio.output(13, False)
    elif gpio.input(5) == False and counter == 0:
        gpio.output(18, True)
        time.sleep(0.5)
        gpio.output(18, False)
    counter = 0

gpio.cleanup()

