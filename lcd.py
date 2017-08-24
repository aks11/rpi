#!/usr/bin/python3

import RPi.GPIO as GPIO
import time

####	Hardware Pins
RS = 21
EN = 5

D4 = 6
D5 = 13
D6 = 19
D7 = 26

DATA = 1
CMD = 0

####	Lines
LINE1 = 0x80
LINE2 = 0xC0
LINE3 = 0x94
LINE4 = 0xD4

####	Special Charaters
SPACE = 0x20
BLOCK = 0xFF

def enable():
	time.sleep(0.00005) # 50usec
	GPIO.output(EN,GPIO.HIGH)
	time.sleep(0.00005) # 50usec
	GPIO.output(EN,GPIO.LOW)	

def default():
	GPIO.output(RS,GPIO.LOW)
	GPIO.output(EN,GPIO.LOW)
	GPIO.output(D4,GPIO.LOW)
	GPIO.output(D5,GPIO.LOW)
	GPIO.output(D6,GPIO.LOW)
	GPIO.output(D7,GPIO.LOW)

def wbyte(value, data):
	# set RS line
	if data == 1:
		GPIO.output(RS,GPIO.HIGH)
	else:
		GPIO.output(RS,GPIO.LOW)
	time.sleep(0.00005) # 50usec

	# send higher nibble
	if ((value >> 4) & 1) == 1:
		GPIO.output(D4,GPIO.HIGH)
	else:
		GPIO.output(D4,GPIO.LOW)
	if ((value >> 5) & 1) == 1:
		GPIO.output(D5,GPIO.HIGH)
	else:
		GPIO.output(D5,GPIO.LOW)
	if ((value >> 6) & 1) == 1:
		GPIO.output(D6,GPIO.HIGH)
	else:
		GPIO.output(D6,GPIO.LOW)
	if ((value >> 7) & 1) == 1:
		GPIO.output(D7,GPIO.HIGH)
	else:
		GPIO.output(D7,GPIO.LOW)
	enable()

	# Write lower 4 bits
	if ((value >> 0) & 1) == 1:
		GPIO.output(D4,GPIO.HIGH)
	else:
		GPIO.output(D4,GPIO.LOW)
	if ((value >> 1) & 1) == 1:
		GPIO.output(D5,GPIO.HIGH)
	else:
		GPIO.output(D5,GPIO.LOW)
	if ((value >> 2) & 1) == 1:
		GPIO.output(D6,GPIO.HIGH)
	else:
		GPIO.output(D6,GPIO.LOW)
	if ((value >> 3) & 1) == 1:
		GPIO.output(D7,GPIO.HIGH)
	else:
		GPIO.output(D7,GPIO.LOW)
	enable()
	
	time.sleep(0.00005) # 50usec
	default()	# put in default
	
def clear():
	wbyte(0x01,CMD)
	wbyte(LINE1,CMD)
	
def wstring(str):
	for index in str:
		wbyte(ord(index),1)
	default()

def init():
	GPIO.setwarnings(False)

	GPIO.setmode(GPIO.BCM)

	# setup as output
	GPIO.setup(RS,GPIO.OUT)
	GPIO.setup(EN,GPIO.OUT)
	GPIO.setup(D4,GPIO.OUT)
	GPIO.setup(D5,GPIO.OUT)
	GPIO.setup(D6,GPIO.OUT)
	GPIO.setup(D7,GPIO.OUT)

	# default LOW
	default()

	time.sleep(1) # for VDD rise
	
	# cmd
	wbyte(0x3,0)
	time.sleep(0.05) # 50msec
	
	wbyte(0x3,0)
	time.sleep(0.05) # 50msec
	
	wbyte(0x3,0)
	time.sleep(0.05) # 50msec

	wbyte(0x2,0)
	time.sleep(0.05) # 50msec

	wbyte(0x28,0)
	time.sleep(0.05) # 50msec

	wbyte(0x06,0)
	time.sleep(0.05) # 50msec

	wbyte(0x01,0)	# clear
	time.sleep(0.05) # 50msec

	wbyte(0x0C,0)	# cursor,blink off
	time.sleep(0.05) # 50msec

	wbyte(LINE1,0)
	time.sleep(0.05) # 50msec

def main():

	print("\nInterfacing LCD(JHD204a) with RPI3 & Python.")
	print("\nThis program runs indefinitely.\nTo quit, Press Ctrl+c...")

	init()
	time.sleep(0.001) # 100msec

	wbyte(LINE1,CMD)
	wstring("++++++++++++++++++++")

	wbyte(LINE2,CMD)
	wstring("+ THIS IS LCD TEST +")

	wbyte(LINE3,CMD)
	wstring("+                  +")

	wbyte(LINE4,CMD)
	wstring("++++++++++++++++++++")
	
	tgl=0
	while True:
		time.sleep(1)
		
		if tgl == 0:
			tgl = 1
			
			wbyte(LINE2,CMD)
			wstring("+ THIS IS LCD TEST +")
		
			wbyte(LINE3,CMD)
			wstring("+                  +")
		else:
			tgl = 0
			
			wbyte(LINE2,CMD)
			wstring("+                  +")
		
			wbyte(LINE3,CMD)
			wstring("+ THIS IS LCD TEST +")

if __name__ == "__main__":
	main()
	GPIO.close()
