# Air-quality-sensor-with-website-interface
Project with Raspberry Pi using an SHT45 and MH-Z14 sensors to collect data about CO2, temperature and humidity levels in my room, using a web interface in the local network.


First, we need to gather the data:
With driver libraries for the sensors we can fetch the current values.

Then we just append it to our database (text file) with the current time
And do this every 60 seconds 

![obrazek](https://github.com/user-attachments/assets/ec7a8fa6-95d2-4d61-b519-aae429195c38)


Then in the stranka.py script, we get the last 24 hours of data + current time, remove outliers and prepare the data for graphing:

![Snímek obrazovky 2025-04-08 114439](https://github.com/user-attachments/assets/26106d7d-5c50-490f-a4a8-220635f9f53a)


Finally, we can look at the results:
![Snímek obrazovky 2025-04-08 114557](https://github.com/user-attachments/assets/17390775-3493-4a28-8524-fe4fd9157f4c)
![Snímek obrazovky 2025-04-08 114623](https://github.com/user-attachments/assets/06e92e10-09c1-4d91-987b-601e81555593)
![Snímek obrazovky 2025-04-08 114640](https://github.com/user-attachments/assets/b8a80f95-b57e-4bc3-a62b-2570403bbc00)
![Snímek obrazovky 2025-04-08 114723](https://github.com/user-attachments/assets/acf3b842-f998-42b4-a9ae-ff5849dd2838)
