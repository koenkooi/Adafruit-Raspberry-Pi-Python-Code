import time
from robot import hexapod,setAngle

for hip in [12, 13, 14, 15]:
	setAngle(hip,0)

hexy = hexapod()


for leg in hexy.legs:
	leg.setFootXY(40,30)

time.sleep(3)

for leg in hexy.legs:
	leg.setFootXY(40,30, stepTime=2)

time.sleep(2)

for leg in hexy.legs:
	leg.setFootXY(40,40, stepTime=2)

time.sleep(2)

for leg in hexy.legs:
   leg.setFootXY(40,50, stepTime=2)

time.sleep(2)

for leg in hexy.legs:
	leg.setFootXY(40,60, stepTime=2)

time.sleep(2)

for leg in hexy.legs:
	leg.setFootXY(40,70, stepTime=2)

time.sleep(2)

for leg in hexy.legs:
	leg.setFootXY(40,80, stepTime=2)

time.sleep(2)

for leg in hexy.legs:
	leg.setFootXY(40,90, stepTime=2)

time.sleep(2)

