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

BACKGROUND_COLOR = (0, 0, 0)  
TEXT_COLOR = (0, 255, 0)  

try:
    disp = LCD_2inch.LCD_2inch()
    disp.Init()
    disp.clear()

    image1 = Image.new("RGB", (disp.height, disp.width), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(image1)

    FontLarge = ImageFont.truetype("/home/sthor726/Raspberry-Pi-Smart-Clock/Font/sysfont.otf", 40)
    FontMedium = ImageFont.truetype("/home/sthor726/Raspberry-Pi-Smart-Clock/Font/sysfont.otf", 30)
    FontSmall = ImageFont.truetype("/home/sthor726/Raspberry-Pi-Smart-Clock/Font/sysfont.otf", 24)

    while True:
        now = datetime.now()
        current_time = now.strftime("%I:%M %p")
        day_of_week = now.strftime("%A")
        
        events = clock.getCalendarEvents(2)
        draw.rectangle([(0, 0), (disp.height, disp.width)], fill=BACKGROUND_COLOR)

        draw.text((10, 10), current_time, fill=TEXT_COLOR, font=FontLarge)
        draw.text((10, 60), day_of_week, fill=TEXT_COLOR, font=FontLarge)

        y_offset = 120
        if events:
            for event in events[:2]:
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

                    event_text = f"{event_date} {event_start_time} - {event_end_time_str}"
                    draw.text((10, y_offset), event_text, fill=TEXT_COLOR, font=FontMedium)
                    draw.text((10, y_offset + 35), event_summary, fill=TEXT_COLOR, font=FontSmall)
                    y_offset += 80
                
                else:
                    draw.text((10, y_offset), "Invalid event time", fill=TEXT_COLOR, font=FontMedium)
                    y_offset += 50
        else:
            draw.text((10, y_offset), "No upcoming events.", fill=TEXT_COLOR, font=FontMedium)

        disp.ShowImage(image1, 0, 0)
        time.sleep(5)

except IOError as e:
    logging.info(e)
except KeyboardInterrupt:
    disp.module.exit()
    logging.info("quit: ")
    exit()
