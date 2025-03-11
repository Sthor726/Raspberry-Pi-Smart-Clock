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
TITLE_COLOR = (140, 140, 140)  
TEXT_COLOR = (20, 20, 20)

try:
    disp = LCD_2inch.LCD_2inch()
    disp.Init()
    disp.clear()

    background = Image.open("/home/sthor726/Raspberry-Pi-Smart-Clock/wii-menu.png").convert("RGB")
    background = background.resize((disp.height, disp.width))

    Font1 = ImageFont.truetype("/home/sthor726/Raspberry-Pi-Smart-Clock/Font/sysfont.otf", 24)
    FontLarge = ImageFont.truetype("/home/sthor726/Raspberry-Pi-Smart-Clock/Font/contm.ttf", 32)

    while True:
        now = datetime.now()
        current_time = now.strftime("%I:%M %p")
        day_of_week = now.strftime("%A")
        
        events = clock.getCalendarEvents(2)
        image1 = background.copy()
        draw = ImageDraw.Draw(image1)

        disp_width, disp_height = disp.height, disp.width  # LCD is rotated, so height is width

        time_bbox = FontLarge.getbbox(current_time)
        day_bbox = FontLarge.getbbox(day_of_week)

        time_text_width = time_bbox[2] - time_bbox[0]
        day_text_width = day_bbox[2] - day_bbox[0]

        time_x = (disp_width - time_text_width) // 2
        day_x = (disp_width - day_text_width) // 2

        draw.text((time_x, 10), current_time, fill=TITLE_COLOR, font=FontLarge)
        draw.text((day_x, 40), day_of_week, fill=TITLE_COLOR, font=FontLarge)


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
                    y_offset += 50
                    
                    if i < len(events) - 1:
                        draw.line((10, y_offset, disp_width - 10, y_offset), fill=TITLE_COLOR, width=2)
                        y_offset += 10
                else:
                    draw.text((10, y_offset), "Invalid event time", fill=TEXT_COLOR, font=Font1)
                    y_offset += 50

        else:
            draw.text((10, 60), "No upcoming events.", fill=TEXT_COLOR, font=Font1)

        disp.ShowImage(image1, 0, 0)
        time.sleep(5)

except IOError as e:
    disp.clear()
    logging.info(e)
except KeyboardInterrupt:
    disp.clear()
    disp.module.exit()
    logging.info("quit: ")
    exit()
