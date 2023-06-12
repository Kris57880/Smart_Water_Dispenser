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
CTL_PIN = 26
BOTTON_PIN = 17

GPIO.setmode(GPIO.BCM)

hx = HX711(DT_PIN, SCK_PIN)
hx.set_reading_format("MSB", "MSB")
GPIO.setup(CTL_PIN,GPIO.OUT)
GPIO.setup(BOTTON_PIN,GPIO.IN)


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
    print("Tare done! ")
def measure():
    val = max(0, int(hx.get_weight(5)))
    hx.power_down()
    hx.power_up()
    if val!=0:
        print(f'weight: {val}')
    #time.sleep(0.2)
    return val 
def pumping(target_weight=100):
    weight = 0
    offset = 3
    hx.tare()
    while weight<target_weight-offset :
        try : 
            weight = measure()
            GPIO.output(CTL_PIN,1)
        except (KeyboardInterrupt, SystemExit):
            GPIO.output(CTL_PIN,0)
            cleanAndExit()

    GPIO.output(CTL_PIN,0)
        
def mycallback(channel):                                                 
    print("Button pressed @", time.ctime())

def main():
    KEY_PRESSED = True # make a function about it 
    previous_Status = None
    try: 
        amount= 100 # make a function about it 
        #input = GPIO.input(BOTTON_PIN)
        GPIO.add_event_detect(BOTTON_PIN, GPIO.FALLING, callback=mycallback, bouncetime=200)  #當檢測到有按鍵被按下時，回調led()函數
        while True :
            time.sleep(60)
        
        #previous_Status = input
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()


    
if __name__=='__main__':
    init()
    main()
    cleanAndExit()