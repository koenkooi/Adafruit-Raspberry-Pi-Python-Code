#!/usr/bin/env python

import time
from robot import hexapod,setAngle,getAngle

hexy = hexapod()

for i in range(2):
	for leg in hexy.legs:
		leg.replantFoot(1,0.20,70)
		time.sleep(0.1)
	time.sleep(0.1)

time.sleep(0.5)

hexy.RB.setHipDeg(-20)
hexy.LB.setHipDeg(20)
hexy.RF.setHipDeg(20)
hexy.LF.setHipDeg(-20)
hexy.LM.setHipDeg(-40)
hexy.RM.setHipDeg(40)

for i in range(1):
	hexy.neck.set(50)
	time.sleep(0.4)
	hexy.neck.set(-50)
	time.sleep(0.4)

hexy.RF.hip(90)
hexy.LF.hip(-90)
hexy.neck.set(0)

hexy.LM.setFootY(70,stepTime=0.2)
hexy.RM.setFootY(70,stepTime=0.2)
hexy.LB.setFootY(50,stepTime=0.2)
hexy.RB.setFootY(50,stepTime=0.2)

hexy.RF.knee(-60)
hexy.RF.ankle(-80)
hexy.LF.knee(-20)
hexy.LF.ankle(-80)

time.sleep(0.2)


hexy.LM.setFootY(40,stepTime=0.2)
hexy.RM.setFootY(40,stepTime=0.2)
hexy.LB.setFootY(20,stepTime=0.2)
hexy.RB.setFootY(20,stepTime=0.2)

time.sleep(0.2)

hexy.LM.setFootY(70,stepTime=0.2)
hexy.RM.setFootY(70,stepTime=0.2)
hexy.LB.setFootY(50,stepTime=0.2)
hexy.RB.setFootY(50,stepTime=0.2)


time.sleep(0.2)


hexy.LM.setFootY(40,stepTime=0.2)
hexy.RM.setFootY(40,stepTime=0.2)
hexy.LB.setFootY(20,stepTime=0.2)
hexy.RB.setFootY(20,stepTime=0.2)

time.sleep(0.2)

hexy.LM.setFootY(70,stepTime=0.2)
hexy.RM.setFootY(70,stepTime=0.2)
hexy.LB.setFootY(50,stepTime=0.2)
hexy.RB.setFootY(50,stepTime=0.2)

time.sleep(0.2)


hexy.LM.setFootY(40,stepTime=0.2)
hexy.RM.setFootY(40,stepTime=0.2)
hexy.LB.setFootY(20,stepTime=0.2)
hexy.RB.setFootY(20,stepTime=0.2)

time.sleep(0.2)

hexy.LM.setFootY(70,stepTime=0.2)
hexy.RM.setFootY(70,stepTime=0.2)
hexy.LB.setFootY(50,stepTime=0.2)
hexy.RB.setFootY(50,stepTime=0.2)
time.sleep(0.2)


hexy.LM.setFootY(40,stepTime=0.2)
hexy.RM.setFootY(40,stepTime=0.2)
hexy.LB.setFootY(20,stepTime=0.2)
hexy.RB.setFootY(20,stepTime=0.2)

time.sleep(0.2)

hexy.LM.setFootY(70,stepTime=0.2)
hexy.RM.setFootY(70,stepTime=0.2)
hexy.LB.setFootY(50,stepTime=0.2)
hexy.RB.setFootY(50,stepTime=0.2)
