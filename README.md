# Raspberry Pi Zero Smart Clock

## Overview
This project leverages a Raspberry Pi and a 2-inch LCD screen to create a display that shows upcoming events from my Google Calendar. The display shows the current time, the day of the week, and details about the next scheduled event, including its time, date, and title.


## Features
- **Hardware**: The project runs on a Raspberry Pi, utilizing the GPIO pins to interface with the 2-inch LCD screen.
- **Google Calendar Integration**: This application uses the google-auth and google-api-python-client libraries to authenticate
with the Google Calendar API and retrieve event data
- **Display Library**: The project uses the Waveshare LCD_2inch library to interface with the 2-inch display.
The PIL (Pillow) library is used to create and manage the images displayed on the screen
