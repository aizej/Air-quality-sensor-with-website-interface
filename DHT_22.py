import Adafruit_DHT

sensor = Adafruit_DHT.DHT22

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!
def DHT_22():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, '4')

    return humidity,temperature
    
