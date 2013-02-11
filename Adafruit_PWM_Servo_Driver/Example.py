import time
from robot import hexapod,setAngle

for hip in [12, 13, 14, 15]:
	setAngle(hip,0)

hexy = hexapod()


for leg in hexy.legs:
	leg.setFootXY(40,30)

time.sleep(0.5)

for leg in hexy.legs:
	leg.setFootXY(40,30, stepTime=0.5)

time.sleep(0.6)

for leg in hexy.legs:
	leg.setFootXY(40,40, stepTime=0.5)

time.sleep(0.6)

for leg in hexy.legs:
   leg.setFootXY(40,50, stepTime=0.5)

time.sleep(0.6)

for leg in hexy.legs:
	leg.setFootXY(40,60, stepTime=0.5)

time.sleep(0.6)

for leg in hexy.legs:
	leg.setFootXY(40,70, stepTime=0.5)

time.sleep(0.6)

for leg in hexy.legs:
	leg.setFootXY(40,80, stepTime=0.5)

time.sleep(0.6)

for leg in hexy.legs:
	leg.setFootXY(40,90, stepTime=0.5)

time.sleep(0.6)

