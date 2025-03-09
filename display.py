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

# Color definitions
BACKGROUND_COLOR = (0, 0, 0)  # Black background
TEXT_COLOR = (0, 255, 0)  # Green text

try:
    disp = LCD_2inch.LCD_2inch()
    disp.Init()
    disp.clear()

    image1 = Image.new("RGB", (disp.height, disp.width), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(image1)

    Font1 = ImageFont.truetype("Font/Font00.ttf", 18)
    Font2 = ImageFont.truetype("Font/Font01.ttf", 22)

    while True:
        now = datetime.now()
        current_time = now.strftime("%I:%M %p")
        day_of_week = now.strftime("%A")
        
        events = clock.getCalendarEvents(1)
        draw.rectangle([(0, 0), (disp.height, disp.width)], fill=BACKGROUND_COLOR)

        draw.text((10, 10), f"Time: {current_time}", fill=TEXT_COLOR, font=Font2)
        draw.text((10, 30), f"Day: {day_of_week}", fill=TEXT_COLOR, font=Font2)

        if events:
            next_event = events[0]
            event_start = next_event["start"]
            event_summary = next_event["summary"]

            event_date = event_start.strftime("%m/%d")
            event_start_time = event_start.strftime("%I:%M %p")
            event_end_time = event_start + timedelta(hours=1)
            event_end_time_str = event_end_time.strftime("%I:%M %p")

            event_text = f"{event_date} {event_start_time}-{event_end_time_str}\n\"{event_summary}\""
            draw.text((10, 60), event_text, fill=TEXT_COLOR, font=Font2)
        
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
