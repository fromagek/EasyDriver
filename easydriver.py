#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as gpio
import time, sys
from switch import Switch


class easydriver(object):
    def __init__(self,pin_step=0,delay=0.1,pin_direction=0,pin_ms1=0,pin_ms2=0,pin_ms3=0,\
    			 pin_sleep=0,pin_enable=0,pin_reset=0,name="Stepper",pin_left_end=0,pin_right_end=0):
        self.pin_step = pin_step
        self.delay = delay / 2
        self.abs_position=self.read_abs_position()
        self.pin_direction = pin_direction
        self.direction=True
        self.pin_microstep_1 = pin_ms1
        self.pin_microstep_2 = pin_ms2
        self.pin_microstep_3 = pin_ms3
        self.pin_sleep = pin_sleep
        self.pin_enable = pin_enable
        self.pin_reset = pin_reset
        self.name = name
        self.pin_left_end = pin_left_end
        self.pin_right_end = pin_right_end
        self.left_switch = Switch(pin_left_end)
        self.right_switch = Switch(pin_right_end)
        self.left_limit=0
        self.right_limit=100
	
        gpio.setmode(gpio.BCM)
        gpio.setwarnings(False)

        if self.pin_step > 0:
            gpio.setup(self.pin_step, gpio.OUT)
        if self.pin_direction > 0:
            gpio.setup(self.pin_direction, gpio.OUT)
            gpio.output(self.pin_direction, True)
        if self.pin_microstep_1 > 0:
            gpio.setup(self.pin_microstep_1, gpio.OUT)
            gpio.output(self.pin_microstep_1, False)
        if self.pin_microstep_2 > 0:
            gpio.setup(self.pin_microstep_2, gpio.OUT)
            gpio.output(self.pin_microstep_2, False)
        if self.pin_microstep_3 > 0:
            gpio.setup(self.pin_microstep_3, gpio.OUT)
            gpio.output(self.pin_microstep_3, False)
        if self.pin_sleep > 0:
            gpio.setup(self.pin_sleep, gpio.OUT)
            gpio.output(self.pin_sleep,True)
        if self.pin_enable > 0:
            gpio.setup(self.pin_enable, gpio.OUT)
            gpio.output(self.pin_enable,False)
        if self.pin_reset > 0:
            gpio.setup(self.pin_reset, gpio.OUT)
            gpio.output(self.pin_reset,True)
        self.sleep()

    def step(self):
    	if self.left_limit<self.abs_position and self.direction or self.abs_position<self.right_limit and not self.direction:
	    	self.wake()
	        gpio.output(self.pin_step,True)
	        time.sleep(self.delay)
	        gpio.output(self.pin_step,False)
	        time.sleep(self.delay)
	        if not self.direction:
	        	self.add_to_abs_position(1)
	        else:
	        	self.add_to_abs_position(-1)
     	print(self.abs_position)
        	
    def set_direction(self,direction):
    	self.direction=direction
        gpio.output(self.pin_direction,self.direction)

    def set_full_step(self):
        gpio.output(self.pin_microstep_1,False)
        gpio.output(self.pin_microstep_2,False)
        gpio.output(self.pin_microstep_3,False)
        
    def set_half_step(self):
        gpio.output(self.pin_microstep_1,True)
        gpio.output(self.pin_microstep_2,False)
        gpio.output(self.pin_microstep_3,False)
        
    def set_quarter_step(self):
        gpio.output(self.pin_microstep_1,False)
        gpio.output(self.pin_microstep_2,True)
        gpio.output(self.pin_microstep_3,False)
        
    def set_eighth_step(self):
        gpio.output(self.pin_microstep_1,True)
        gpio.output(self.pin_microstep_2,True)
        gpio.output(self.pin_microstep_3,False)

    def set_sixteenth_step(self):
        gpio.output(self.pin_microstep_1,True)
        gpio.output(self.pin_microstep_2,True)
        gpio.output(self.pin_microstep_3,True)
        
    def add_to_abs_position(self,delta):
    	self.abs_position+=delta
    	self.write_abs_position(str(self.abs_position))
    	
    def set_abs_position_zero(self):
    	self.abs_position=0
    	self.write_abs_position(self.abs_position)
    	
    def sleep(self):
        gpio.output(self.pin_sleep,False)

    def wake(self):
        gpio.output(self.pin_sleep,True)
    
    def disable(self):
        gpio.output(self.pin_enable,True)

    def enable(self):
        gpio.output(self.pin_enable,False)

    def reset(self):
        gpio.output(self.pin_reset,False)
        time.sleep(1)
        gpio.output(self.pin_reset,True)

    def set_delay(self, delay):
        self.delay = delay / 2
        
    def read_abs_position(self):
    	file=open('abs_pos.txt','r')
    	self.abs_position=eval(file.readline())
    	file.close()
    	return self.abs_position
        
    def write_abs_position(self, abs_pos):
    	file=open('abs_pos.txt','w')
    	file.write(str(abs_pos))
    	file.close()
    	self.abs_position=int(abs_pos)
        
    def left_switch_status(self):
		return self.left_switch.switch_status()
		
    def find_left_end_stop(self):
    	self.set_direction(False)
    	while not (self.left_switch_status()):
			self.step()
    	self.set_abs_position_zero()
	
    def finish(self):
    	if self.pin_sleep!=0:
    		self.sleep()
    		print('sleep')
        gpio.cleanup()
