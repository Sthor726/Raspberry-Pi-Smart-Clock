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
import requests
import json
from datetime import datetime, timedelta
import io
from cairosvg import svg2png

RST = 27
DC = 25
BL = 18
bus = 0
device = 0
logging.basicConfig(level=logging.DEBUG)

WEATHER_API_KEY = '/home/sthor726/Raspberry-Pi-Smart-Clock/weather_key.json'
BACKGROUND_COLOR = (166, 166, 154)  
TITLE_COLOR = (140, 140, 140)  
TEXT_COLOR = (20, 20, 20)
ORANGE = (80, 20, 0)
BLUE = (0, 20, 80)


def get_event_text(list_events):
    event_details = [["" for _ in range(3)] for _ in range(2)]

    if list_events:
        for i, event in enumerate(list_events[:2]):
            event_start = event["start"]
            
            summary = event["summary"]
            summary_bbox = FontLarge.getbbox(summary)
            summary_text_width = summary_bbox[2] - summary_bbox[0]
            #text is too large for screen width
            if(summary_text_width > disp_width - 20):
                #truncate text and add '...' after
                summary = summary[:int((disp_width - 20) / 12)] + "..."
            
            event_details[i][2] = summary

            try:
                event_start = datetime.fromisoformat(event_start)
                event_details[i][0] = event_start.strftime("%m/%d")
                event_details[i][1] = event_start.strftime("%I:%M %p")
            except ValueError:
                logging.error(f"Invalid event start format: {event_start}")
                event_details[i][0] = "Invalid"
                event_details[i][1] = "Time"
    return event_details

def get_daily_forecast():
    key = json.load(open(WEATHER_API_KEY))["key"]
    url = f"https://api.weatherbit.io/v2.0/forecast/daily?city=Minneapolis,MN&units=I&days=1&key={key}"
    response = requests.get(url)
    return response.json()["data"]

# Function to load and convert an SVG to a Pillow image
def load_svg_as_image(svg_path):
    # Convert SVG to PNG in memory
    png_data = svg2png(url=svg_path)
    
    # Load the PNG data into a Pillow image
    image = Image.open(io.BytesIO(png_data))
    return image

if __name__ == '__main__':
    forecast = get_daily_forecast()
    greeting = ""

