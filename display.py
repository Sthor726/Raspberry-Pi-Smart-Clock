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

RST = 27
DC = 25
BL = 18
bus = 0
device = 0
logging.basicConfig(level=logging.DEBUG)

try:
    disp = LCD_2inch.LCD_2inch()
    disp.Init()
    disp.clear()

    image1 = Image.new("RGB", (disp.height, disp.width), "WHITE")
    draw = ImageDraw.Draw(image1)

    Font1 = ImageFont.truetype("Font/Font00.ttf", 18)
    Font2 = ImageFont.truetype("Font/Font01.ttf", 22)

    while True:
        events = clock.getCalendarEvents(5)
        draw.rectangle([(0, 0), (disp.height, disp.width)], fill="WHITE")

        if events:
            y_position = 10
            for i, event in enumerate(events[:2]):
                start_time = event["start"]
                summary = event["summary"]

                draw.text((10, y_position), f"Start: {start_time}", fill="BLACK", font=Font1)
                y_position += 25

                draw.text((10, y_position), summary, fill="BLACK", font=Font2)
                y_position += 40

                if i < 1:
                    draw.line([(10, y_position), (disp.height-10, y_position)], fill="BLACK", width=1)
                    y_position += 10

            if len(events) > 2:
                draw.text((10, y_position), "More events available...", fill="BLACK", font=Font1)

            disp.ShowImage(image1, 0, 0)
        else:
            logging.info("No upcoming events found.")
            draw.text((10, 20), "No upcoming events found.", fill="BLACK", font=Font2)
            disp.ShowImage(image1, 0, 0)

        time.sleep(5)

except IOError as e:
    logging.info(e)
except KeyboardInterrupt:
    disp.module.exit()
    logging.info("quit: ")
    exit()
