#!/usr/bin/env python

import time
from robot import hexapod,setAngle,getAngle

hexy = hexapod()

for i in range(4):
	hexy.neck.set(50)
	time.sleep(0.4)
	hexy.neck.set(-50)
	time.sleep(0.4)

hexy.neck.set(0)
