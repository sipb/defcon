#!/usr/bin/python
# -*- coding: utf-8 -*-
# usage: display.py VALUE
# sets the relevant Rasperry Pi GPIO output pins to drive a 7-segment display to display VALUE

import RPi.GPIO as GPIO
import sys

def main(value):
    
    # use P1 header pin numbering convention
    GPIO.setmode(GPIO.BOARD)
    
    # map 7-seg segment labels to GPIO pin numbers (P1 labelling convention)
    # 7-seg segment labels start at top segment, proceed clockwise, and terminate in the center
    seg_A = 3
    seg_B = 5
    seg_C = 7
    seg_D = 11
    seg_E = 13
    seg_F = 15
    seg_G = 19
    
    # setup output pins
    GPIO.setup(seg_A, GPIO.OUT)
    GPIO.setup(seg_B, GPIO.OUT)
    GPIO.setup(seg_C, GPIO.OUT)
    GPIO.setup(seg_D, GPIO.OUT)
    GPIO.setup(seg_E, GPIO.OUT)
    GPIO.setup(seg_F, GPIO.OUT)
    GPIO.setup(seg_G, GPIO.OUT)

    # push proper outputs to GPIO pins to display value
    if value == ' ': # an input of a single space will blank the display
        GPIO.output(seg_A, GPIO.LOW)
        GPIO.output(seg_B, GPIO.LOW)
        GPIO.output(seg_C, GPIO.LOW)
        GPIO.output(seg_D, GPIO.LOW)
        GPIO.output(seg_E, GPIO.LOW)
        GPIO.output(seg_F, GPIO.LOW)
        GPIO.output(seg_G, GPIO.LOW)
    elif value == '0':
        GPIO.output(seg_A, GPIO.HIGH)
        GPIO.output(seg_B, GPIO.HIGH)
        GPIO.output(seg_C, GPIO.HIGH)
        GPIO.output(seg_D, GPIO.HIGH)
        GPIO.output(seg_E, GPIO.HIGH)
        GPIO.output(seg_F, GPIO.HIGH)
        GPIO.output(seg_G, GPIO.LOW)
    elif value == '1':
        GPIO.output(seg_A, GPIO.LOW)
        GPIO.output(seg_B, GPIO.HIGH)
        GPIO.output(seg_C, GPIO.HIGH)
        GPIO.output(seg_D, GPIO.LOW)
        GPIO.output(seg_E, GPIO.LOW)
        GPIO.output(seg_F, GPIO.LOW)
        GPIO.output(seg_G, GPIO.LOW)
    elif value == '2':
        GPIO.output(seg_A, GPIO.HIGH)
        GPIO.output(seg_B, GPIO.HIGH)
        GPIO.output(seg_C, GPIO.LOW)
        GPIO.output(seg_D, GPIO.HIGH)
        GPIO.output(seg_E, GPIO.HIGH)
        GPIO.output(seg_F, GPIO.LOW)
        GPIO.output(seg_G, GPIO.HIGH)
    elif value == 'e':
        GPIO.output(seg_A, GPIO.HIGH)
        GPIO.output(seg_B, GPIO.HIGH)
        GPIO.output(seg_C, GPIO.LOW)
        GPIO.output(seg_D, GPIO.HIGH)
        GPIO.output(seg_E, GPIO.HIGH)
        GPIO.output(seg_F, GPIO.HIGH)
        GPIO.output(seg_G, GPIO.HIGH)
    elif value == '3':
        GPIO.output(seg_A, GPIO.HIGH)
        GPIO.output(seg_B, GPIO.HIGH)
        GPIO.output(seg_C, GPIO.HIGH)
        GPIO.output(seg_D, GPIO.HIGH)
        GPIO.output(seg_E, GPIO.LOW)
        GPIO.output(seg_F, GPIO.LOW)
        GPIO.output(seg_G, GPIO.HIGH)
    elif value == 'π':
        GPIO.output(seg_A, GPIO.HIGH)
        GPIO.output(seg_B, GPIO.HIGH)
        GPIO.output(seg_C, GPIO.HIGH)
        GPIO.output(seg_D, GPIO.LOW)
        GPIO.output(seg_E, GPIO.HIGH)
        GPIO.output(seg_F, GPIO.HIGH)
        GPIO.output(seg_G, GPIO.LOW)
    elif value == '4':
        GPIO.output(seg_A, GPIO.LOW)
        GPIO.output(seg_B, GPIO.HIGH)
        GPIO.output(seg_C, GPIO.HIGH)
        GPIO.output(seg_D, GPIO.LOW)
        GPIO.output(seg_E, GPIO.LOW)
        GPIO.output(seg_F, GPIO.HIGH)
        GPIO.output(seg_G, GPIO.HIGH)
    elif value == '5':
        GPIO.output(seg_A, GPIO.HIGH)
        GPIO.output(seg_B, GPIO.LOW)
        GPIO.output(seg_C, GPIO.HIGH)
        GPIO.output(seg_D, GPIO.HIGH)
        GPIO.output(seg_E, GPIO.LOW)
        GPIO.output(seg_F, GPIO.HIGH)
        GPIO.output(seg_G, GPIO.HIGH)
    else:
        print "Invalid input.\nPlease set the DEFCON value to a single digit between 1 and 5.\nThe physical display has not been changed and will update when the next valid value is set."

if __name__ == "__main__":
    main(sys.argv[1])
