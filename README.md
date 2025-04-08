# Air-quality-sensor-with-website-interface
Project with Raspberry Pi using an SHT45 and MH-Z14 sensors to collect data about CO2, temperature and humidity levels in my room, using a web interface in the local network.


First, we need to gather the data:
With driver libraries for our sensors that comunicate with I2C to aou raspberri pi.

We just append it to our database (text file) with the current time
And do this every 60 seconds 

![main_obrazek](https://github.com/aizej/Air-quality-sensor-with-website-interface/assets/61479273/76953b42-b060-4096-9af8-2af1c7ddc10b)

Then in the web.py script, we get the last 24 hours of data + current time and pass it to html-javascript

![web_script_obrazek](https://github.com/aizej/Air-quality-sensor-with-website-interface/assets/61479273/29d00d3b-f450-4969-8c63-aa542dfd73ae)



Finally, we can look at the results:


![Snímek obrazovky 2023-12-29 145214](https://github.com/aizej/Air-quality-sensor-with-website-interface/assets/61479273/8568bcdd-063d-422e-b770-95b7eeed9f30)


