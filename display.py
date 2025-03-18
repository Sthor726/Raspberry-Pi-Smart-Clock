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
    
    crt_filter = Image.open("/home/sthor726/Raspberry-Pi-Smart-Clock/filter.png").convert("RGBA")
    crt_filter = crt_filter.resize((disp.height, disp.width))

    Font1 = ImageFont.truetype("/home/sthor726/Raspberry-Pi-Smart-Clock/Font/sysfont.otf", 24)
    FontLarge = ImageFont.truetype("/home/sthor726/Raspberry-Pi-Smart-Clock/Font/contm.ttf", 32)
    FontMedium = ImageFont.truetype("/home/sthor726/Raspberry-Pi-Smart-Clock/Font/contm.ttf", 28)

    while True:
        # State 1: Display greeting and date / time
        now = datetime.now()
        current_time = now.strftime("%I:%M %p")
        current_hour = int(now.strftime("%H"))  # Get the hour in 24-hour format
        
        day_of_week = now.strftime("%A")
        today_date = now.strftime("%B %d")
        
        events = clock.getCalendarEvents(2)
        image1 = background.copy()
        draw = ImageDraw.Draw(image1)

        disp_width, disp_height = disp.height, disp.width  # LCD is rotated, so height is width

        time_bbox = FontMedium.getbbox(current_time)
        date_bbox = FontMedium.getbbox(today_date)
        day_bbox = FontLarge.getbbox(day_of_week)
        greeting_bbox = FontLarge.getbbox("Good Morning!")

        time_text_width = time_bbox[2] - time_bbox[0]
        day_text_width = day_bbox[2] + date_bbox[2] - (day_bbox[0] + date_bbox[0])
        greeting_text_width = greeting_bbox[2] - greeting_bbox[0]
        
        greeting_x = (disp_width - greeting_text_width) // 2
        time_x = (disp_width - time_text_width) // 2
        day_x = (disp_width - day_text_width) // 2
        
        if current_hour < 12:
            greeting = "Good Morning!"
        elif current_hour < 18:
            greeting = "Good Afternoon!"
        else:
            greeting = "Good Evening!"
            
        draw.text((greeting_x, 20), greeting, fill=TITLE_COLOR, font=FontLarge)
        draw.text((day_x, 100), day_of_week + ", " + today_date, fill=TITLE_COLOR, font=FontMedium)
        draw.text((time_x, 130), current_time, fill=TITLE_COLOR, font=FontLarge)
        
        image1.paste(crt_filter, (0, 0), crt_filter)
        disp.ShowImage(image1, 0, 0)
        
        time.sleep(10)
        
        # Swipe transition text off screen
        for offset in range(0, disp_width + 1, 3):  # Increment by 10 pixels per frame
            image1 = background.copy()
            draw = ImageDraw.Draw(image1)

            # Move text to the left by decreasing x-coordinates
            draw.text((greeting_x - offset, 20), greeting, fill=TITLE_COLOR, font=FontLarge)
            draw.text((day_x - offset, 100), day_of_week + ", " + today_date, fill=TITLE_COLOR, font=FontMedium)
            draw.text((time_x - offset, 130), current_time, fill=TITLE_COLOR, font=FontLarge)

            # Display the updated image
            image1.paste(crt_filter, (0, 0), crt_filter)
            disp.ShowImage(image1, 0, 0)
            time.sleep(0.01)  # Adjust speed of animation

        # Clear the screen after the animation
        disp.clear()

        # State 2: Display upcoming events
        text_bbox = FontLarge.getbbox("Upcoming Events")
        text_width = text_bbox[2] - text_bbox[0]
        text_x = (disp_width - text_width) // 2
        draw.text((text_x, 20), "Upcoming Events", fill=TITLE_COLOR, font=FontLarge)
        
        if events:
            y_offset = 100  # Reset y_offset before the loop
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

                    event_text = f"{event_date} {event_start_time} \n {event_summary}"
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
            
        image1.paste(crt_filter, (0, 0), crt_filter)
        disp.ShowImage(image1, 0, 0)
        
        time.sleep(10)
        
        # Swipe transition text off screen
        for offset in range(0, disp_width + 1, 3):
            y_offset = 100 
            image1 = background.copy()
            draw = ImageDraw.Draw(image1)

            draw.text((text_x - offset, 20), "Upcoming Events", fill=TITLE_COLOR, font=FontLarge)
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

                    event_text = f"{event_date} {event_start_time} \n {event_summary}"
                    draw.text((10 - offset, y_offset), event_text, fill=TEXT_COLOR, font=Font1)
                    y_offset += 50

                    if i < len(events) - 1:
                        draw.line((10 - offset, y_offset, disp_width - 10, y_offset), fill=TITLE_COLOR, width=2)
                        y_offset += 10
                else:
                    draw.text((10 - offset, y_offset), "Invalid event time", fill=TEXT_COLOR, font=Font1)
                    y_offset += 50

            image1.paste(crt_filter, (0, 0), crt_filter)
            disp.ShowImage(image1, 0, 0)
            time.sleep(0.01)

except IOError as e:
    if 'disp' in locals():
        disp.clear()
    logging.info(e)
except KeyboardInterrupt:
    if 'disp' in locals():
        disp.clear()
        disp.module.exit()
    logging.info("quit: ")
    exit()
