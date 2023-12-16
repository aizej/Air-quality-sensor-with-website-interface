import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import time
from senzor import Co2_sensor

# Initialize the I2C interface
i2c = busio.I2C(board.SCL, board.SDA)

# Create an ADS1115 object
ads = ADS.ADS1115(i2c)

# Define the analog input channel
channel = AnalogIn(ads, ADS.P0)

while True:
    time.sleep(60)
    PP = Co2_sensor(channel.value)[1]
    print((0,PP))
    with open("/home/pi/Desktop/CO2/myfile.txt", 'a') as file1:
        file1.write(f"\n{time.time()}*{PP}")
