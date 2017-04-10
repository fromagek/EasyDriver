#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as gpio
import time, sys

class Switch(object):
    def __init__(self,pin_switch=0):
        self.pin_switch = pin_switch
	gpio.setmode(gpio.BCM)
	gpio.setup(self.pin_switch,gpio.IN)

    def switch_status(self):
        return gpio.input(self.pin_switch)
