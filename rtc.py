#!/usr/bin/python3

import smbus
import time
import subprocess

bus = smbus.SMBus(1)

#	PCF8563
address = 0x51

#	If '1', current RTC time will be set as system time
setSystemTime=0

########################################################
####    Write Date Time Register
####    Format:- [secs,min,hour,date,day,month,year]
####    Note:- ALL values must be in BCD and should not\
####        excced their MAX values
####    secs  -> MIN = 0x00, MAX = 0x59
####    min   -> MIN = 0x00, MAX = 0x59
####    hour  -> MIN = 0x00, MAX = 0x23
####    date  -> MIN = 0x01, MAX = 0x31
####    days  -> MIN = 0x00, MAX = 0x06, 0 = MONDAY,...
####    month -> MIN = 0x01, MAX = 0x12
####    year  -> MIN = 0x00, MAX = 0x99
########################################################
#WriteDateTime = [0,0x02,0x9,0x14,0x1,0x3,0x17]
#bus.write_i2c_block_data(address,0x02,WriteDateTime)

print("***************************")
print("****    PCF8563 RTC    ****")
print("***************************")

while True:
    time.sleep(1)
    ReadDateTime = bus.read_i2c_block_data(address,0x02,8)
    
    secs = ReadDateTime[0]
    minute = ReadDateTime[1]
    hours = ReadDateTime[2]
    date = ReadDateTime[3]
    days = ReadDateTime[4]
    month = ReadDateTime[5]
    year = ReadDateTime[6]

    #print(hex(year)+" "+hex(month)+" "+hex(date)+" "+hex(days)+" "+hex(hours)+" "+hex(minute)+" "+hex(secs))

    # BCD into integer
    secs = secs & 0x7F
    secs = (secs>>4)*10 + (secs & 0xF)
    
    minute = minute & 0x7F
    minute = (minute>>4)*10 + (minute & 0xF)

    hours = hours & 0x3F
    hours = (hours>>4)*10 + (hours & 0xF)
    
    date = date & 0x3F
    date = (date>>4)*10 + (date & 0xF)

    days = days & 0x7
    days = (days>>4)*10 + (days & 0xF)

    month = month & 0x1F
    month = (month>>4)*10 + (month & 0xF)

    year = year & 0xFF
    year = (year>>4)*10 + (year & 0xF)  

    #print("\nCurrent Time:")
    #print(str(hours)+":"+str(minute)+":"+str(secs))    
    #print("\nCurrent Date:")
    #print(str(days)+", "+str(date)+"/"+str(month)+"/"+str(year+2000))

    timedate = str(year+2000)+"-"+str(month)+"-"+str(date)+" "+str(hours)+":"+str(minute)+":"+str(secs)
    print(timedate)

    if setSystemTime == 1:
        #	date -s "2017-1-12 17:35:50"
        subprocess.call(["sudo","date","-s",timedate])
        setSystemTime=0
