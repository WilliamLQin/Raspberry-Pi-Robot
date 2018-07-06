import time
from neopixel import *
import argparse

LED_COUNT = 10
LED_PIN = 18

LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

internal_clock = 0
call_queue = []
queue_position = 0
current_mode = "off"

moving = 0  # 0 for stop, 1 for forward, 2 for backward, 3 for turn left, 4 for turn right
strafing = 0  # 0 for stop, 1 for left, 2 for right

def clock():
	global internal_clock
	global call_queue
	global queue_position
	global strip

	internal_clock -= 1;
	while internal_clock <= 0 and queue_position < len(call_queue):
		next = call_queue[queue_position]
		if next[0] == "goto":
			queue_position = next[1]
			continue
		strip.setPixelColor(next[0], next[1])
		strip.show()
		internal_clock = next[2]
		queue_position += 1

def off():
	global strip

	for i in range(strip.numPixels()):
		strip.setPixelColor(i, Color(0,0,0))
		strip.show()	

def clear():
	global call_queue
	global queue_position

	call_queue[:] = []
	queue_position = 0

def stopMoving():
	global moving
	global strafing

	moving = 0
	if strafing == 1:
		stateStrafingLeft()
	elif strafing == 2:
		stateStrafingRight()
	else:
		stateParked()

def stopStrafing():
	global moving
	global strafing

	strafing = 0
	if moving == 1:
		stateMovingForward()
	elif moving == 2:
		stateMovingBackward()
	elif moving == 3:
		stateRotatingLeft()
	elif moving == 4:
		stateRotatingRight()
	else:
		stateParked()

def colorWipe(color, wait_ms=50):
	global call_queue

	for i in range(10):
		call_queue.append([i, color, wait_ms])

def stateParked(wait_ms=300):
	global call_queue
	global current_mode
	
	current_mode = "parked"

	clear()

	call_queue.append([0, Color(0,255,0), 0])
	call_queue.append([1, Color(255,255,0), 0])
	call_queue.append([2, Color(255,255,0), 0])
	call_queue.append([3, Color(0,0,0), 0])
	call_queue.append([4, Color(0,0,255), 0])	

	call_queue.append([5, Color(0,255,0), 0])
	call_queue.append([6, Color(255,255,0), 0])
	call_queue.append([7, Color(255,255,0), 0])
	call_queue.append([8, Color(0,0,0), 0])
	call_queue.append([9, Color(0,0,255), wait_ms])

	call_queue.append([0, Color(0,0,255), 0])
	call_queue.append([1, Color(0,0,0), 0])
	call_queue.append([2, Color(255,255,0), 0])	
	call_queue.append([3, Color(255,255,0), 0])
	call_queue.append([4, Color(0,255,0), 0])	

	call_queue.append([5, Color(0,0,255), 0])
	call_queue.append([6, Color(0,0,0), 0])
	call_queue.append([7, Color(255,255,0), 0])	
	call_queue.append([8, Color(255,255,0), 0])
	call_queue.append([9, Color(0,255,0), wait_ms])	

	call_queue.append(["goto", 0])

def stateMovingForward(wait_ms=200):
	global call_queue
	global current_mode
	global moving

	if current_mode == "move_forward":
		return

	current_mode = "move_forward"
	moving = 1

	clear()

	call_queue.append([0, Color(0,255,0), 0])
	call_queue.append([1, Color(0,255,0), 0])
	call_queue.append([2, Color(255,255,255), 0])
	call_queue.append([3, Color(0,0,255), 0])
	call_queue.append([4, Color(0,0,255), 0])	

	call_queue.append([5, Color(0,255,0), 0])
	call_queue.append([6, Color(0,255,0), 0])
	call_queue.append([7, Color(255,140,0), 0])
	call_queue.append([8, Color(0,0,255), 0])
	call_queue.append([9, Color(0,0,255), wait_ms])

	call_queue.append([0, Color(0,0,255), 0])
	call_queue.append([1, Color(0,0,255), 0])
	call_queue.append([2, Color(255,255,255), 0])	
	call_queue.append([3, Color(0,255,0), 0])
	call_queue.append([4, Color(0,255,0), 0])	

	call_queue.append([5, Color(0,0,255), 0])
	call_queue.append([6, Color(0,0,255), 0])
	call_queue.append([7, Color(255,140,0), 0])	
	call_queue.append([8, Color(0,255,0), 0])
	call_queue.append([9, Color(0,255,0), wait_ms])	

	call_queue.append(["goto", 0])

