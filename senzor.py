#!/usr/bin/env python3.11
import pandas as pd
import time
from SHT45 import get_avg_of_k_measurements
from CO2_laser_sensor import PPM,GPIO_setup
from datetime import datetime
import pickle
try:
    from zoneinfo import ZoneInfo  # Works in Python 3.9+
except ImportError:
    from backports.zoneinfo import ZoneInfo  # Use backport for Python 3.7


GPIO_setup()

pickle_file = "cached.pickle"


cache_for_web_unprocessed = pd.DataFrame({
    'time':     pd.Series(dtype='str'),
    'PPM':      pd.Series(dtype='int64'),
    'humidity': pd.Series(dtype='float64'),
    'temp':     pd.Series(dtype='float64')
})

humidity = 65
temperature = 22



timer_start = time.time()

while True:
    s = time.time()
    
    result = get_avg_of_k_measurements(100)
    if result != None:
        humidity = result[1]
        temperature = result[0]
    
    
    PP = int(PPM())
    

    with open("myfile.txt", 'a') as file1:
        file1.write(f"\n{time.time()},{PP},{humidity},{temperature}")
    


    cache_time = time.time()

    smoothing_window = 10

    #use this for oldeer pandas #cache_for_web_unprocessed = cache_for_web_unprocessed.append({'time': datetime.fromtimestamp(time.time(), ZoneInfo('Europe/Prague')).strftime('%H:%M:%S'), 'PPM': PP, 'humidity': humidity, 'temp': temperature}, ignore_index=True)
    cache_for_web_unprocessed.loc[len(cache_for_web_unprocessed)] = {
        'time': datetime.fromtimestamp(time.time(), ZoneInfo('Europe/Prague')).strftime('%H:%M:%S'),
        'PPM': PP,
        'humidity': humidity,
        'temp': temperature
    }
    cache_for_web_unprocessed = cache_for_web_unprocessed.tail(60*24)

    cache_for_web = cache_for_web_unprocessed.copy()

    if(len(cache_for_web_unprocessed.index) > smoothing_window):
        # does not preserve the actual data and last window/2 values are None
        cache_for_web["PPM_removed_outliers"] = cache_for_web["PPM"].rolling(window=smoothing_window, center=True).median()
        cache_for_web["temp_removed_outliers"] = cache_for_web["temp"].rolling(window=smoothing_window, center=True).median()
        cache_for_web["humidity_removed_outliers"] = cache_for_web["humidity"].rolling(window=smoothing_window, center=True).median()
        #get rid of the None by filling them with the original data
        cache_for_web["PPM"] = cache_for_web["PPM_removed_outliers"].fillna(cache_for_web["PPM"])
        cache_for_web["temp"] = cache_for_web["temp_removed_outliers"].fillna(cache_for_web["temp"])
        cache_for_web["humidity"] = cache_for_web["humidity_removed_outliers"].fillna(cache_for_web["humidity"])


    cache_for_web['PPM_normalised'] = (cache_for_web['PPM'] - cache_for_web['PPM'].min()) / (cache_for_web['PPM'].max() - cache_for_web['PPM'].min())
    cache_for_web['temp_normalised'] = (cache_for_web['temp'] - cache_for_web['temp'].min()) / (cache_for_web['temp'].max() - cache_for_web['temp'].min())
    cache_for_web['humidity_normalised'] = (cache_for_web['humidity'] - cache_for_web['humidity'].min()) / (cache_for_web['humidity'].max() - cache_for_web['humidity'].min())

    cashe_graph_labels = cache_for_web['time'].tolist()
    cashe_graph_values_CO2=[int(x) for x in cache_for_web["PPM"].tolist()]
    cashe_graph_values_Temperature=[float(x) for x in cache_for_web["temp"].tolist()]
    cashe_graph_values_Humidity=[float(x) for x in cache_for_web["humidity"].tolist()]
    cashe_graph_values_Combined_CO2=[float(x) for x in cache_for_web["PPM_normalised"].tolist()]
    cashe_graph_values_Combined_Temperature=[float(x) for x in cache_for_web["temp_normalised"].tolist()]
    cashe_graph_values_Combined_Humidity=[float(x) for x in cache_for_web["humidity_normalised"].tolist()]

    chache_ALL_to_pickle = [cashe_graph_labels,cashe_graph_values_CO2,cashe_graph_values_Temperature,cashe_graph_values_Humidity,cashe_graph_values_Combined_CO2,cashe_graph_values_Combined_Temperature,cashe_graph_values_Combined_Humidity]
    with open(pickle_file, 'wb') as f:
        pickle.dump(chache_ALL_to_pickle, f)


    print(f"{PP} {humidity} {temperature} {len(cache_for_web_unprocessed.index)} {round(cache_time-s,2)} total: {round(time.time()-s,2)}s")
    time.sleep(60-(time.time()-s)-1) #antibusy wait
    while time.time()-timer_start < 60:
        pass
    timer_start = time.time()
