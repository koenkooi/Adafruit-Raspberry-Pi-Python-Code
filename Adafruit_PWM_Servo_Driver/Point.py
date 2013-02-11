#!/usr/bin/env python

import time
from robot import hexapod,setAngle,getAngle

hexy = hexapod()

hexy.neck.set(0)
time.sleep(0.5)

hexy.neck.set(30)
time.sleep(0.5)

hexy.RF.knee(60)
hexy.RF.ankle(60)

time.sleep(0.2)

hexy.RF.hip(-45)
hexy.neck.set(0)

