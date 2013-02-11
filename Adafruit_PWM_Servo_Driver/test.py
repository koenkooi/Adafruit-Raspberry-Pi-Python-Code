#!/usr/bin/env python

import time
from robot import hexapod,setAngle,getAngle

hexy = hexapod()

# 12cm spacing in the forward axis
hexy.RB.setHipDeg(-20)
hexy.LB.setHipDeg(20)
hexy.RF.setHipDeg(20)
hexy.LF.setHipDeg(-20)
hexy.LM.setHipDeg(0)
hexy.RM.setHipDeg(0)

time.sleep(0.2)
hexy.LF.setFootXY(70, 30, stepTime=0.5)
time.sleep(1)

hexy.LF.setFootXY(65, 30, stepTime=0.5)
time.sleep(1)

hexy.LF.setFootXY(60, 40, stepTime=0.5)
time.sleep(1)

hexy.LF.setFootXY(55, 50, stepTime=0.5)
time.sleep(1)

hexy.LF.setFootXY(50, 60, stepTime=0.5)
time.sleep(1)

hexy.LF.setFootXY(45, 70, stepTime=0.5)
time.sleep(1)

hexy.LF.setFootXY(40, 80, stepTime=0.5)
time.sleep(1)

hexy.LF.setFootXY(35, 90, stepTime=0.5)
time.sleep(1)

hexy.LF.setFootXY(30, 100, stepTime=0.5)
time.sleep(1)

