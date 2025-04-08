#!/usr/bin/env python3.11
import board
import busio
import time
import RPi.GPIO as GPIO
from SHT45 import get_avg_of_k_measurements
from CO2_laser_sensor import PPM,GPIO_setup



GPIO_setup()


humiduty = 65
temperature = 22
last_PP = 422


timer_start = time.time()

while True:
    s = time.time()
    
    result = get_avg_of_k_measurements(100)
    if result != None:
        humiduty = result[1]
        temperature = result[0]
    
    
    PP = int(PPM())
    

    with open("/home/pi/Desktop/CO2/myfile.txt", 'a') as file1:
        file1.write(f"\n{time.time()},{PP},{humiduty},{temperature}")
    
    print(PP,humiduty,temperature,time.time()-s)

    while time.time()-timer_start < 60:
        pass
    timer_start = time.time()

