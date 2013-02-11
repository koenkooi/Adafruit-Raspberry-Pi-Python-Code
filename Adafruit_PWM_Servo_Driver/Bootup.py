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

for i in range(1):
	hexy.neck.set(50)
	time.sleep(0.4)
	hexy.neck.set(-50)
	time.sleep(0.4)

time.sleep(0.2)

# 70 - 30, 30 - 100

for i in range(4):
	for leg in hexy.tripod1:
		leg.replantFoot(1,0.20,70)
		time.sleep(0.1)
	time.sleep(0.2)
	for leg in hexy.tripod2:
		leg.replantFoot(1,0.20,70)
		time.sleep(0.1)

time.sleep(0.5)




