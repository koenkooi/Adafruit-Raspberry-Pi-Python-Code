#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
from robot import hexapod,setAngle
import time

pwm = PWM(0x40, debug=False)
pwm2 = PWM(0x41, debug=False)


pwm.setPWMFreq(60)                        # Set frequency to 60 Hz
pwm2.setPWMFreq(60)

hexy = hexapod()

for i in range(19):
	setAngle(i,0)

