#!/usr/bin/env python

import time
from robot import hexapod,setAngle

hexy = hexapod()

# Move: Shutdown

deg = -15
r_angle = 90

#neck in sleep position; turned left
hexy.neck.set(r_angle)

#bring hexy down low; don't want to belly (smack) flop
for leg in hexy.legs:
    leg.setFootY(deg)

time.sleep(0.5)

#point feet up
for leg in hexy.legs:
    leg.ankle(r_angle)

time.sleep(0.5)

#point knees up
for leg in hexy.legs:
    leg.knee(-r_angle)

time.sleep(0.5)

#zero hips
for leg in hexy.legs:
    leg.hip(0)

#kill all servos
#hexy.con.killAll()





