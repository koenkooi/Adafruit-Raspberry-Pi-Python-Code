import time
from robot import hexapod,setAngle

hexy = hexapod()

for servo in range(18):
	setAngle(servo,0)

for leg in hexy.legs:
	leg.setFootXY(30,90, stepTime=2)

time.sleep(2)
