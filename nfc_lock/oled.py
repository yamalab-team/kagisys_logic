# Copyright (c) 2017 Adafruit Industries
# Author: Tony DiCola & James DeVito
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


# -*- coding: utf-8 -*-
import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

class OLED_Display:
    def __init__(self):
        # Raspberry Pi pin configuration:
        self.RST = None     # on the PiOLED this pin isnt used
        # Note the following are only used with SPI:
        self.DC = 23
        self.SPI_PORT = 0
        self.SPI_DEVICE = 0

        # Beaglebone Black pin configuration:
        # RST = 'P9_12'
        # Note the following are only used with SPI:
        # DC = 'P9_15'
        # SPI_PORT = 1
        # SPI_DEVICE = 0

        # 128x32 display with hardware I2C:
        self.disp = Adafruit_SSD1306.SSD1306_128_32(rst=self.RST)

        # 128x64 display with hardware I2C:
        # disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

        # Note you can change the I2C address by passing an i2c_address parameter like:
        # disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)

        # Alternatively you can specify an explicit I2C bus number, for example
        # with the 128x32 display you would use:
        # disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, i2c_bus=2)

        # 128x32 display with hardware SPI:
        # disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

        # 128x64 display with hardware SPI:
        # disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

        # Alternatively you can specify a software SPI implementation by providing
        # digital GPIO pin numbers for all the required display pins.  For example
        # on a Raspberry Pi with the 128x32 display you might use:
        # disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, sclk=18, din=25, cs=22)

        # Initialize library.
        self.disp.begin()

        # Clear display.
        self.disp.clear()
        self.disp.display()

        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        self.width = self.disp.width
        self.height = self.disp.height
        self.image = Image.new('1', (self.width, self.height))

        # Get drawing object to draw on image.
        self.draw = ImageDraw.Draw(self.image)

        # Draw a black filled box to clear the image.
        self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)

        # Draw some shapes.
        # First define some constants to allow easy resizing of shapes.
        self.padding = -2
        self.top = self.padding
        self.bottom = self.height-self.padding
        # Move left to right keeping track of the current x position for drawing shapes.
        self.x = 0


        # Load default font.
        self.fontE = ImageFont.load_default()
        self.fontJ = ImageFont.load.truetype('fonts-japanese-gothic.ttf', 8)

        # Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
        # Some other nice fonts to try: http://www.dafont.com/bitmap.php
        # font = ImageFont.truetype('Minecraftia.ttf', 8)
        self.cmd = "hostname -I | cut -d\' \' -f1"
        self.IP = subprocess.check_output(self.cmd, shell = True )
        self.draw.text((self.x, self.top),       "IP: " + str(self.IP),  font=self.font, fill=255)
        self.disp.image(self.image)
        self.disp.display()
    
    # textsは配列で与える max3つ
    def display(self, texts):
        self.draw.text((self.x, self.top),       "IP: " + str(self.IP),  font=self.fontE, fill=255)
        self.max = min(len(texts), 2) 
        for i in range(self.max):
            self.draw.text((self.x, self.top+((i+1)*10)), texts[i], font=self.fontJ, fill=255)
        self.disp.image(self.image)
        self.disp.display()

    def clear(self):
        self.draw.text((self.x, self.top),       "IP: " + str(self.IP),  font=self.fontE, fill=255)
        self.disp.image(self.image)
        self.disp.display()
