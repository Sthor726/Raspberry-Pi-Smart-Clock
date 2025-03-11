#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
import time
import logging
import spidev as SPI
from PIL import Image, ImageDraw, ImageFont
from lib import LCD_2inch
import clock
from datetime import datetime, timedelta

RST = 27
DC = 25
BL = 18
bus = 0
device = 0
logging.basicConfig(level=logging.DEBUG)

BACKGROUND_COLOR = (166, 166, 154)  
TEXT_COLOR = (0, 0, 0)  

try:
    disp = LCD_2inch.LCD_2inch()
    disp.Init()
    disp.clear()

    background = Image.open("wii-menu.png").convert("RGB")
    background = background.resize((disp.height, disp.width))

    Font1 = ImageFont.truetype("/home/sthor726/Raspberry-Pi-Smart-Clock/Font/sysfont.otf", 24)

    while True:
        now = datetime.now()
        current_time = now.strftime("%I:%M %p")
        day_of_week = now.strftime("%A")
        
        events = clock.getCalendarEvents(2)
        image1 = background.copy()
        draw = ImageDraw.Draw(image1)

        draw.text((10, 10), f"{current_time}", fill=TEXT_COLOR, font=Font1)
        draw.text((10, 30), f"{day_of_week}", fill=TEXT_COLOR, font=Font1)

        if events:
            y_offset = 100
            for i, event in enumerate(events[:2]):
                event_start = event["start"]
                event_summary = event["summary"]

                if isinstance(event_start, str):
                    try:
                        event_start = datetime.fromisoformat(event_start)
                    except ValueError:
                        logging.error(f"Invalid event start format: {event_start}")
                        event_start = None

                if event_start:
                    event_date = event_start.strftime("%m/%d")
                    event_start_time = event_start.strftime("%I:%M %p")
                    event_end_time = event_start + timedelta(hours=1)
                    event_end_time_str = event_end_time.strftime("%I:%M %p")

                    event_text = f"{event_date} {event_start_time} - {event_end_time_str} \n {event_summary}"
                    draw.text((10, y_offset), event_text, fill=TEXT_COLOR, font=Font1)
                    y_offset += 70
                
                else:
                    draw.text((10, y_offset), "Invalid event time", fill=TEXT_COLOR, font=Font1)
                    y_offset += 70

        else:
            draw.text((10, 60), "No upcoming events.", fill=TEXT_COLOR, font=Font1)

        disp.ShowImage(image1, 0, 0)
        time.sleep(5)

except IOError as e:
    logging.info(e)
except KeyboardInterrupt:
    disp.module.exit()
    logging.info("quit: ")
    exit()
