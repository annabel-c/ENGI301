# PocketBeagle Sun Clock
Clock that shows the position of the sun and has a screen display of time; alarm can be set through mode, hour, and minute buttons

## Materials
PocketBeagle	
BeagleBoard.org PocketBeagle ×	1	

SparkFun HS-422 Servo ×	1	

Adafruit CR1220 12mm Diameter - 3V Lithium Coin Cell Battery - CR1220 ×	1	

Adafruit DS1307 Real Time Clock Assembled Breakout Board ×	1	

Buzzer	×	1	

Adafruit 2.8" TFT LCD with Touchscreen Breakout Board w/MicroSD Socket - ILI9341 ×	1	

Pushbutton switch 12mm SparkFun Pushbutton switch 12mm ×	3	

Resistor 1k ohm ×	2	

Resistor 2.2k ohm	×	2	

Breadboard (generic) ×	1	

## Story
When times call for another alarm clock--why not build it yourself? Make it fun with your personal indoor sun and moon (great for a cloudy day!), and have the option to set an alarm through 3 simple buttons: mode, hour and minute.



## Overview

The TFT display shows the time. Time is set upon boot, in Central Standard Time. Hold down the mode button (blue) to set an alarm time with hour (yellow) and minute (red). Every press increments the respective parameter by 1. Press hour and minute buttons at the same time to toggle alarm on and off. The on state is indicated by a red border (replacing the original gray one) on the screen display. A buzzer will sound at the time of the alarm, lasting a few seconds and turning off automatically. The servo will rotate 180 degrees at 6 am and 6 pm, revealing the sun or moon representing daytime or nighttime, respectively.

## Instructions

#### Hardware

Connect everything as shown in the Fritzing diagram. Headers/pins should be soldered to the PocketBeagle, the screen, and the RTC; the rest can easily be connected via wires on a breadboard. It can be helpful to use two power rails such that one runs at 3.3 V and the other at 5V. Note that there are three pads (IM1/2/3) on the bottom of the screen that must be soldered in order for SPI to work.

The main pin configurations are described below:

TFT screen - SPI0

RTC - I2C1

Servo - PWM0

Speaker - PWM1

Buttons - GPIO 64, 46, 48




### Software

For help getting started with a PocketBeagle, see https://beagleboard.org/getting-started. Before running the code, several libraries must be downloaded:

- Install the Adafruit_Blinka library by running the following in Cloud9 IDE

sudo pip3 install Adafruit_Blinka

(run "sudo apt-get install python-setuptools" and "sudo apt-get install python-dev" if the above throws an error)

and download the Adafruit CircuitPython Library Bundle at https://github.com/adafruit/Adafruit_CircuitPython_Bundle

- Follow the instructions at https://learn.adafruit.com/adafruit-2-dot-8-color-tft-touchscreen-breakout-v2/python-wiring-and-setup for installing the RGB Display Library, DejaVu TTF Font, and the Pillow Library

See the Hackster.io page for more details: https://www.hackster.io/annabel-chang/pocketbeagle-sun-clock-f72acc

In the process of coding, make sure to use python3 (instead of python) is and use the prefix "sudo" to resolve any permission issues.

With everything set up, running

sudo python3 sun_clock.py

in the current directory should produce the clock display and functions as described in the first section. An auto run is also set up for this project such that the file runs upon boot.

A video demonstrating how the alarm works can be reached here: https://www.youtube.com/watch?v=hUiSdnFPSFs&feature=youtu.be

The current time is 03:22, the alarm is set to 03:23 by holding the mode button and pressing the minute button (not shown setting from the initial 00:00 due to time constraints), the alarm is turned on by pressing hour and minute together (screen border turns red), and wait.... the alarm begins beeping at the set time! The alarm eventually terminates and the gray screen border is restored.



## Future Work

The screen provides a great deal of potential and versatility for this project; a touchscreen controller can be added so that touchcreen buttons replace the physical one, or other modes such as photo galleries and temperature/humidity detection can be included within the clock.

Python code for RTC with PocketBeagle remains to be investigated, hence this iteration of this project relies on datetime for time information. Future iterations could focus more on user-setting time and mode changes.

In addition, to become a more finished, stand-alone product, the clock should have a battery instead of an USB cable, and an aesthetic casing or LED effects would put the finishing touches on it.
