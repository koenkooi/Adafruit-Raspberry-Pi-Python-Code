#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time
import math

# Controller at i2c address 0x40
pwm = PWM(0x40, debug=True)

# Store offsets, cheap analog servos aren't that precise
servoCenter = [410,430,395,360,390,370,370,380,380,360,390,400,480,370,380,370]
servoMin = [170,185,150,135,155,140,140,140,140,135,160,160,220,135,145,140]
servoMax = [650,660,650,620,640,620,640,630,640,610,635,635,670,630,645,645]

# Feet ID, counter-clockwise
LF = 0
LM = 1
LB = 2
RB = 3
RM = 4
RF = 5

pwm.setPWMFreq(60)                        # Set frequency to 60 Hz

for i in range(16):
  pwm.setPWM(i,0,0)
