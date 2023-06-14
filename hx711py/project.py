#! /usr/bin/python2

import time
import sys
EMULATE_HX711=False

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711
    
referenceUnit = -473
DT_PIN = 5
SCK_PIN = 6
COLD_PIN = 26
HOT_PIN = 4

GPIO.setmode(GPIO.BCM)

hx = HX711(DT_PIN, SCK_PIN)
hx.set_reading_format("MSB", "MSB")
GPIO.setup(COLD_PIN,GPIO.OUT)
GPIO.setup(HOT_PIN,GPIO.OUT)


def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()
        
    print("Bye!")
    sys.exit()

def init():

    hx.set_reference_unit(referenceUnit)
    hx.reset()
    hx.tare()
    GPIO.output(COLD_PIN,0)
    GPIO.output(HOT_PIN,0)

    print("Tare done! ")
def measure():
    val = max(0, int(hx.get_weight(5)))
    hx.power_down()
    hx.power_up()
    if val>=0:
        print(f'weight: {val}')
    time.sleep(0.2)
    return val 
def pumping(target_weight=300,mode="cold"):
    weight = 0
    offset = 3
    hx.set_reference_unit(referenceUnit)
    hx.reset()
    hx.tare()
    print("tare before pump")

    #hx.tare()
    weight = measure()
    while weight<target_weight-offset :
        try : 
            weight = measure()
            if mode=='cold':
                GPIO.output(COLD_PIN,1)
            elif mode =='hot':
                GPIO.output(HOT_PIN,1)
        except (KeyboardInterrupt, SystemExit):
            if mode=='cold':
                GPIO.output(COLD_PIN,0)
            elif mode =='hot':
                GPIO.output(HOT_PIN,0)
            cleanAndExit()
    if mode=='cold':
        GPIO.output(COLD_PIN,0)
    elif mode =='hot':
        GPIO.output(HOT_PIN,0)
    #cleanAndExit()
    
def mycallback(channel):                                                 
    print("Button pressed @", time.ctime())

def main():
    KEY_PRESSED = True # make a function about it 
    try: 
        amount= 100 # make a function about it 
        
        while True :
            pumping(target_weight=100,mode='hot')
            time.sleep(5)
            pumping(target_weight=100,mode='cold')
            time.sleep(5)


        #previous_Status = input
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()


    
if __name__=='__main__':
    init()
    main()
    cleanAndExit()
