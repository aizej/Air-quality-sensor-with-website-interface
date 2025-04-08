import time 
import numpy as np
from flask import Flask, render_template, jsonify, request
from datetime import datetime, timezone, timedelta
import pandas as pd
import subprocess
from collections import deque
try:
    from zoneinfo import ZoneInfo  # Works in Python 3.9+
except ImportError:
    from backports.zoneinfo import ZoneInfo  # Use backport for Python 3.7

app = Flask(__name__)

splitting_token = ","





def get_data(number_of_points=60*24+1):
    file_path = "/home/pi/Desktop/CO2/myfile.txt"
    

    # Use system tail command (works on Linux/Mac, Windows needs alternative)
    cmd = f"tail -n {number_of_points} {file_path}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    # Read the output into DataFrame
    df = pd.read_csv(pd.compat.StringIO(result.stdout))
    df.columns = ['time', 'PPM', 'humidity', 'temp']
    df = df.dropna()
    return df


def get_data_deque(number_of_points=60*24):
    file_path = "/home/pi/Desktop/CO2/myfile.txt"
    

    with open(file_path, 'r') as f:
        last_lines = deque(f, maxlen=number_of_points)
        
        # Convert to DataFrame
    df = pd.DataFrame([line.strip().split(',') for line in last_lines], columns=['time', 'PPM', 'temp', 'humidity'])

    # Convert columns to numeric (handling potential NaN values)
    numeric_cols = ['PPM', 'temp', 'humidity']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    
    # Convert timestamp column
    df['time'] = pd.to_numeric(df['time'], errors='coerce')
    
    # Drop any rows with NaN values (optional)
    return df


@app.route('/')
def home():
    # Specify the number and word to be displayed
    start = time.time()
    
    todays_data = get_data()
    
    curr_time = time.strftime("%H:%M:%S")

    curr_PPM = int(todays_data["PPM"].iloc[-1])
    curr_humidity = round(float(todays_data["humidity"].iloc[-1]),2)
    curr_temp = round(float(todays_data["temp"].iloc[-1]),2)
    

    check_data = time.time()

    # Convert timestamp to time string
    todays_data["time"] = todays_data["time"].apply(
        lambda x: datetime.fromtimestamp(x, ZoneInfo('Europe/Prague')).strftime('%H:%M:%S')
    )

    todays_data["temp"].round(2)
    todays_data["humidity"].round(2)


    trend_data = todays_data["PPM"][-60:]
    trend, _ = np.polyfit(range(len(trend_data)),trend_data, 1)
    trend = int(trend*len(trend_data))

    if curr_PPM < 600:
        word = "supr"
    elif curr_PPM < 1000:
        word = "dobry"
    elif curr_PPM < 1500:
        word = "OK"
    elif curr_PPM < 2500:
        word = "Špatné"
    elif curr_PPM < 3500:
        word = "Velmi Špatné"
    else:
        word = "Okamžitě vyvětrat!"




    rem_out = time.time()
    
    # does not preserve the actual data and last window/2 values are None
    todays_data["PPM_removed_outliers"] = todays_data["PPM"].rolling(window=10, center=True).median()
    todays_data["temp_removed_outliers"] = todays_data["temp"].rolling(window=10, center=True).median()
    todays_data["humidity_removed_outliers"] = todays_data["humidity"].rolling(window=10, center=True).median()
    #get rid of the None by filling them with the original data
    todays_data["PPM"] = todays_data["PPM_removed_outliers"].fillna(todays_data["PPM"])
    todays_data["temp"] = todays_data["temp_removed_outliers"].fillna(todays_data["temp"])
    todays_data["humidity"] = todays_data["humidity_removed_outliers"].fillna(todays_data["humidity"])
    

    norm = time.time()

    todays_data['PPM_normalised'] = (todays_data['PPM'] - todays_data['PPM'].min()) / (todays_data['PPM'].max() - todays_data['PPM'].min())
    todays_data['temp_normalised'] = (todays_data['temp'] - todays_data['temp'].min()) / (todays_data['temp'].max() - todays_data['temp'].min())
    todays_data['humidity_normalised'] = (todays_data['humidity'] - todays_data['humidity'].min()) / (todays_data['humidity'].max() - todays_data['humidity'].min())



    print(f"Time taken: {check_data-start} {rem_out-check_data}  {norm-rem_out} {time.time()-norm}seconds")
    # Check if the request is an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Return JSON data for AJAX requests
        return jsonify(CO2_PPM_number=curr_PPM,
                        Temperature_number=curr_temp,
                        Humidity_number=curr_humidity,
                        word=word,
                        curr_time=curr_time,
                        trend=trend,
                        graph_labels=todays_data["time"].tolist(),
                        graph_values_CO2=[int(x) for x in todays_data["PPM"].tolist()],
                        graph_values_Temperature=[float(x) for x in todays_data["temp"].tolist()],
                        graph_values_Humidity=[float(x) for x in todays_data["humidity"].tolist()],
                        graph_values_Combined_CO2=[float(x) for x in todays_data["PPM_normalised"].tolist()],
                        graph_values_Combined_Temperature=[float(x) for x in todays_data["temp_normalised"].tolist()],
                        graph_values_Combined_Humidity=[float(x) for x in todays_data["humidity_normalised"].tolist()])
    else:
        # Render the HTML template for regular browser requests
        return render_template('index.html',
                                CO2_PPM_number=curr_PPM,
                        Temperature_number=curr_temp,
                        Humidity_number=curr_humidity,
                        word=word,
                        curr_time=curr_time,
                        trend=trend,
                        graph_labels=todays_data["time"].tolist(),
                        graph_values_CO2=[int(x) for x in todays_data["PPM"].tolist()],
                        graph_values_Temperature=[float(x) for x in todays_data["temp"].tolist()],
                        graph_values_Humidity=[float(x) for x in todays_data["humidity"].tolist()],
                        graph_values_Combined_CO2=[float(x) for x in todays_data["PPM_normalised"].tolist()],
                        graph_values_Combined_Temperature=[float(x) for x in todays_data["temp_normalised"].tolist()],
                        graph_values_Combined_Humidity=[float(x) for x in todays_data["humidity_normalised"].tolist()])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)