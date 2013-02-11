#!/usr/bin/env python

import time
from robot import hexapod,setAngle,getAngle

hexy = hexapod()

hexy.RB.setHipDeg(20)
hexy.LB.setHipDeg(-20)
hexy.LM.setHipDeg(30)
hexy.RM.setHipDeg(-30)

hexy.neck.set(0)
time.sleep(0.5)

hexy.neck.set(30)
time.sleep(0.5)

hexy.LB.replantFoot(1,0.1,50)
hexy.RB.replantFoot(1,0.1,50)

hexy.RF.knee(-80)
hexy.RF.ankle(-80)
hexy.LF.knee(-80)
hexy.LF.ankle(-80)

time.sleep(0.2)

hexy.RF.hip(90)
hexy.LF.hip(-90)
hexy.neck.set(0)

