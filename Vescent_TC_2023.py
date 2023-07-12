import os
import serial as serial  #first:  pip install pyserial
from datetime import datetime, timedelta
import time
#import matplotlib.pyplot as plt
#from datetime import date
from ramps import rampdef



# define vescent coms
com = 'COM4'#onr laptop
#com = 'COM3' my laptop


def establish_com(com): #takes ser in case ser already exists
    try:
        ser = serial.Serial(com, baudrate=9600, parity='N', stopbits=1, timeout=0, bytesize=8, xonxoff=0, rtscts=0)
        print(com+' connected')
        return (ser)
    except:
        print('Serial port connection failed.  Already connected / open? Connected in other tab?')
    time.sleep(1)

def servo_enable(channel):
   serstr = 'Control '+str(channel)+' 3\r\n'  # ch command ( 1 manual off, 1 servo off, 2, manual on, 3, servo on)
   serstr=bytes(serstr,'ascii')
   ser.write(serstr)
   print('Enabing ch '+str(channel))
   time.sleep(1) #normally I don't like using sleep (instead use while loops like below, e.g.), but this is a short fixed sleep

def set_Vesc_temp(ser, channel, T_C): #ch 1,2,3,4
    setTempstring = 'TempSet ' + str(channel) + ' ' + str(T_C) + '\r\n'
    serstr = bytes(setTempstring, 'ascii')
    ser.write(serstr)
    confirm = ser.readline().decode('utf-8')[:-4]
    while confirm == '':  # avoid empty returns, no need for sleep delay
        confirm = ser.readline().decode('utf-8')[:-4]
    msg='Channel '+str(channel)+' set to ' + confirm + ' °C: ' + str(datetime.now())
    print(msg)#'Channel '+str(channel)+' set to ' + confirm + ' °C: ' + str(datetime.now()))
    logtofile(logfilename,msg)
    if float(confirm)!=T_C:
        print('Setpoint not correct, T limit exceeded?')
    #   servo_enable(CH) #this would make sure the channel is on, but causes a short glitch as it resets.

def logtofile(filename,infostring):
    try:
        import os
        cwd = os.getcwd()
        os.makedirs(cwd + '/logs')
    except:
        print('folder not created (already exists?)')
    import logging
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(filename=filename, level=logging.INFO)
    logging.info(infostring)
   # logging.debug('abc method started...')


print('Start')
# start_time=datetime.now()
print(datetime.now())


rampname = '87/32 retrace 20h+4h'#'test'#
Temperatures,Elapsed_m, start_time, repeats, repeat_interval_m = rampdef(rampname)

if start_time == 'now':
    start_time = datetime.now()

logfilename = start_time.strftime('./logs/logfile_%Y-%m-%d_%H-%M-%S.log')#'./logs/'+str(start_time)+'.log'
Timelist = []
for m in Elapsed_m:
    Timelist.append(start_time+timedelta(minutes=m))
print(Timelist)
logtofile(logfilename, 'ramp definitions: '+rampname)
logtofile(logfilename,'Elapsed_m:  '+str(Elapsed_m))
logtofile(logfilename,'Temperature setpoints: '+str(Temperatures))
logtofile(logfilename,'Repeats:  '+str(repeats))
logtofile(logfilename,'Repeat Interval (m): '+str(repeat_interval_m))
logtofile(logfilename,'---------------------------------------------')

#main loop
while(repeats>0):
    loopstart_t=datetime.now()
    last_time = Timelist[-1]
    first_time = Timelist[0]
    while(datetime.now()< last_time):#+repeat_interval_m): #runs until last point is set, then repeats  #<loopstart_t+timedelta(seconds = 10)): #use loopstart for testing
       # print('sequence ends in :' + str(last_time-datetime.now()))
        print('sequence begins in :' + str(first_time - datetime.now()))

        #print(datetime.now())
        #for i, timeset in enumerate(Timelist):
        #time.sleep(1)
        for i in range(0,len(Timelist),1):
            #loopran = 0
            if datetime.now()>Timelist[i]:# && loopran=0:
                ser = establish_com(com)
                print(ser)
                #ser.open()
                for Vchannel, channel_seq in enumerate(Temperatures):
                    # print(Vchannel+1)
                    # print(channel_seq)
                    # print(Temperatures[channel_seq][i])
                    #channel in range(1,len(Temperatures)+1,1):
                    set_Vesc_temp(ser, Vchannel+1, Temperatures[channel_seq][i])
                #loopran = 1;
                Timelist[i] += timedelta(weeks=100)  # blow up the time so the channel isnt repeatedly set, timelist is reinitialized for subsequent repeats
                try:
                    ser.close()
                except:
                    print('com connection close failed')

        time.sleep(60) #60
    repeats -= 1
    print('Repeats left: ' + str(repeats))

    Timelist = [] #redo time list
    start_time+=timedelta(minutes = repeat_interval_m)
    for m in Elapsed_m:
        #Timelist.append(datetime.now() + timedelta(minutes=m))
        Timelist.append(start_time + timedelta(minutes=m))
logtofile(logfilename,'done')
ser.close()