def stateMovingBackward(wait_ms=200):
	global call_queue
	global current_mode
	global moving

	if current_mode == "move_backward":
		return

	current_mode = "move_backward"
	moving = 2

	clear()

	call_queue.append([0, Color(0,255,0), 0])
	call_queue.append([1, Color(0,255,0), 0])
	call_queue.append([2, Color(255,140,0), 0])
	call_queue.append([3, Color(0,0,255), 0])
	call_queue.append([4, Color(0,0,255), 0])	

	call_queue.append([5, Color(0,255,0), 0])
	call_queue.append([6, Color(0,255,0), 0])
	call_queue.append([7, Color(255,255,255), 0])
	call_queue.append([8, Color(0,0,255), 0])
	call_queue.append([9, Color(0,0,255), wait_ms])

	call_queue.append([0, Color(0,0,255), 0])
	call_queue.append([1, Color(0,0,255), 0])
	call_queue.append([2, Color(255,140,0), 0])	
	call_queue.append([3, Color(0,255,0), 0])
	call_queue.append([4, Color(0,255,0), 0])	

	call_queue.append([5, Color(0,0,255), 0])
	call_queue.append([6, Color(0,0,255), 0])
	call_queue.append([7, Color(255,255,255), 0])	
	call_queue.append([8, Color(0,255,0), 0])
	call_queue.append([9, Color(0,255,0), wait_ms])	

	call_queue.append(["goto", 0])

def stateStrafingRight(wait_ms=50):
	global call_queue
	global current_mode
	global strafing

	if current_mode == "strafe_right":
		return

	current_mode = "strafe_right"
	strafing = 2

	clear()

	for i in range(5):
		call_queue.append([(5-i)%5, Color(0,0,255), 0])
		call_queue.append([(6-i)%5, Color(0,0,255), 0])
		call_queue.append([(7-i)%5, Color(0,255,0), 0])
		call_queue.append([(8-i)%5, Color(0,255,0), 0])
		call_queue.append([(9-i)%5, Color(0,255,255), 0])	

		call_queue.append([(5+i)%5+5, Color(0,255,255), 0])
		call_queue.append([(6+i)%5+5, Color(0,255,0), 0])
		call_queue.append([(7+i)%5+5, Color(0,255,0), 0])
		call_queue.append([(8+i)%5+5, Color(0,0,255), 0])
		call_queue.append([(9+i)%5+5, Color(0,0,255), wait_ms])

	call_queue.append(["goto", 0])

def stateStrafingLeft(wait_ms=50):
	global call_queue
	global current_mode
	global strafing

	if current_mode == "strafe_left":
		return

	current_mode = "strafe_left"
	strafing = 1

	clear()

	for i in range(5):
		call_queue.append([(0+i)%5, Color(0,255,255), 0])
		call_queue.append([(1+i)%5, Color(0,255,0), 0])
		call_queue.append([(2+i)%5, Color(0,255,0), 0])
		call_queue.append([(3+i)%5, Color(0,0,255), 0])
		call_queue.append([(4+i)%5, Color(0,0,255), 0])	

		call_queue.append([(5-i)%5+5, Color(0,0,255), 0])
		call_queue.append([(6-i)%5+5, Color(0,0,255), 0])
		call_queue.append([(7-i)%5+5, Color(0,255,0), 0])
		call_queue.append([(8-i)%5+5, Color(0,255,0), 0])
		call_queue.append([(9-i)%5+5, Color(0,255,255), wait_ms])

	call_queue.append(["goto", 0])

def stateRotatingLeft(wait_ms=30):
	global call_queue
	global current_mode
	global moving

	if current_mode == "rotate_left":
		return

	current_mode = "rotate_left"
	moving = 3

	clear()

	for i in range(5):
		call_queue.append([(0+i)%5, Color(0,255,0), 0])
		call_queue.append([(1+i)%5, Color(0,255,0), 0])
		call_queue.append([(2+i)%5, Color(0,0,255), 0])
		call_queue.append([(3+i)%5, Color(0,0,255), 0])
		call_queue.append([(4+i)%5, Color(0,0,255), 0])	

		call_queue.append([(0+i)%5+5, Color(0,255,0), 0])
		call_queue.append([(1+i)%5+5, Color(0,255,0), 0])
		call_queue.append([(2+i)%5+5, Color(0,0,255), 0])
		call_queue.append([(3+i)%5+5, Color(0,0,255), 0])
		call_queue.append([(4+i)%5+5, Color(0,0,255), wait_ms])

	call_queue.append(["goto", 0])

def stateRotatingRight(wait_ms=30):
	global call_queue
	global current_mode
	global moving

	if current_mode == "rotate_right":
		return

	current_mode = "rotate_right"
	moving = 4

	clear()

	for i in range(5):
		call_queue.append([(5-i)%5, Color(0,255,0), 0])
		call_queue.append([(6-i)%5, Color(0,255,0), 0])
		call_queue.append([(7-i)%5, Color(0,0,255), 0])
		call_queue.append([(8-i)%5, Color(0,0,255), 0])
		call_queue.append([(9-i)%5, Color(0,0,255), 0])	

		call_queue.append([(5-i)%5+5, Color(0,255,0), 0])
		call_queue.append([(6-i)%5+5, Color(0,255,0), 0])
		call_queue.append([(7-i)%5+5, Color(0,0,255), 0])
		call_queue.append([(8-i)%5+5, Color(0,0,255), 0])
		call_queue.append([(9-i)%5+5, Color(0,0,255), wait_ms])

	call_queue.append(["goto", 0])


clear()
