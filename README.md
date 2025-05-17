# Air-quality-sensor-with-website-interface
http://158.101.167.252:8000/

Project with Raspberry Pi using an SHT45 and MH-Z14 sensors to collect data about CO2, temperature and humidity levels in my room, using a web interface for visualization.


First, we need to gather the data:
With driver libraries for the sensors we can fetch the current values.

Then we just append it to our database (text file) with the current time
And do this every 60 seconds.
While appending the files to our main database we also prepare and store the last 1440 mesured values for fast retrieval by the stranka.py file.

Finally, we can look at the results:
![Snímek obrazovky 2025-04-08 114557](https://github.com/user-attachments/assets/17390775-3493-4a28-8524-fe4fd9157f4c)
![Snímek obrazovky 2025-04-08 114623](https://github.com/user-attachments/assets/06e92e10-09c1-4d91-987b-601e81555593)
![Snímek obrazovky 2025-04-08 114640](https://github.com/user-attachments/assets/b8a80f95-b57e-4bc3-a62b-2570403bbc00)
![Snímek obrazovky 2025-04-08 114723](https://github.com/user-attachments/assets/acf3b842-f998-42b4-a9ae-ff5849dd2838)
