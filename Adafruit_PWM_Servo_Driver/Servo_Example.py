#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time
import math

# Controller at i2c address 0x40
pwm = PWM(0x40, debug=True)

# Store offsets, cheap analog servos aren't that precise
servoCenter = [410,430,395,360,390,370,370,380,380,360,390,400,480,370,380,370]
servoMin = [170,185,150,135,155,140,140,140,140,135,150,160,220,135,145,140]
servoMax = [650,660,650,620,640,620,640,630,640,610,635,635,670,630,645,645]

# Feet ID, counter-clockwise
LF = 0
LM = 1
LB = 2
RB = 3
RM = 4
RF = 5

pwm.setPWMFreq(60)                        # Set frequency to 60 Hz

def setAngle(pwm, channel, angle):
  if angle < -90:
    angle = -90
  if angle > 90:
    angle = 90
  if angle == 0:
    pwmvalue = servoCenter[channel]
  if angle > 0:
    pwmvalue = servoCenter[channel] + (angle/90.0)*abs(servoMax[channel] - servoCenter[channel])
  if angle < 0:
    pwmvalue = servoCenter[channel] + (angle/90.0)*abs(servoCenter[channel] - servoMin[channel]) 
  pwm.setPWM(channel, 0, int(pwmvalue))
  #print "angle: %s, pwmvalue: %s" % (angle, pwmvalue)

def setFootY(pwm, footno, ypos):
  kneeAngle = math.degrees(math.asin(float(ypos)/85.0))
  ankleAngle = 90.0-kneeAngle
  setAngle(pwm,footno*2+1,kneeAngle)
  setAngle(pwm,footno*2,-ankleAngle)

for hip in [12, 13, 14, 15]:
  setAngle(pwm,hip,0)

for iter in range(1):
  for i in range(15):
    for leg in range(6):
      setFootY(pwm,leg,-10 + i*5)
    time.sleep(1/60.0)

  for i in range(15):
    for leg in range(6):
      setFootY(pwm,leg,65-i*5)
    time.sleep(1/60.0)

time.sleep(1)

setFootY(pwm,0,85)
setFootY(pwm,1,50)
setFootY(pwm,2,-10)
setFootY(pwm,3,-10)
setFootY(pwm,4,50)
setFootY(pwm,5,85)

time.sleep(0.5)

setFootY(pwm,0,-15)
setAngle(pwm,12,-60)
setAngle(pwm,0,-60)
time.sleep(0.2)
setAngle(pwm,0,60)
time.sleep(0.2)
setAngle(pwm,0,-60)
time.sleep(0.2)
setAngle(pwm,0,60)

time.sleep(5)

setAngle(pwm,12,0)

for leg in range(6):
  setFootY(pwm,leg,-10)

time.sleep(0.5)

for i in range(16):
  pwm.setPWM(i,0,0)
