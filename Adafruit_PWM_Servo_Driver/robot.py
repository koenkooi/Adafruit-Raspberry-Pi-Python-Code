#!/usr/bin/env python

from Adafruit_PWM_Servo_Driver import PWM
import time
import math
import threading
from datetime import datetime, timedelta
import os.path

# Controller at i2c address 0x40
pwm = PWM(0x40, debug=False)
pwm2 = PWM(0x41, debug=False)

# Store offsets, cheap analog servos aren't that precise
servoCenter = [320,350,365,380,320,360,385,350,340,350,270,355,390,390,380,380, 380, 390, 400]
servoMin = [170,185,150,135,155,140,140,140,140,135,150,160,220,135,145,140, 150, 150, 150]
servoMax = [650,660,650,620,640,620,640,630,640,610,635,635,670,630,645,645, 650, 650, 650]

# Interpolation steps
stepPerS = 16

# Max height
floor = 60

global upsidedown
upsidedown = 2

# leg dimensions
legLength = 48.0
footLength = 51.0

# Set frequency to 60 Hz, max for servos
pwm.setPWMFreq(60)

lock = threading.Lock()

class runMovement(threading.Thread):
	def __init__(self,function,*args):
		threading.Thread.__init__(self)
		self.function=function
		self.args = args
		self.lock = lock
		self.start()

	def run(self):
		self.function(*self.args)

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

		self.orientation = 0

