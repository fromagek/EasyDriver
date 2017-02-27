#!/usr/bin/python
# -*- coding: utf-8 -*-

# Simple example of the easydriver Python library.
# Dave Finch 2013

import easydriver as ed
import time

# Direction of rotation is dependent on how the motor is connected.
# If the motor runs the wrong way swap the values of cw and ccw.
cw = True
ccw = False

"""
Arguments to pass or set up after creating the instance.

Step GPIO pin number.
Delay between step pulses in seconds.
Direction GPIO pin number.
Microstep 1 GPIO pin number.
Microstep 2 GPIO pin number.
Microstep 3 GPIO pin number.
Sleep GPIO pin number.
Enable GPIO pin number.
Reset GPIO pin number.
Name as a string.
"""

# Create an instance of the easydriver class.
# Not using sleep, enable or reset in this example.
stepper = ed.easydriver(pin_step=27,delay=0.1,pin_direction=17,pin_ms1=25,pin_ms2=23,pin_ms3=21,pin_sleep=10,pin_enable=22,name="Stepper")

# Set motor direction to clockwise.
stepper.set_direction(ccw)

# Set the motor to run in 1/8 of a step per pulse.
stepper.set_eighth_step()
stepper.wake()

# Do some steps.
for i in range(0,100):
    stepper.step()
stepper.sleep()
time.sleep(9)
stepper.wake()
for i in range(0,100):
	stepper.set_direction(cw)
	stepper.step()
stepper.sleep()
# Clean up (just calls GPIO.cleanup() function.)
stepper.finish()
