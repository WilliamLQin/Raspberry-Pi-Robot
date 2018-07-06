# Raspberry-Pi-Robot

![Robot](https://raw.githubusercontent.com/WilliamLQin/Raspberry-Pi-Robot/master/robot.jpg)

## External Resources

External resources were used in this project:
* pigpio python module for GPIO control: http://abyz.me.uk/rpi/pigpio/python.html
* rpi_ws281x for RGB LED strip control: https://github.com/jgarff/rpi_ws281x 

## Components

The robot has four main components to programming.

robot_bt.py is the main file that runs and handles Bluetooth and infrared signals
* It uses threads to run the Bluetooth, infrared, and LED clock controls simultaneously

robot_controller.py handles all servo motor speed and direction control
* It does this by setting the pulse width of signal to the servo motor to a certain width
** Widths 500-1500 move backwards
** Widths 1500-2500 move forwards
** Width 0 stops

robot_led.py controls the RGB LED strip and holds the various patterns
* It maintains a queue of commands to set LEDs in an orderly fashion
* It holds the robot state to determine which pattern to run when commands are issued

ir_hasher.py decodes data from the infrared receiver
* The Raspberry Pi has already been calibrated to the IR remote to receive certain hashes when buttons are pressed

## Getting Started

1) SSH into the Raspberry Pi and begin the program
* Enable the pigpio daemon
```
sudo pigpiod
```

* Run “sudo python robot_bt.py” to begin the program
```
sudo python robot_bt.py
```

Note: You can automate step one by adding these commands to /etc/rc.local. Then, when the Raspberry Pi is turned on, the commands will automatically run, so there is no need to SSH into the Raspberry Pi.


2) Connect to Bluetooth to control the robot
* Use a phone to connect to the Raspberry Pi with a Bluetooth terminal

3) Control the robot with either Bluetooth or infrared!
* Bluetooth: used the keypad as seen in Figure 4 to control the robot
*	Infrared: press buttons as seen in Figure 5 to control the robot

4) When done, enter “q” in the Bluetooth terminal to quit the program


