# Raspberry Pi Zero Smart Clock

## Overview
This project leverages a Raspberry Pi and a 2-inch LCD screen to create a display that shows upcoming events from my Google Calendar. The display shows the current time, the day of the week, and details about the next scheduled events, including its time, date, and title.


## Features
- **Hardware**: The project runs on a Raspberry Pi, utilizing the GPIO pins to interface with the 2-inch LCD screen.
- **Google Calendar Integration**: This application uses the google-auth and google-api-python-client libraries to authenticate
with the Google Calendar API and retrieve event data
- **Display Library**: The project uses the Waveshare LCD_2inch library to interface with the 2-inch display.
The PIL (Pillow) library is used to create and manage the images displayed on the screen
- **Casing**: The Raspberry Pi and LCD screen are housed in a 3d printed case, meant to resemble an old-fashioned TV.
## Project Images:

<p float="left">
  <img src="https://github.com/user-attachments/assets/8b152666-feb8-4e22-bd5b-d92a1ad29a7e" width="400" />
  <img src="https://github.com/user-attachments/assets/fe7e5a38-059d-4074-b55b-d7c8e96b5f87" width="400" />
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


##### .json files have been removed to hide API keys