try:
    disp = LCD_2inch.LCD_2inch()
    disp.Init()
    disp.clear()

    background = Image.open("/home/sthor726/Raspberry-Pi-Smart-Clock/images/wii-menu.png").convert("RGB")
    background = background.resize((disp.height, disp.width))
    
    crt_filter = Image.open("/home/sthor726/Raspberry-Pi-Smart-Clock/images/filter.png").convert("RGBA")
    crt_filter = crt_filter.resize((disp.height, disp.width))

    Font1 = ImageFont.truetype("/home/sthor726/Raspberry-Pi-Smart-Clock/fonts/sysfont.otf", 24)
    Font2 = ImageFont.truetype("/home/sthor726/Raspberry-Pi-Smart-Clock/fonts/sysfont.otf", 28)
    FontLarge = ImageFont.truetype("/home/sthor726/Raspberry-Pi-Smart-Clock/fonts/contm.ttf", 32)
    FontMedium = ImageFont.truetype("/home/sthor726/Raspberry-Pi-Smart-Clock/fonts/contm.ttf", 28)

    disp.clear()  # Clear the screen once during initialization

    # Create a base image with the background and CRT filter
    base_image = background.copy()
    base_image.paste(crt_filter, (0, 0), crt_filter)
    
    getWeather = False
    while True:
        # State 1: Display greeting and date / time
        now = datetime.now()
        current_time = now.strftime("%I:%M %p")
        current_hour = int(now.strftime("%H"))  # Get the hour in 24-hour format
        
        day_of_week = now.strftime("%A")
        today_date = now.strftime("%B %d")
        if current_hour < 12:
            if greeting == "Good Evening!":
                getWeather = True;
            greeting = "Good Morning!"
        elif current_hour < 18:
            if greeting == "Good Morning!":
                getWeather = True;
            greeting = "Good Afternoon!"
        else:
            if greeting == "Good Afternoon!":
                getWeather = True;
            greeting = "Good Evening!"
            
        if(getWeather):
            forecast = get_daily_forecast()
            getWeather = False
        
        

        disp_width, disp_height = disp.height, disp.width  # LCD is rotated, so height is width

        time_bbox = FontMedium.getbbox(current_time)
        date_bbox = FontMedium.getbbox(today_date)
        day_bbox = FontLarge.getbbox(day_of_week)
        greeting_bbox = FontLarge.getbbox(greeting)

        time_text_width = time_bbox[2] - time_bbox[0]
        day_text_width = day_bbox[2] + date_bbox[2] - (day_bbox[0] + date_bbox[0])
        greeting_text_width = greeting_bbox[2] - greeting_bbox[0]
        
        greeting_x = (disp_width - greeting_text_width) // 2
        time_x = (disp_width - time_text_width) // 2
        day_x = (disp_width - day_text_width) // 2
        
        
        
        # swipe from right on screen
        for offset in range(0, disp_width + 1, 10): 
            image1 = base_image.copy()  # Start with the base image
            draw = ImageDraw.Draw(image1)

            draw.text((greeting_x + disp_width + 1 - offset, 20), greeting, fill=TITLE_COLOR, font=FontLarge)
            draw.text((day_x + disp_width + 1 - offset, 100), day_of_week + ", " + today_date, fill=TITLE_COLOR, font=FontMedium)
            draw.text((time_x + disp_width + 1 - offset, 130), current_time, fill=TITLE_COLOR, font=FontLarge)

            disp.ShowImage(image1, 0, 0)
            
            
        image1 = base_image.copy()
        draw = ImageDraw.Draw(image1)    
            
        draw.text((greeting_x, 20), greeting, fill=TITLE_COLOR, font=FontLarge)
        draw.text((day_x, 100), day_of_week + ", " + today_date, fill=TITLE_COLOR, font=FontMedium)
        draw.text((time_x, 130), current_time, fill=TITLE_COLOR, font=FontLarge)
        
        disp.ShowImage(image1, 0, 0)
        
        # get events while greeting page is open - save time in transitions
        events = clock.getCalendarEvents(2)
        time.sleep(10)
        
        # Swipe transition text off screen
        for offset in range(0, disp_width + 1, 10): 
            image1 = base_image.copy()  # Start with the base image
            draw = ImageDraw.Draw(image1)

            draw.text((greeting_x - offset, 20), greeting, fill=TITLE_COLOR, font=FontLarge)
            draw.text((day_x - offset, 100), day_of_week + ", " + today_date, fill=TITLE_COLOR, font=FontMedium)
            draw.text((time_x - offset, 130), current_time, fill=TITLE_COLOR, font=FontLarge)

            disp.ShowImage(image1, 0, 0)

        # State 2: Display upcoming events
        text_bbox = FontLarge.getbbox("Upcoming Events")
        text_width = text_bbox[2] - text_bbox[0]
        text_x = (disp_width - text_width) // 2

        # translate events to text 
        event_details = get_event_text(events)
        
        # swipe from right on screen
        for offset in range(0, disp_width + 1, 10):
            y_offset = 100
            image1 = base_image.copy() 
            draw = ImageDraw.Draw(image1)
            if events:
                for i in range(len(event_details)):
                    event_text = f"{event_details[i][0]} {event_details[i][1]} \n {event_details[i][2]}"
                    draw.text((10 + disp_width + 1 - offset, y_offset), event_text, fill=TEXT_COLOR, font=Font1)
                    y_offset += 50
            else:
                draw.text((10 + disp_width + 1 - offset, 60), "No upcoming events.", fill=TEXT_COLOR, font=Font1)
            draw.text((text_x + disp_width + 1 - offset, 20), "Upcoming Events", fill=TITLE_COLOR, font=FontLarge)
            disp.ShowImage(image1, 0, 0)


        y_offset = 100
        image1 = base_image.copy() 
        draw = ImageDraw.Draw(image1)
        if events:
            for i in range(len(event_details)):
                event_text = f"{event_details[i][0]} {event_details[i][1]} \n {event_details[i][2]}"
                draw.text((10, y_offset), event_text, fill=TEXT_COLOR, font=Font1)
                y_offset += 50
        else:
            draw.text((10, 60), "No upcoming events.", fill=TEXT_COLOR, font=Font1)
        draw.text((text_x, 20), "Upcoming Events", fill=TITLE_COLOR, font=FontLarge)
        disp.ShowImage(image1, 0, 0)


        time.sleep(10)

        # Swipe transition text off screen
        for offset in range(0, disp_width + 1, 10):
            y_offset = 100

            image1 = base_image.copy()  # Start with the base image
            draw = ImageDraw.Draw(image1)

            draw.text((text_x - offset, 20), "Upcoming Events", fill=TITLE_COLOR, font=FontLarge)
            for i, event in enumerate(events[:2]):
                event_text = f"{event_details[i][0]} {event_details[i][1]} \n {event_details[i][2]}"
                draw.text((10 - offset, y_offset), event_text, fill=TEXT_COLOR, font=Font1)
                y_offset += 50

            disp.ShowImage(image1, 0, 0)


        time.sleep(10)
        
        
        # State 3: Display weather forecast with swipe animations
        forecast_title_bbox = FontLarge.getbbox("Today's Forecast")
        forecast_title_width = forecast_title_bbox[2] - forecast_title_bbox[0]
        forecast_title_x = (disp_width - forecast_title_width) // 2 

        # Access the first day's forecast
        today_forecast = forecast[0]

        # Extract weather details
        high = today_forecast["high_temp"].replace(u'\N{DEGREE SIGN}', "")
        low = today_forecast["low_temp"].replace(u'\N{DEGREE SIGN}', "")
        precip = today_forecast["pop"]

        # Handle weather icon based on the icon_code
        icon_code = today_forecast["weather"]["icon"]

        if icon_code[0] == 't':
            # Thunderstorm
            weather_icon_path = "/home/sthor726/Raspberry-Pi-Smart-Clock/images/weathericons/thunder.svg"
        elif icon_code[0] in ['d', 'r']:
            # Rain
            weather_icon_path = "/home/sthor726/Raspberry-Pi-Smart-Clock/images/weathericons/rainy-6.svg"
        elif icon_code[0] == 's':
            # Snow
            weather_icon_path = "/home/sthor726/Raspberry-Pi-Smart-Clock/images/weathericons/snowy-6.svg"
        elif icon_code[0] == 'a':
            # Haze
            weather_icon_path = "/home/sthor726/Raspberry-Pi-Smart-Clock/images/weathericons/haze.svg"
        elif icon_code[:3] == 'c01':
            # Clear
            weather_icon_path = "/home/sthor726/Raspberry-Pi-Smart-Clock/images/weathericons/day.svg"
        elif icon_code[:3] in ['c02', 'c03']:
            # Partly Cloudy
            weather_icon_path = "/home/sthor726/Raspberry-Pi-Smart-Clock/images/weathericons/cloudy-day-2.svg"
        elif icon_code[:3] == 'c04':
            # Cloudy
            weather_icon_path = "/home/sthor726/Raspberry-Pi-Smart-Clock/images/weathericons/cloudy.svg"
        else:
            # Unknown condition
            weather_icon_path = "/home/sthor726/Raspberry-Pi-Smart-Clock/images/weathericons/weather.svg"

        # Load and resize the weather icon
        weather_icon = load_svg_as_image(weather_icon_path)
        weather_icon = weather_icon.resize((100, 100))

        # Swipe in the weather forecast from the right
        for offset in range(0, disp_width + 1, 10):  # Increment by 10 pixels per frame
            image1 = base_image.copy()  # Start with the base image
            draw = ImageDraw.Draw(image1)

            # Move the forecast title
            draw.text((forecast_title_x + disp_width + 1 - offset, 20), "Today's Forecast", fill=TITLE_COLOR, font=FontLarge)

            # Move the high, low, and precipitation values
            draw.text((10 + disp_width + 1 - offset, 80), f"Day: {high}°F", fill=ORANGE, font=FontMedium)
            draw.text((10 + disp_width + 1 - offset, 120), f"Night: {low}°F", fill=BLUE, font=Font1)
            draw.text((10 + disp_width + 1 - offset, 160), f"Precipitation: {precip}%", fill=TEXT_COLOR, font=Font1)

            # Move the weather icon
            image1.paste(weather_icon, (disp_width - 200 + disp_width + 1 - offset, 80), weather_icon)

            # Display the updated image
            disp.ShowImage(image1, 0, 0)

        # Display the weather forecast in its final position
        image1 = base_image.copy()
        draw = ImageDraw.Draw(image1)

        # Draw the forecast title
        draw.text((forecast_title_x, 20), "Today's Forecast", fill=TITLE_COLOR, font=FontLarge)

        # Draw the high, low, and precipitation values
        draw.text((10, 80), f"Day: {high}°F", fill=ORANGE, font=Font2)
        draw.text((10, 120), f"Night: {low}°F", fill=BLUE, font=Font1)
        draw.text((10, 160), f"Precipitation: {precip}%", fill=TEXT_COLOR, font=Font1)

        # Draw the weather icon
        image1.paste(weather_icon, (disp_width - 200, 80), weather_icon)

        # Display the final image
        disp.ShowImage(image1, 0, 0)

        time.sleep(10)

        # Swipe out the weather forecast to the left
        for offset in range(0, disp_width + 1, 10):  # Increment by 10 pixels per frame
            image1 = base_image.copy()  # Start with the base image
            draw = ImageDraw.Draw(image1)

            # Move the forecast title
            draw.text((forecast_title_x - offset, 20), "Today's Forecast", fill=TITLE_COLOR, font=FontLarge)

            # Move the high, low, and precipitation values
            draw.text((10 - offset, 80), f"Day: {high}°F", fill=ORANGE, font=Font2)
            draw.text((10 - offset, 120), f"Night: {low}°F", fill=BLUE, font=Font1)
            draw.text((10 - offset, 160), f"Precipitation: {precip}%", fill=TEXT_COLOR, font=Font1)

            # Move the weather icon
            image1.paste(weather_icon, (disp_width - 200 - offset, 80), weather_icon)

            # Display the updated image
            disp.ShowImage(image1, 0, 0)
        
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
