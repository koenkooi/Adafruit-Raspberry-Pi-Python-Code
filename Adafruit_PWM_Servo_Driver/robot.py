#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time
import math

# Controller at i2c address 0x40
pwm = PWM(0x40, debug=True)

# Store offsets, cheap analog servos aren't that precise
servoCenter = [410,430,395,360,390,370,370,380,380,360,390,400,480,370,380,370, 16, 17, 18]
servoMin = [170,185,150,135,155,140,140,140,140,135,150,160,220,135,145,140, 16, 17, 18]
servoMax = [650,660,650,620,640,620,640,630,640,610,635,635,670,630,645,645, 16, 17, 18]

pwm.setPWMFreq(60)												# Set frequency to 60 Hz

class hexapod():
	def __init__(self):
		self.RF = leg('rightFront',15,11,10)
		self.RM = leg('rightMid',14,9,8)
		self.RB = leg('rightBack',16,7,6)
		
		self.LF = leg('leftFront',12,1,0)
		self.LM = leg('leftMid',13,3,2)
		self.LB = leg('leftBack',17,5,4)
		
		self.legs = [self.RF,self.RM,self.RB,self.LF,self.LM,self.LB]
		
		self.neck = neck(18)
		
		self.tripod1 = [self.RF,self.RB,self.LM]
		self.tripod2 = [self.LF,self.LB,self.RM]

class neck():
	def __init__(self,servoNum):
		self.servoNum = servoNum

	def set(self,deg):
		setAngle(servoNum, deg)

class leg():

	def __init__(self,name,hipServoNum,kneeServoNum,ankleServoNum,simOrigin=(0,3,0)):
		self.name = name
		self.hipServoNum = hipServoNum
		self.kneeServoNum = kneeServoNum
		self.ankleServoNum = ankleServoNum

	def hip(self, deg):
		if deg == "sleep":
			pwm.setPWM(self.hipServoNum, 0, 0)
		else:
			setAngle(self.hipServoNum, deg)

	def knee(self, deg):
		if deg == "sleep":
			pwm.setPWM(self.kneeServoNum, 0, 0)
		else:
			setAngle(self.kneeServoNum, deg)

	def ankle(self, deg):
		if deg == "sleep":
			pwm.setPWM(self.ankleServoNum, 0, 0)
		else:
			setAngle(self.ankleServoNum, deg)

	def setHipDeg(self,endHipAngle,stepTime=1):
		#currentHipAngle = self.con.servos[self.hipServoNum].getPosDeg()
		#hipMaxDiff = endHipAngle-currentHipAngle
		
		setAngle(self.hipServoNum, endHipAngle)
		time.sleep(stepTime)
		
		'''
			steps = range(int(stepPerS))
			for i,t in enumerate(steps):
			# TODO: implement time-movements the servo commands sent for far fewer
			#       total servo commands
			hipAngle = (hipMaxDiff/len(steps))*(i+1)
			try:
			anglNorm=hipAngle*(180/(hipMaxDiff))
			except:
			anglNorm=hipAngle*(180/(1))
			hipAngle = currentHipAngle+hipAngle
			self.con.servos[self.hipServoNum].setPos(deg=hipAngle)
			
			#wait for next cycle
			time.sleep(stepTime/float(stepPerS))
			'''
	
	def setFootY(self,footY,stepTime=1):
		# TODO: max steptime dependent
		# TODO: implement time-movements the servo commands sent for far fewer
		#       total servo commands
		
		if (footY < 75) and (footY > -75):
			kneeAngle = math.degrees(math.asin(float(footY)/85.0))
			ankleAngle = 90.0-kneeAngle
			setAngle(self.kneeServoNum, kneeAngle)
			setAngle(self.ankleServoNum,-ankleAngle)
	
	def replantFoot(self,endHipAngle,stepTime=1, height=60):
		# Smoothly moves a foot from one position on the ground to another in time seconds
		# TODO: implement time-movements the servo commands sent for far fewer total servo
		#       commands
		
		#currentHipAngle = self.con.servos[self.hipServoNum].getPosDeg()
		#hipMaxDiff = endHipAngle-currentHipAngle
		
		# Raise boot to max
		self.setFootY(0,stepTime=0)
		# Rotate hip
		setAngle(self.hipServoNum, endHipAngle)
		# sleep a bit to adhere to steptime param
		time.sleep(stepTime/2)
		# Lower foot to height
		self.setFootY(height,stepTime=0)
		
		
		'''
		steps = range(int(stepPerS))
		for i,t in enumerate(steps):
			
			hipAngle = (hipMaxDiff/len(steps))*(i+1)
			#print "hip angle calc'd:",hipAngle
			
			#calculate the absolute distance between the foot's highest and lowest point
			footMax = 0
			footMin = floor
			footRange = abs(footMax-footMin)
			
			#normalize the range of the hip movement to 180 deg
			try:
			anglNorm=hipAngle*(180/(hipMaxDiff))
			except:
			anglNorm=hipAngle*(180/(1))
			#print "normalized angle:",anglNorm
			
			#base footfall on a sin pattern from footfall to footfall with 0 as the midpoint
			footY = footMin-math.sin(math.radians(anglNorm))*footRange
			#print "calculated footY",footY
			
			#set foot height
			self.setFootY(footY,stepTime=0)
			hipAngle = currentHipAngle+hipAngle
			self.con.servos[self.hipServoNum].setPos(deg=hipAngle)
			
			#wait for next cycle
			time.sleep(stepTime/float(stepPerS))
		'''


def setAngle(channel, angle):
	if angle < -90:
		angle = -90
	if angle > 90:
		angle = 90
	if angle == 0:
		pwmvalue = servoCenter[channel]
	if angle > 0:
		pwmvalue = servoCenter[channel] + (angle/90.0)*abs(servoMax[channel] - servoCenter[channel])
	if angle < 0:
		pwmvalue = servoCenter[channel] + (angle/90.0)*abs(servoCenter[channel] - servoMin[channel])
	pwm.setPWM(channel, 0, int(pwmvalue))
	#print "angle: %s, pwmvalue: %s" % (angle, pwmvalue)
