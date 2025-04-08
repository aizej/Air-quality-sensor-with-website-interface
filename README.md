# Air-quality-sensor-with-website-interface
Project with Raspberry Pi using an SHT45 and MH-Z14 sensors to collect data about CO2, temperature and humidity levels in my room, using a web interface in the local network.


First, we need to gather the data:
With driver libraries for the sensors we can fetch the current values.

Then we just append it to our database (text file) with the current time
And do this every 60 seconds 

![obrazek](https://github.com/user-attachments/assets/ec7a8fa6-95d2-4d61-b519-aae429195c38)


Then in the stranka.py script, we get the last 24 hours of data + current time, remove outliers and prepare the data for graphing:

![web_script_obrazek](https://github.com/aizej/Air-quality-sensor-with-website-interface/assets/61479273/29d00d3b-f450-4969-8c63-aa542dfd73ae)



Finally, we can look at the results:


![Snímek obrazovky 2023-12-29 145214](https://github.com/aizej/Air-quality-sensor-with-website-interface/assets/61479273/8568bcdd-063d-422e-b770-95b7eeed9f30)


