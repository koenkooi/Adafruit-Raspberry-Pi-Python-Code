#!/usr/bin/env python

import time
from robot import hexapod,setAngle

hexy = hexapod()

deg = 25
midFloor = 30
hipSwing = 25
steptime = 0.8
pause = steptime + 0.4

#tripod1 = RF,LM,RB
#tripod2 = LF,RM,LB

for timeStop in range(8):
	time.sleep(0.1)
	# replant tripod2 forward while tripod1 move behind
	#   relpant tripod 2 forward
	hexy.LF.replantFoot(deg-hipSwing,stepTime=steptime)
	hexy.RM.replantFoot(hipSwing,stepTime=steptime)
	hexy.LB.replantFoot(-deg-hipSwing,stepTime=steptime)

	#   tripod1 moves behind
	hexy.RF.setHipDeg(-deg-hipSwing,stepTime=steptime)
	hexy.LM.setHipDeg(hipSwing,stepTime=steptime)
	hexy.RB.setHipDeg(deg-hipSwing,stepTime=steptime)
	time.sleep(pause)

	# replant tripod1 forward while tripod2 move behind
	#   replant tripod1 forward
	hexy.RF.replantFoot(-deg+hipSwing,stepTime=steptime)
	hexy.LM.replantFoot(-hipSwing,stepTime=steptime)
	hexy.RB.replantFoot(deg+hipSwing,stepTime=steptime)

	#   tripod2 moves behind
	hexy.LF.setHipDeg(deg+hipSwing,stepTime=steptime)
	hexy.RM.setHipDeg(-hipSwing,stepTime=steptime)
	hexy.LB.setHipDeg(-deg+hipSwing,stepTime=steptime)
	time.sleep(pause)

time.sleep(1)
hexy.setPitch(10,0.1,95)