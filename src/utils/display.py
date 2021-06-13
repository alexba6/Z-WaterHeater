import threading
import Adafruit_SSD1306

from RPi import GPIO

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from ..config import APP_ENV, DEV


class Display:
    def __init__(self):
        if APP_ENV == DEV:
            return
        self._display = Adafruit_SSD1306.SSD1306_128_32(rst=None)
        GPIO.cleanup()

    def init(self):
        if APP_ENV == DEV:
            return
        self._display.begin()
        self._display.clear()
        self._display.display()
        self.printHome()

    def printHome(self):
        if APP_ENV == DEV:
            return
        print(self._display.width, self._display.height)
        image = Image.new('1', (self._display.width, self._display.height))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('src/assets/font/coolvetica.ttf', 32)
        draw.text((30, 0), 'Z-CE', font=font, fill=255)
        self._display.clear()
        self._display.image(image)
        self._display.display()

    def printCode(self, code: str, durationSecond: int):
        if APP_ENV == DEV:
            print(f'Code : {code}')
            return
        print(self._display.width, self._display.height)
        image = Image.new('1', (self._display.width, self._display.height))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('src/assets/font/coolvetica.ttf', 30)
        draw.text((10, 1), f'{code}', font=font, fill=255)
        self._display.clear()
        self._display.image(image)
        self._display.display()

        threading.Timer(durationSecond, lambda: self.printHome()).start()


display = Display()
