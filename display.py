#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import chardet
import os
import clock
import sys
import time
import logging
import spidev as SPI
sys.path.append("..")
from lib import LCD_2inch
from PIL import Image,ImageDraw,ImageFont

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0
device = 0
logging.basicConfig(level=logging.DEBUG)
try:
    # display with hardware SPI:
    ''' Warning!!!Don't  creation of multiple displayer objects!!! '''
    #disp = LCD_2inch.LCD_2inch(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
    disp = LCD_2inch.LCD_2inch()
    # Initialize library.
    disp.Init()
    # Clear display.
    disp.clear()

    # Create blank image for drawing.
    image1 = Image.new("RGB", (disp.height, disp.width ), "WHITE")
    draw = ImageDraw.Draw(image1)
    
    # logging.info("draw point")

    # draw.rectangle((5,10,6,11), fill = "BLACK")
    # draw.rectangle((5,25,7,27), fill = "BLACK")
    # draw.rectangle((5,40,8,43), fill = "BLACK")
    # draw.rectangle((5,55,9,59), fill = "BLACK")

    # logging.info("draw line")
    # draw.line([(20, 10),(70, 60)], fill = "RED",width = 1)
    # draw.line([(70, 10),(20, 60)], fill = "RED",width = 1)
    # draw.line([(170,15),(170,55)], fill = "RED",width = 1)
    # draw.line([(150,35),(190,35)], fill = "RED",width = 1)

    # logging.info("draw rectangle")
    # draw.rectangle([(20,10),(70,60)],fill = "WHITE",outline="BLUE")
    # draw.rectangle([(85,10),(130,60)],fill = "BLUE")

    # logging.info("draw circle")
    # draw.arc((150,15,190,55),0, 360, fill =(0,255,0))
    # draw.ellipse((150,65,190,105), fill = (0,255,0))

    # logging.info("draw text")
    #Font1 = ImageFont.truetype("/home/sthor726/Raspberry-Pi-Smart-Clock/Font/Font00.ttf",25)
    #Font2 = ImageFont.truetype("/home/sthor726/Raspberry-Pi-Smart-Clock/Font/Font01.ttf",35)
    #Font3 = ImageFont.truetype("/home/sthor726/Raspberry-Pi-Smart-Clock/Font/Font02.ttf",32) # Absolute path
    Font1 = ImageFont.truetype("Font01.ttf", 25)  # Set font size

    # draw.rectangle([(0,65),(140,100)],fill = "WHITE")
    # draw.text((5, 68), 'Hello world', fill = "BLACK",font=Font1)
    # draw.rectangle([(0,115),(190,160)],fill = "RED")
    # draw.text((5, 118), 'WaveShare', fill = "WHITE",font=Font2)
    # draw.text((5, 160), '1234567890', fill = "GREEN",font=Font3)
    while(True):
        events = clock.getCalendarEvents(5)
        if events:
            for event in events:
                logging.info(event)
                draw.text((5, 68), event, fill = "BLACK",font=Font1)
                disp.ShowImage(image1,0,0)
                time.sleep(5)
                disp.clear()
        else:
            logging.info("No upcoming events found.")
            draw.text((5, 68), "No upcoming events found.", fill = "BLACK",font=Font1)
            disp.ShowImage(image1,0,0)
        
    
except IOError as e:
    logging.info(e)
except KeyboardInterrupt:
    disp.module.exit()
    logging.info("quit: ")
    exit()
