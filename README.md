# Raspberry Pi Zero Smart Clock

## Overview
This project leverages a Raspberry Pi and a 2-inch LCD screen to create a display that shows upcoming events from my Google Calendar. The display shows the current time and date, information about scheduled events on my Google Calendar, and the daily weather forecast.


## Features
- **Hardware**: The project runs on a Raspberry Pi, utilizing the GPIO pins to interface with the 2-inch LCD screen.
- **Screens**: The Raspberry Pi alternates between 3 different screens: time/date, calendar, and weather. A swipe animation is created to allow for a seamless transition between screens.
- **Google Calendar Integration**: This application uses the google-auth and google-api-python-client libraries to authenticate
with the Google Calendar API and retrieve event data.
- **Weather Integration**: This application uses the WeatherBit API to display the current day's forecast.
- **Display Library**: The project uses the Waveshare LCD_2inch library to interface with the 2-inch display.
The PIL (Pillow) library is used to create and manage the images displayed on the screen.
- **Casing**: The project uses a custom casing 3D modeled for the Raspberry Pi and LCD screen using Blender.
## Project Images:

<p float="left">
  <img src="https://github.com/user-attachments/assets/7aae32e6-3d72-4237-9f06-f1dd57116d71" width="300" />
  <img src="https://github.com/user-attachments/assets/fa5bc933-ab4d-4384-b2f1-f6b17efca043" width="300" />
  <img src="https://github.com/user-attachments/assets/aeacf704-b9d9-478d-9ac3-55b5aa7fcae3" width="300" />

  <img src="https://github.com/user-attachments/assets/fe7e5a38-059d-4074-b55b-d7c8e96b5f87" width="200" />
</p>

## Implementation  

On boot, the Raspberry Pi executes the following commands from `rc.local` to activate the virtual environment and start the display script:  

```bash
source /home/<username>/venv/bin/activate  
python3 /home/<username>/Raspberry-Pi-Smart-Clock/display.py &
```

</br>
</br>
</br>




