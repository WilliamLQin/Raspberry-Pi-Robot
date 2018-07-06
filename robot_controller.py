import pigpio 
import time

PIN_STRAFE = 22
PIN_LEFT = 25
PIN_RIGHT = 23
SPEED = 400
MIN_SPEED = 260
MAX_SPEED = 520
INCREMENT = 20

pi = pigpio.pi()

direction_strafe = 0
direction_left = 0
direction_right = 0

speed_strafe = MAX_SPEED
speed_left = MIN_SPEED - 20
speed_right = MIN_SPEED + 170
mode = 'strafe'

pi.set_servo_pulsewidth(PIN_STRAFE, 0)
pi.set_servo_pulsewidth(PIN_LEFT, 0)
pi.set_servo_pulsewidth(PIN_RIGHT, 0)

def change_control(key):
	global direction_strafe
	global direction_left
	global direction_right
	global speed_strafe
	global speed_left
	global speed_right
	global mode

	if key == '9':
		direction_left = 0.5
		direction_right = -0.5
	elif key == '7':
		direction_left = -0.5
		direction_right = 0.5
	elif key == '1':
		direction_strafe = 1
	elif key == '2':
		direction_strafe = 0
	elif key == '3': 
		direction_strafe = -1
	elif key == '5':
		direction_left = 1
		direction_right = 1
	elif key == '8':
		direction_left = 0
		direction_right = 0
	elif key == '0':
		direction_left = -1
		direction_right = -1
	
	if key == 'ch-':
		mode = 'left'
	elif key == 'ch':
		mode = 'strafe'
	elif key == 'ch+':
		mode = 'right'
	if key == 'vol-':
		if mode == 'left':
			speed_left -= INCREMENT
			if speed_left <= MIN_SPEED:
				speed_left = MIN_SPEED
		if mode == 'right':
			speed_right -= INCREMENT
			if speed_right <= MIN_SPEED:
				speed_right = MIN_SPEED
	elif key == 'vol+':
		if mode == 'left':
			speed_left += INCREMENT
			if speed_left >= MAX_SPEED:
				speed_left = MAX_SPEED
		if mode == 'right':
			speed_right += INCREMENT
			if speed_right >= MAX_SPEED:
				speed_right = MAX_SPEED


	if key == 'play':
		direction_left = 0
		direction_right = 0
		direction_strafe = 0

	if direction_left != 0:
		pi.set_servo_pulsewidth(PIN_LEFT, 1500 + speed_left*direction_left)
	else:
		pi.set_servo_pulsewidth(PIN_LEFT, 0)
	if direction_right != 0:
		pi.set_servo_pulsewidth(PIN_RIGHT, 1500 + speed_right*direction_right)
	else:
		pi.set_servo_pulsewidth(PIN_RIGHT, 0)
	if direction_strafe != 0:
		pi.set_servo_pulsewidth(PIN_STRAFE, 1500 + speed_strafe*direction_strafe)
	else:
		pi.set_servo_pulsewidth(PIN_STRAFE, 0)

	print key


