import time
import pigpio
import bluetooth
import robot_controller
import robot_led
from neopixel import *
import threading
import ir_hasher

pi = pigpio.pi()

pi.write(26, 1)

server_socket = None
client_socket = None

end = False

def checkBT():
	global server_socket
	global client_socket
	global end

	while 1:
		data = client_socket.recv(1024)
		print ("Received:", data)
		if data == "q":
			quit()
		elif data == "c":
			robot_led.clear()
			robot_led.colorWipe(Color(0,255,0))
		else:
			robot_controller.change_control(data)

		setRobotState(data)

		time.sleep(0.001)

		if end:
			break

def led_clock():
	global end

	while 1:
		robot_led.clock()
		time.sleep(0.001)
	
		if end:
			break

def callback(hash):
	if hash in ir_hasher.hashes:
		key = ir_hasher.hashes[hash]
		
		if key == "2":
			key = "5"
		elif key == "5":
			key = "8"
		elif key == "8":
			key = "0"
		elif key == "0":
			key = "1"
		elif key == "100+":
			key = "2"
		elif key == "200+":
			key = "3"
		elif key == "4":
			key = "7"
		elif key == "6":
			key = "9"
		elif key == "1" or "3" or "7" or "9":
			return
		
		setRobotState(key)
		robot_controller.change_control(key)

def setRobotState(key):
	if key == "5":
		robot_led.stateMovingForward()
	elif key == "0":
		robot_led.stateMovingBackward()
	elif key == "1":
		robot_led.stateStrafingLeft()
	elif key == "3":
		robot_led.stateStrafingRight()
	elif key == "7":
		robot_led.stateRotatingLeft()
	elif key == "9":
		robot_led.stateRotatingRight()
	elif key == "8":
		robot_led.stopMoving()
	elif key == "2":
		robot_led.stopStrafing()
	elif key == "play":
		robot_led.stopMoving()
		robot_led.stopStrafing()
		
def quit():
	global client_socket
	global server_socket
	global end

	print("Quit")
	robot_controller.change_control("play")
	pi.write(26, 0)
	robot_led.off()
	
	end = True

	if client_socket is not None:
		client_socket.close()

	if server_socket is not None:
		server_socket.close()

	pi.stop()

server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
port = 1
server_socket.bind(("",port))
server_socket.listen(1)

client_socket,address = server_socket.accept()
print ("Accepted connection from ", address)
	
ir = ir_hasher.hasher(pi, 13, callback, 5) 

threading.Thread(target=checkBT).start()

threading.Thread(target=led_clock).start()


