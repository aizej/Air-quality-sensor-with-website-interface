import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import time
from senzor import Co2_sensor
from DHT_22 import DHT_22


# Initialize the I2C interface
i2c = busio.I2C(board.SCL, board.SDA)

# Create an ADS1115 object
ads = ADS.ADS1115(i2c)

# Define the analog input channel
channel = AnalogIn(ads, ADS.P0)



# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!
humiduty = 65
temperature = 22

while True:
    new_h,new_t = DHT_22()
    if new_h != None:
        humiduty = new_h
    if new_t != None:
        temperature = new_t

    PP = Co2_sensor(humiduty, temperature, channel.value)[1]

    print(PP,new_h,new_t)

    with open("/home/pi/Desktop/CO2/myfile.txt", 'a') as file1:
        file1.write(f"\n{time.time()}*{PP}")

    time.sleep(60)