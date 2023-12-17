# Air-quality-sensor-with-website-interface
Project with Raspberry Pi using an MQ-135 sensor to collect data about CO2 levels in my room, using a web interface in the local network.


First, we need to gather the data:
With a slightly modified driver for ads1115 and MQ-135 from 
https://github.com/danielcshn/MQ135-ADS1115-Python which is inspired by https://github.com/GeorgK/MQ135

We take the data from our analog to digital converter and pass it to the driver
After that, we just append it to our database (text file) with the current time
And do this every 60 seconds 

![main_obrazek](https://github.com/aizej/Air-quality-sensor-with-website-interface/assets/61479273/76953b42-b060-4096-9af8-2af1c7ddc10b)

Then in the web.py script, we get the last 24 hours of data + current time and pass it to html-javascript

![web_script_obrazek](https://github.com/aizej/Air-quality-sensor-with-website-interface/assets/61479273/29d00d3b-f450-4969-8c63-aa542dfd73ae)



Finally, we can look at  the result:


![stranka_obrazek](https://github.com/aizej/Air-quality-sensor-with-website-interface/assets/61479273/038067c2-9242-4ad3-9822-aeafd1d55855)

