import time 
import numpy as np
from flask import Flask, render_template, jsonify, request
import pandas as pd


app = Flask(__name__)

splitting_token = ","





def get_data():
    file_path = "/home/pi/Desktop/CO2/cached.pickle"
    return pd.read_pickle(file_path)
    




@app.route('/')
def home():
    # Specify the number and word to be displayed
    start = time.time()
    
    cashe_graph_labels,cashe_graph_values_CO2,cashe_graph_values_Temperature,cashe_graph_values_Humidity,cashe_graph_values_Combined_CO2,cashe_graph_values_Combined_Temperature,cashe_graph_values_Combined_Humidity = get_data()
    
    curr_time = time.strftime("%H:%M:%S")

    curr_PPM = cashe_graph_values_CO2[-1]
    curr_humidity = round(cashe_graph_values_Humidity[-1],2)
    curr_temp = round(cashe_graph_values_Temperature[-1],2)
    

    check_data = time.time()

    


    trend_data = cashe_graph_values_CO2["PPM"][-60:]
    trend_data_len = len(trend_data)
    trend, _ = np.polyfit(range(trend_data_len),trend_data, 1)
    trend = int(trend*trend_data_len)

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




    print(f"Time taken: {round(check_data-start,2)} {round(time.time()-check_data,2)}  total: {round(time.time()-start,2)} s")
    # Check if the request is an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Return JSON data for AJAX requests
        return jsonify(CO2_PPM_number=curr_PPM,
                        Temperature_number=curr_temp,
                        Humidity_number=curr_humidity,
                        word=word,
                        curr_time=curr_time,
                        trend=trend,
                        graph_labels=cashe_graph_labels,
                        graph_values_CO2=cashe_graph_values_CO2,
                        graph_values_Temperature=cashe_graph_values_Temperature,
                        graph_values_Humidity=cashe_graph_values_Humidity,
                        graph_values_Combined_CO2=cashe_graph_values_Combined_CO2,
                        graph_values_Combined_Temperature=cashe_graph_values_Combined_Temperature,
                        graph_values_Combined_Humidity=cashe_graph_values_Combined_Humidity)
    else:
        # Render the HTML template for regular browser requests
        return render_template('index.html',
                                CO2_PPM_number=curr_PPM,
                        Temperature_number=curr_temp,
                        Humidity_number=curr_humidity,
                        word=word,
                        curr_time=curr_time,
                        trend=trend,
                        graph_labels=cashe_graph_labels,
                        graph_values_CO2=cashe_graph_values_CO2,
                        graph_values_Temperature=cashe_graph_values_Temperature,
                        graph_values_Humidity=cashe_graph_values_Humidity,
                        graph_values_Combined_CO2=cashe_graph_values_Combined_CO2,
                        graph_values_Combined_Temperature=cashe_graph_values_Combined_Temperature,
                        graph_values_Combined_Humidity=cashe_graph_values_Combined_Humidity)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)