class neck():
	def __init__(self,servoNum):
		self.servoNum = servoNum

	def set(self,deg):
		setAngle(self.servoNum, deg)

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
		runMovement(self.setHipDeg_function, endHipAngle,stepTime)
		
	def setHipDeg_function(self,endHipAngle,stepTime):
		getOrientation()
		#print "endHipAngle: %s,servoNum: %s" % (endHipAngle, self.hipServoNum)
		
		'''
		# Non-interpolated version
		setAngle(self.hipServoNum, endHipAngle)
		time.sleep(stepTime)
		'''
		
		lock.acquire()
		currentHipAngle = getAngle(self.hipServoNum)
		lock.release()
		
		hipMaxDiff = float(endHipAngle-currentHipAngle)
		
		steps = range(int(stepPerS*stepTime))
		stepDelay = 1/float(stepPerS)
		for i,t in enumerate(steps):
			startiter = datetime.now()
			# TODO: implement time-movements the servo commands sent for far fewer
			#       total servo commands
			hipAngle = (hipMaxDiff/len(steps))*(i+1)
			try:
				anglNorm=hipAngle*(180/(hipMaxDiff))
			except:
				anglNorm=hipAngle*(180/(1.0))
			hipAngle = currentHipAngle+hipAngle
			setAngle(self.hipServoNum, hipAngle)
			
			#wait for next cycle
			enditer = datetime.now()
			elapsed = enditer - startiter
			elapsedTime = elapsed.microseconds / 1000000.0
			if elapsedTime < stepDelay*0.9:
				stepSleep = stepDelay -elapsedTime
				time.sleep(stepSleep)
			enditer2 = datetime.now()
			elapsed2 = enditer2 - startiter
			#print "Iteration took %s/%s ms sleep, expected %s ms" % (elapsed2.microseconds/1000.0, elapsedTime * 1000, stepDelay * 1000)

	def setFootY(self,footY,stepTime=0.2):
		runMovement(self.setFootY_function, footY,stepTime)
		
	def setFootY_function(self,footY,stepTime):
		# TODO: max steptime dependent
		# TODO: implement time-movements the servo commands sent for far fewer
		#       total servo commands
	
		# Check orientation
		getOrientation()

		#print "footY: %s" % footY
		if (footY < 75) and (footY > -75):

			lock.acquire()
			currentKneeAngle = getAngle(self.kneeServoNum)
			currentAnkleAngle = getAngle(self.ankleServoNum)
			lock.release()
			
			kneeAngle = math.degrees(math.asin(float(footY)/75.0))
			ankleAngle = 90.0-kneeAngle


			if stepTime > (2/float(stepPerS)):
				kneeDiff = float(kneeAngle - currentKneeAngle)
				ankleDiff = float(ankleAngle - currentAnkleAngle)
				#print "setFootY: cKa: %s \tcAa: %s \tkA: %s \taA: %s \tkD: %s" % (currentKneeAngle, currentAnkleAngle, kneeAngle, ankleAngle, kneeDiff)

				steps = range(int(stepPerS*stepTime))
				stepDelay = 1/float(stepPerS)
				loopstart = datetime.now()
				for i,t in enumerate(steps):
					startiter = datetime.now()
					newKneeAngle = (kneeDiff/len(steps))*(i+1)
					newAnkleAngle = (ankleDiff/len(steps))*(i+1)
					setAngle(self.kneeServoNum, currentKneeAngle + newKneeAngle)
					setAngle(self.ankleServoNum,-(currentAnkleAngle + newAnkleAngle))

					enditer = datetime.now()
					elapsed = enditer - startiter
					elapsedTime = elapsed.microseconds / 1000000.0
					if elapsedTime < stepDelay*0.9:
						stepSleep = stepDelay -elapsedTime
						time.sleep(stepSleep)
					enditer2 = datetime.now()
					elapsed2 = enditer2 - startiter
					#print "Iteration took %s/%s ms sleep, expected %s ms" % (elapsed2.microseconds/1000.0, elapsedTime * 1000, stepDelay * 1000)
				loopend = datetime.now()
				loopelapsed = loopend - loopstart
				#print str(loopelapsed)
			else:
				setAngle(self.kneeServoNum, kneeAngle)
				setAngle(self.ankleServoNum,-ankleAngle)

	def setFootXY(self,footX, footY, stepTime=0.2):
		runMovement(self.setFootXY_function, footX, footY, stepTime)

	def setFootXY_function(self,footX, footY,stepTime):
		getOrientation()
		if math.sqrt(footX*footX + footY*footY) < (footLength + legLength):

			try:
				d = math.sqrt(footX*footX+footY*footY)
				k = (d*d-footLength*footLength+legLength*legLength)/(2*d)
				m = math.sqrt(legLength*legLength-k*k)
			except ZeroDivisionError:
				print "Divide by Zero error. No valid joint solution."
				return
			except ValueError:
				print "Math function error. Probably square root of negative number. No valid joint solution."
				return
			theta = math.degrees(math.atan2(float(footY),float(footX))-math.atan2(m,k))
			phi   = math.degrees(math.atan2(m,k)+math.atan2(m,(d-k)))

			#x=acos(theta)+bcos(theta + phi)
			#y=asin(theta)+bsin(theta + phi)
			
			lock.acquire()
			currentKneeAngle = getAngle(self.kneeServoNum)
			currentAnkleAngle = getAngle(self.ankleServoNum)
			lock.release()
			
			kneeAngle = theta
			ankleAngle = phi
			
			kneeDiff = float(kneeAngle - currentKneeAngle)
			ankleDiff = float(ankleAngle - currentAnkleAngle)
			
			steps = range(int(stepPerS*stepTime))
			stepDelay = 1/float(stepPerS)

			start = datetime.now()
			for i,t in enumerate(steps):
				startiter = datetime.now()
				newKneeAngle = (kneeDiff/len(steps))*(i+1)
				newAnkleAngle = (ankleDiff/len(steps))*(i+1)
				setAngle(self.kneeServoNum, currentKneeAngle + newKneeAngle)
				setAngle(self.ankleServoNum,-(currentAnkleAngle + newAnkleAngle))
				
				enditer = datetime.now()
				elapsed = enditer - startiter
				elapsedTime = elapsed.microseconds / 1000000.0
				if elapsedTime < stepDelay:
					stepSleep = stepDelay -elapsedTime
					time.sleep(stepSleep)
				enditer2 = datetime.now()
				elapsed2 = enditer2 - startiter
				#print "Iteration took %s/%s ms sleep, expected %s ms" % (elapsed2.microseconds/1000.0, elapsedTime * 1000, stepDelay * 1000)
			loopend = datetime.now()
			loopelapsed = loopend - start
			#print str(loopelapsed)
		else:
			print "Position (%s,%s) out of reach, ignoring" % (footX, footY)

	def setRoll(self,rollDeg,stepTime=1, height=60):
		runMovement(self.setRoll_function, rollDeg,stepTime, height)

	def setRoll_function(self,rollDeg,stepTime, height):
		print "setRoll: Implement me"
		hexy.RB.setHipDeg(20)
		hexy.LB.setHipDeg(-20)
		hexy.RF.setHipDeg(-20)
		hexy.LF.setHipDeg(20)
		for leg in hexy.legs:
			leg.setFootXY(30, height, stepTime=0.1)

	def setPitch(self,pitchDeg,stepTime=1, height=60):
		runMovement(self.setPitch_function, pitchDeg,stepTime, height)

	def setPitch_function(self,pitchDeg,stepTime, height):
		print "setPitch: Implement me"
		# 12cm leg spacing
		hexy.RB.setHipDeg(20)
		hexy.LB.setHipDeg(-20)
		hexy.RF.setHipDeg(-20)
		hexy.LF.setHipDeg(20)
		for leg in hexy.legs:
			leg.setFootXY(30, height, stepTime=0.1)

	def replantFoot(self,endHipAngle,stepTime=1, height=60):
		runMovement(self.replantFoot_function, endHipAngle,stepTime, height)
		
	def replantFoot_function(self,endHipAngle,stepTime, height):
		# Smoothly moves a foot from one position on the ground to another in time seconds
		# TODO: implement time-movements the servo commands sent for far fewer total servo
		#       commands
		
		'''
		# Non-interpolated version
		# Raise boot to max
		self.setFootY(0,stepTime=0)
		# Rotate hip
		setAngle(self.hipServoNum, endHipAngle)
		# sleep a bit to adhere to steptime param
		time.sleep(stepTime/2)
		# Lower foot to height
		self.setFootY(height,stepTime=0)
		'''

		lock.acquire()
		currentHipAngle = getAngle(self.hipServoNum)
		lock.release()
		
		hipMaxDiff = float(endHipAngle - currentHipAngle)
			
		steps = range(int(stepPerS*stepTime))
		stepDelay = 1/float(stepPerS)
		start = datetime.now()
		for i,t in enumerate(steps):
			startiter = datetime.now()
	
			#print "replantFoot %s:\ti: %s cur: %s end: %s max: %s" % (self.hipServoNum, i, currentHipAngle, endHipAngle, hipMaxDiff)
			hipAngle = (hipMaxDiff/len(steps))*(i+1)
			#print "hip angle calc'd:",hipAngle
			
			#calculate the absolute distance between the foot's highest and lowest point
			footMax = 0
			footMin = height
			footRange = abs(footMax-footMin)
			
			#normalize the range of the hip movement to 180 deg
			try:
				anglNorm=hipAngle*(180/(hipMaxDiff))
			except:
				anglNorm=hipAngle*(180/(1.0))
			#print "normalized angle:",anglNorm
			
			#base footfall on a sin pattern from footfall to footfall with 0 as the midpoint
			footY = footMin-math.sin(math.radians(anglNorm))*footRange
			#print "calculated footY",footY
			
			#set foot height
			self.setFootY(footY,stepTime=0)
			hipAngle = currentHipAngle+hipAngle
			setAngle(self.hipServoNum, hipAngle)
			
			enditer = datetime.now()
			elapsed = enditer - startiter
			elapsedTime = elapsed.microseconds / 1000000.0
			if elapsedTime < stepDelay*0.9:
				stepSleep = stepDelay -elapsedTime
				time.sleep(stepSleep)
			enditer2 = datetime.now()
			elapsed2 = enditer2 - startiter
		#print "Iteration took %s/%s ms sleep, expected %s ms" % (elapsed2.microseconds/1000.0, elapsedTime * 1000, stepDelay * 1000)
		loopend = datetime.now()
		loopelapsed = loopend - start
		#print str(loopelapsed)


