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

    Font1 = ImageFont.truetype("Font/Font00.ttf", 24)
    Font2 = ImageFont.truetype("Font/Font00.ttf", 20)

    while True:
        now = datetime.now()
        current_time = now.strftime("%I:%M %p")
        day_of_week = now.strftime("%A")
        
        events = clock.getCalendarEvents(1)
        draw.rectangle([(0, 0), (disp.height, disp.width)], fill=BACKGROUND_COLOR)

        draw.text((10, 10), f"{current_time}", fill=TEXT_COLOR, font=Font1)
        draw.text((10, 30), f"{day_of_week}", fill=TEXT_COLOR, font=Font1)

        if events:
            next_event = events[0]
            event_start = next_event["start"]
            event_summary = next_event["summary"]

            # Ensure event_start is a datetime object, else try to parse it.
            if isinstance(event_start, str):
                try:
                    event_start = datetime.fromisoformat(event_start)  # Try to parse as ISO format
                except ValueError:
                    logging.error(f"Invalid event start format: {event_start}")
                    event_start = None

            if event_start:
                event_date = event_start.strftime("%m/%d")
                event_start_time = event_start.strftime("%I:%M %p")
                event_end_time = event_start + timedelta(hours=1)
                event_end_time_str = event_end_time.strftime("%I:%M %p")

                event_text = f"{event_date} {event_start_time} - {event_end_time_str}\n{event_summary}"
                
                draw.text((10, 70), "Next:", fill=TEXT_COLOR, font=Font2)
                draw.text((10, 100), event_text, fill=TEXT_COLOR, font=Font2)
            else:
                draw.text((10, 60), "Invalid event time", fill=TEXT_COLOR, font=Font2)
        
        else:
            draw.text((10, 60), "No upcoming events.", fill=TEXT_COLOR, font=Font2)

        disp.ShowImage(image1, 0, 0)
        time.sleep(5)

except IOError as e:
    logging.info(e)
except KeyboardInterrupt:
    disp.module.exit()
    logging.info("quit: ")
    exit()
