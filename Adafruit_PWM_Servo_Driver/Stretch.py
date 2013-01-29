#!/usr/bin/env python

import time
from robot import hexapod,setAngle,getAngle

hexy = hexapod()


for leg in hexy.legs:
	leg.setHipDeg(0)
	leg.ankle(0)
	leg.knee(0)



