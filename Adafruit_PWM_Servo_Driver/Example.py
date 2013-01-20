import time
from robot import hexapod,setAngle

for hip in [12, 13, 14, 15]:
	setAngle(hip,0)

hexy = hexapod()

hexy.LF.setFootY(70)
hexy.LM.setFootY(70)
hexy.LB.setFootY(70)
hexy.RB.setFootY(70)
hexy.RM.setFootY(70)
hexy.RF.setFootY(70)


time.sleep(2)

setAngle(12,0)

hexy.LF.setFootY(10)
hexy.LM.setFootY(10)
hexy.LB.setFootY(10)
hexy.RB.setFootY(10)
hexy.RM.setFootY(10)
hexy.RF.setFootY(10)

time.sleep(1)

for leg in hexy.legs:
	leg.hip("sleep")
	leg.knee("sleep")
	leg.ankle("sleep")
