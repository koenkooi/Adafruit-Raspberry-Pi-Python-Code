#!/usr/bin/env python

import time
from robot import hexapod,setAngle

hexy = hexapod()

# 12cm spacing in the forward axis
hexy.RB.setHipDeg(-20)
hexy.LB.setHipDeg(20)
hexy.RF.setHipDeg(20)
hexy.LF.setHipDeg(-20)

while True: 
	for leg in hexy.legs:
		leg.setFootXY(20, 80, stepTime=0.1)

	time.sleep(0.5)


