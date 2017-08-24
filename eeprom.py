#!/usr/bin/python3

import smbus
import time

i2c = None

def set_addr(slave, addr):
	global i2c
	addrH = addr//256	# floor division - truncate to integer
	addrL = addr%256
	
	try:
		i2c.write_i2c_block_data(slave, addrH, [addrL])
	finally:
		time.sleep(0.015) # data sheet says 10 msec max

def read_byte(slave):
	global i2c
	return i2c.read_byte(slave)

def write_byte(slave, addr, byte):
	global i2c
	
	addrH = addr//256	# floor division - truncate to integer
	addrL = addr%256

	try:
		i2c.write_i2c_block_data(slave, addrH, [addrL,byte])
	finally:
		time.sleep(0.015) # data sheet says 10 msec max

####	Convert STRING into LIST i.e
####	"01234" ---> [48,49,50,51,52]
def str2list(str):
	return list(str.encode('utf-8'))

####	Convert LIST into STRING i.e
####	[48,49,50,51,52] ---> "01234"
def list2str(lst):
	chrlst = []
	
	for i in range(len(lst)):
		chrlst.append(chr(lst[i]))

	return "".join(chrlst)

####	Open i2c <bus>
def open(bus):
	global i2c
	i2c = smbus.SMBus(bus)
	
####	Close i2c <bus>
def close():
	global i2c
	i2c.close()

####	Read block of <count> number of bytes from <addr>
def read_block(slave, addr, count):
	rdata = []	# empty list, to be filled
	
	set_addr(slave,addr)
	for i in range(0,count):
		rdata.append(read_byte(slave))

	return rdata

####	Write block of <data> to <addr>
def write_block(slave, addr, data):
	global i2c
	
	addrH = addr//256	# floor division - truncate to integer
	addrL = addr%256
	
	wdata = [addrL] + data
	
	try:
		i2c.write_i2c_block_data(slave, addrH, wdata)
	finally:
		time.sleep(0.015) # data sheet says 10 msec max

if __name__ == '__main__':
	print("++++++++++++++++++++++++++++++++++")
	print("++++     eeprom.py module     ++++")
	print("++++++++++++++++++++++++++++++++++\n")
	
	slaveaddr= 0x50		# EEPROM Slave Address - 7bit
	addrloc = 0		# memory pointer location
	rcount = 36			# number of bytes to read from memory
	
	open(1)		# i2c bus 1

	print("Reading",rcount,"bytes from loc=", addrloc)
	rdata = read_block(slaveaddr, addrloc, rcount)
	print(">>  RAW=", rdata)
	print(">>ASCII=", list2str(rdata))

	wdata = "+ABCDEFGHI0123456789abcdefghi+"
	print("\nWriting data=",wdata, "at loc=",addrloc)
	write_block(slaveaddr,addrloc,str2list(wdata))

	close()
