"""
--------------------------------------------------------------------------
Sun Clock via PocketBeagle
--------------------------------------------------------------------------
License:   
Copyright 2019 - Annabel Chang

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, 
this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------
Clock 

  - RTC connected to I2C1
  - Screen connected to SPI1
  - Servo connected to PWM0 (P1_36)
  - Buzzer connected to PWM1 (P2_1)
  - Mode button connected to Pin 64 (P1_20)
  - Up button connected to Pin 46 (P1_22)
  - Down button connected to Pin 48 (P1_24)

"""
# ------------------------------------------------------------------------
# Libraries
# ------------------------------------------------------------------------

# Import Libraries
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO
import time
import datetime
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.ili9341 as ili9341

# ------------------------------------------------------------------------
# Variables
# ------------------------------------------------------------------------

# Pin Assignments
SERVO = "P1_36"
BUTTON_MODE = "P2_20"
BUTTON_HOUR = "P2_22"
BUTTON_MINUTE = "P2_24"
BUZZER = "P2_1"


# Define Variables
time_zone = -6 # CST
hour = datetime.datetime.now().hour + time_zone
if(hour < 0):
    hour += 24
minute = datetime.datetime.now().minute
alarm_hour = 0
alarm_minute = 0
alarm = 0
old_hour = 0
old_minute = 0
b4_hour = 0
b4_minute = 0


# ------------------------------------------------------------------------
# Setup
# ------------------------------------------------------------------------

# Calibrate Servo
PWM.start(SERVO,50,60)
time.sleep (1.0)
PWM.stop(SERVO)
PWM.cleanup()

# Initialize Buttons
GPIO.setup(BUTTON_MODE, GPIO.IN)
GPIO.setup(BUTTON_HOUR, GPIO.IN)
GPIO.setup(BUTTON_MINUTE, GPIO.IN)

# Setup Screen
# First define some constants to allow easy resizing of shapes.
BORDER = 20
FONTSIZE = 70
 
# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.P2_6)
dc_pin = digitalio.DigitalInOut(board.P2_8)
reset_pin = digitalio.DigitalInOut(board.P2_10)
 
# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000
 
# Setup SPI bus using hardware SPI:
spi = board.SPI()
disp = ili9341.ILI9341(spi, rotation=90,                           # 2.2", 2.4", 2.8", 3.2" ILI9341
                       cs=cs_pin, dc=dc_pin, rst=reset_pin, baudrate=BAUDRATE)
                       
# ------------------------------------------------------------------------
# Main Script
# ------------------------------------------------------------------------

# Format and Display Time
print("{0:0>2}".format(hour), ':', "{0:0>2}".format(minute))
 
# Create blank image for drawing with mode 'RGB' for full color
if disp.rotation % 180 == 90:
    height = disp.width   #swap height/width to rotate to landscape
    width = disp.height
else:
    width = disp.width
    height = disp.height
 
image = Image.new('RGB', (width, height))
 
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
 
# Draw a gray filled box as the background
draw.rectangle((0, 0, width, height), fill=(128, 128, 128))
disp.image(image)
 
# Draw a smaller inner blue rectangle
draw.rectangle((BORDER, BORDER, width - BORDER - 1, height - BORDER - 1),
               fill=(0, 255, 255))
 
# Load a TTF Font
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', FONTSIZE)
 
