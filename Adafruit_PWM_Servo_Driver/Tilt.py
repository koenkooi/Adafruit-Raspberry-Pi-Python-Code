#!/usr/bin/env python

import time
from robot import hexapod,setAngle,getAngle,getHeading

hexy = hexapod()

'''
# 12cm spacing in the forward axis
hexy.RB.setHipDeg(-20)
hexy.LB.setHipDeg(20)
hexy.RF.setHipDeg(20)
hexy.LF.setHipDeg(-20)
hexy.LM.setHipDeg(0)
hexy.RM.setHipDeg(0)

time.sleep(0.2)
hexy.neck.set(0)

tiltdiff = 70

hexy.RF.setFootXY(10, 105, stepTime=0.1)
hexy.RM.setFootXY(35, 105 - tiltdiff/2, stepTime=0.1)
hexy.RB.setFootXY(50, 105 - tiltdiff, stepTime=0.1)
hexy.LF.setFootXY(10, 105, stepTime=0.1)
hexy.LM.setFootXY(35, 105 - tiltdiff/2, stepTime=0.1)
hexy.LB.setFootXY(50, 105 - tiltdiff, stepTime=0.1)

time.sleep(0.5)

getHeading()
'''

print "5"
hexy.setPitch(5,0.1,105)
time.sleep(1)
getHeading()
time.sleep(2)

print "10"
hexy.setPitch(10,0.1,105)
time.sleep(1)
getHeading()
time.sleep(2)

print "20"
hexy.setPitch(20,0.1,105)
time.sleep(1)
getHeading()


