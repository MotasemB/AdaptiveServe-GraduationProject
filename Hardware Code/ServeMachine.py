import RPi.GPIO as GPIO
import time

#assign GPIO pin numbers to different switches on relay
FrequencyInc = 3
FrequencyDec = 5
OscillationInc = 11
OscillationDec = 13
TopspinInc = 19
TopspinDec = 21
BackspinInc = 35
BackspinDec = 37 

#counters to keep track of different adjustmnets
FrequencyCounter = 1
OscillationCounter = 1
TopspinCounter = 1
BackspinCounter = 1

def IncFrequency():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(FrequencyInc, GPIO.OUT)

    GPIO.output(FrequencyInc, GPIO.LOW)
    time.sleep(0.03)
    GPIO.cleanup()
    global FrequencyCounter 
    FrequencyCounter += 1 

def DecFrequency():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(FrequencyDec, GPIO.OUT)

    GPIO.output(FrequencyDec, GPIO.LOW)
    time.sleep(0.03)
    GPIO.cleanup()
    global FrequencyCounter 
    FrequencyCounter -= 1 

def IncOscillation():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(OscillationInc, GPIO.OUT)

    GPIO.output(OscillationInc, GPIO.LOW)
    time.sleep(0.03)
    GPIO.cleanup()
    global OscillationCounter 
    OscillationCounter += 1 

def DecOscillation():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(OscillationDec, GPIO.OUT)

    GPIO.output(OscillationDec, GPIO.LOW)
    time.sleep(0.03)
    GPIO.cleanup()
    global OscillationCounter 
    OscillationCounter -= 1 

def IncTopspin():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(TopspinInc, GPIO.OUT)

    GPIO.output(TopspinInc, GPIO.LOW)
    time.sleep(0.03)
    GPIO.cleanup()
    global TopspinCounter 
    TopspinCounter += 1 

def DecTopspin():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(TopspinDec, GPIO.OUT)

    GPIO.output(TopspinDec, GPIO.LOW)
    time.sleep(0.03)
    GPIO.cleanup()
    global TopspinCounter 
    TopspinCounter -= 1
    
def IncBackspin():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BackspinInc, GPIO.OUT)

    GPIO.output(BackspinInc, GPIO.LOW)
    time.sleep(0.03)
    GPIO.cleanup()
    global BackspinCounter 
    BackspinCounter += 1 

def DecBackspin():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BackspinDec, GPIO.OUT)

    GPIO.output(BackspinDec, GPIO.LOW)
    time.sleep(0.03)
    GPIO.cleanup()
    global BackspinCounter 
    BackspinCounter -= 1 

#test to make sure switches are working
#IncFrequency()
#time.sleep(1)
#DecFrequency()
#time.sleep(1)

#IncOscillation()
#time.sleep(1)
#DecOscillation()
#time.sleep(1)

#IncTopspin()
#time.sleep(1)
#DecTopspin()
#time.sleep(1)

#IncBackspin()
#time.sleep(1)
#DecBackspin()