def setAngle(channel, angle):
	if upsidedown > 0:
		angle = -angle
	if angle < -92:
		#print "Angle smaller than -92: %s for channel %s" % (angle, channel)
		angle = -92
	if angle > 92:
		#print "Angle larger than 92: %s for channel %s" % (angle, channel)
		angle = 92
	if angle == 0:
		pwmvalue = servoCenter[channel]
	if angle > 0:
		pwmvalue = servoCenter[channel] + (angle/90.0)*abs(servoMax[channel] - servoCenter[channel])
	if angle < 0:
		pwmvalue = servoCenter[channel] + (angle/90.0)*abs(servoCenter[channel] - servoMin[channel])
	#print "\t\t\t%s: angle: %s, pwmvalue: %s" % (channel, angle, pwmvalue)

	lock.acquire()
	if channel < 16:
		pwm.setPWM(channel, 0, int(pwmvalue))
	else:
		pwm2.setPWM(channel - 16, 0, int(pwmvalue))
	lock.release()

def getAngle(channel):
	if channel < 16:
		pwmvalue = pwm.getPWM(channel)
	else:
		pwmvalue = pwm2.getPWM(channel - 16)
			
	if pwmvalue > servoCenter[channel]:
		angle = 90.0*(pwmvalue - servoCenter[channel])/float(servoMax[channel] - servoCenter[channel])
	else:
		angle = 90.0*(servoCenter[channel] - pwmvalue)/float(servoCenter[channel] - servoMin[channel])
	#print "%s: angle %s" % (channel, angle)
	if (angle < -100):
		angle = -100
	if (angle > 100):
		angle = 100
	if upsidedown < 1:
		return angle
	else:
		return -angle

# Board is rotated 90 degrees, so X and Y are swapped

def getOrientation():
	runMovement(getOrientation_function)

def getOrientation_function():
	global upsidedown
	iopath='/sys/devices/ocp.2/4819c000.i2c/i2c-1/1-0019/iio:device0'
	if os.path.exists(iopath):
		f = open(iopath + '/in_accel_z_raw','r')
		accelZ=float(f.read()) 
		f.close
		if accelZ > 500:
			#print "Upside down!"
			upsidedown = 1
			return 0
		else:
			upsidedown = 0
			return 1
	else:
		upsidedown = 0
		return 1