# Draw Some Text
text = str("{0:0>2}".format(hour))+':'+str("{0:0>2}".format(minute))
(font_width, font_height) = font.getsize(text)
draw.text((width//2 - font_width//2, height//2 - font_height//2),
          text, font=font, fill=(0, 0, 0))
 
# Display image.
disp.image(image)

while(True): 
    
    # Update Time
    updated_hour = datetime.datetime.now().hour + time_zone
    if(updated_hour < 0):
        updated_hour += 24
    updated_minute = datetime.datetime.now().minute
    if(updated_hour != hour or updated_minute != minute):
        print("{0:0>2}".format(updated_hour), ':', "{0:0>2}".format(updated_minute))
        # Update Screen
        draw.rectangle((BORDER, BORDER, width - BORDER - 1, height - BORDER - 1),
               fill=(0, 255, 255))
        text = str("{0:0>2}".format(updated_hour))+':'+str("{0:0>2}".format(updated_minute))
        (font_width, font_height) = font.getsize(text)
        draw.text((width//2 - font_width//2, height//2 - font_height//2),
                  text, font=font, fill=(0, 0, 0))
        disp.image(image)
    hour = updated_hour
    minute = updated_minute
    
    # Set Alarm while Mode Button is Held
    while(GPIO.input(BUTTON_MODE) == 1):
        
        # Increment Time if Up Button is Pressed
        cur_hour = GPIO.input(BUTTON_HOUR)
        if(cur_hour-old_hour == 1):
            alarm_hour += 1
            if(alarm_hour == 24):
                alarm_hour = 0
            print("Alarm", "{0:0>2}".format(alarm_hour), ':', "{0:0>2}".format(alarm_minute))
            #Update Screen
            draw.rectangle((BORDER, BORDER, width - BORDER - 1, height - BORDER - 1),
               fill=(0, 255, 255))
            text = str("{0:0>2}".format(alarm_hour))+':'+str("{0:0>2}".format(alarm_minute))
            (font_width, font_height) = font.getsize(text)
            draw.text((width//2 - font_width//2, height//2 - font_height//2),
                      text, font=font, fill=(0, 0, 0))
            disp.image(image)
        old_hour = cur_hour
    
        # Decrement Time if Down Button is Pressed
        cur_minute = GPIO.input(BUTTON_MINUTE)
        if(cur_minute-old_minute == 1):
            alarm_minute += 1
            if(alarm_minute == 60):
                alarm_minute = 0
            print("Alarm", "{0:0>2}".format(alarm_hour), ':', "{0:0>2}".format(alarm_minute))
            #Update Screen
            draw.rectangle((BORDER, BORDER, width - BORDER - 1, height - BORDER - 1),
               fill=(0, 255, 255))
            text = str("{0:0>2}".format(alarm_hour))+':'+str("{0:0>2}".format(alarm_minute))
            (font_width, font_height) = font.getsize(text)
            draw.text((width//2 - font_width//2, height//2 - font_height//2),
                      text, font=font, fill=(0, 0, 0))
            disp.image(image)
        old_minute = cur_minute
        
        time.sleep(0.1)
        
    # Turn On/Off Alarm if Up and Down Buttons are Pressed at the Same Time
    now_hour = GPIO.input(BUTTON_HOUR)
    now_minute = GPIO.input(BUTTON_MINUTE)
    if(now_hour+now_minute == 2 and b4_hour+b4_minute != 2):
        if(alarm == 0):
            alarm = 1
            print('ALARM ON!')
            #Update Screen with Red Border
            draw.rectangle((0, 0, width, height), fill=(255, 0, 0))
            draw.rectangle((BORDER, BORDER, width - BORDER - 1, height - BORDER - 1),
               fill=(0, 255, 255))
            text = str("{0:0>2}".format(updated_hour))+':'+str("{0:0>2}".format(updated_minute))
            (font_width, font_height) = font.getsize(text)
            draw.text((width//2 - font_width//2, height//2 - font_height//2),
                      text, font=font, fill=(0, 0, 0))
            disp.image(image)
        else:
            alarm = 0
            print('ALARM OFF!')
            #Update Screen with Gray Border
            draw.rectangle((0, 0, width, height), fill=(128, 128, 128))
            draw.rectangle((BORDER, BORDER, width - BORDER - 1, height - BORDER - 1),
               fill=(0, 255, 255))
            text = str("{0:0>2}".format(updated_hour))+':'+str("{0:0>2}".format(updated_minute))
            (font_width, font_height) = font.getsize(text)
            draw.text((width//2 - font_width//2, height//2 - font_height//2),
                      text, font=font, fill=(0, 0, 0))
            disp.image(image)
    b4_hour = now_hour
    b4_minute = now_minute
    
    # Sound Buzzer at Correct Time if Alarm is On
    if(alarm == 1 and alarm_hour == hour and alarm_minute == minute):
        print("BUZZZZ")
        for i in 'beep':
            PWM.start(BUZZER, 50, 1500)
            time.sleep(1.0)
            PWM.stop(BUZZER)
            time.sleep(1.0)
        alarm = 0
        #Update Screen with Gray Border
        draw.rectangle((0, 0, width, height), fill=(128, 128, 128))
        draw.rectangle((BORDER, BORDER, width - BORDER - 1, height - BORDER - 1),
           fill=(0, 255, 255))
        text = str("{0:0>2}".format(updated_hour))+':'+str("{0:0>2}".format(updated_minute))
        (font_width, font_height) = font.getsize(text)
        draw.text((width//2 - font_width//2, height//2 - font_height//2),
                  text, font=font, fill=(0, 0, 0))
        disp.image(image)
        PWM.cleanup()
        print('ALARM OFF!')
    
    # Rotate Servo CCW 180 Degrees at 6am and 6pm
    if((updated_hour == 6 and updated_minute == 0 and minute == 59) or (updated_hour == 18 and updated_minute == 0 and minute == 59)):
        PWM.start(SERVO,0,60)
        time.sleep (1.0)
        PWM.stop(SERVO)
        PWM.cleanup()
        time.sleep(1.0)
    
