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

# 70 - 30, 30 - 100

for i in range(4,11):
	for leg in hexy.tripod1:
		leg.setFootXY(100-10*i, i*10, stepTime=0.1)
	time.sleep(0.1)
	for leg in hexy.tripod2:
		leg.setFootXY(100-10*i, i*10, stepTime=0.1)

time.sleep(0.5)



