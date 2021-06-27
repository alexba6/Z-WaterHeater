import threading
from typing import List
from Adafruit_SSD1306 import SSD1306_128_32

from RPi import GPIO

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from ..config import APP_ENV, DEV


class DisplayManager:
    def __init__(self):
        self._slideImages: List[List[int, object]] = []
        self._slideTimer = threading.Timer(0, lambda: self._changeSlide())
        self._slideIndex: int = 0

        self._showNowTimer = None

        self.displaySize = (128, 64)

        if APP_ENV == DEV:
            return
        self._display: SSD1306_128_32 = SSD1306_128_32(rst=None)
        GPIO.cleanup()

    # Init the display screen
    def init(self):
        image = Image.new('1', self.displaySize)
        draw = ImageDraw.Draw(image)
        ImageFont.load_default()
        font = ImageFont.truetype('Z_WH/assets/font/coolvetica.ttf', 32)
        draw.text((30, 0), 'Z-WH', font=font, fill=255)
        self._slideImages.append([2, lambda: image])

        self._slideTimer.start()
        if APP_ENV == DEV:
            return
        self._display.begin()
        self._display.clear()
        self._display.display()

    # Add defilement slide in the buffer
    def addSlide(self, duration: float = 2, func=None):
        self._slideImages.append([
            duration,
            func
        ])

    # Auto change the slide
    def _changeSlide(self):
        duration, func = self._slideImages[self._slideIndex]
        self._slideTimer = threading.Timer(duration, lambda: self._changeSlide())

        if self._slideIndex + 1 != len(self._slideImages):
            self._slideIndex += 1
        else:
            self._slideIndex = 0

        self._slideTimer.start()

        img: Image = func()

        if APP_ENV == DEV:
            return

        self._display.clear()
        self._display.image(img)
        self._display.display()

    # Stop the slide defilement ans show an image
    def showImageNow(self,  duration: int, image: Image):
        self._slideTimer.cancel()

        self._showNowTimer = threading.Timer(duration, lambda: self._changeSlide())
        self._showNowTimer.start()

        if APP_ENV == DEV:
            image.show()
            return

        self._display.clear()
        self._display.image(image)
        self._display.display()

    # Resume the slide timer
    def startSlide(self):
        if self._showNowTimer and self._slideTimer.is_alive():
            self._slideTimer.cancel()
        if not self._slideTimer.is_alive():
            self._changeSlide()
