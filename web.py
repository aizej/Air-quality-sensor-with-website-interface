from flask import Flask, render_template, jsonify, request
import time
from datetime import datetime, timezone, timedelta

app = Flask(__name__)

@app.route('/')
def home():
    # Specify the number and word to be displayed

    with open("/home/pi/Desktop/CO2/myfile.txt", 'r') as file:
        last_line = None
        todays_data = []
        for line in file:
            last_line = line.strip()

            todays_data.append(line.strip())
            if len(todays_data) > 60*24:
                todays_data.pop(0)

        cas, ppm = last_line.split("*")

    number = float(ppm)
    if number < 600:
        word = "supr"
    elif number < 1000:
        word = "dobry"
    elif number < 1500:
        word = "OK"
    elif number < 2000:
        word = "Spatne"
    elif number < 5000:
        word = "Velmi Spatne"
    else:
        word = "Okamzite vyvetrat!"

    number = float(int(number))

    curr_time = time.strftime("%H:%M:%S")

    data_times = []
    data_values = []

    for line in todays_data:
        time_for_value, value = line.split("*")
        value = int(float(value))
        time_for_value = float(time_for_value)
        time_for_value = datetime.fromtimestamp(time_for_value, timezone(timedelta(hours=1)))
        time_for_value = time_for_value.strftime('%H:%M:%S')

        data_times.append(time_for_value)
        data_values.append(value)

        
        



    # Check if the request is an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Return JSON data for AJAX requests
        return jsonify(number=number, word=word, curr_time=curr_time, graph_labels=data_times, graph_values=data_values)
    else:
        # Render the HTML template for regular browser requests
        return render_template('index.html', number=number, word=word, curr_time=curr_time, graph_labels=data_times, graph_values=data_values)

if __name__ == '__main__':
    app.run(host='10.0.0.3', port=8000, debug=True)