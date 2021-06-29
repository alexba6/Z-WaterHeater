import threading
import string
from typing import List
from Adafruit_SSD1306 import SSD1306_128_32

from RPi import GPIO

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from Z_WH.config import APP_ENV, DEV
from Z_WH.tools.randomString import getRandomString

DISPLAY_SIZE = (128, 32)


class SlideError(Exception):
    def __init__(self, message: str):
        self.message = message


class Slide:
    def __init__(self, **kwargs):
        self.id: str = kwargs.get('id')
        duration = kwargs.get('duration')
        if duration is None:
            duration = 2
        assert duration <= 3, SlideError('Duration must be under 3 seconds !')
        self.duration: float = duration
        self._image: Image or None = None
        self.enable = True

    def newId(self):
        self.id = getRandomString(string.ascii_uppercase + string.digits, 8)

    @property
    def image(self):
        if not self.enable:
            raise SlideError('Slide deleted !')
        return self._image

    @image.setter
    def image(self, image: Image):
        self._image = image


class DisplayManager:
    def __init__(self):
        self._slides: List[Slide] = []

        self._slideThread = threading.Timer(0, lambda: self._changeSlide())

        self._slideIndex: int = 0
        self._showNowTimer = None
        if APP_ENV == DEV:
            return
        self._display: SSD1306_128_32 = SSD1306_128_32(rst=None)
        GPIO.cleanup()

    # Init the display screen
    def init(self):

        homeSlid = Slide(duration=2)
        homeSlid.newId()

        image = Image.new('1', DISPLAY_SIZE)
        draw = ImageDraw.Draw(image)
        ImageFont.load_default()
        font = ImageFont.truetype('Z_WH/assets/font/coolvetica.ttf', 26)
        draw.text((35, 0), 'Z-WH', font=font, fill=255)

        homeSlid.image = image
        self.addSlide(homeSlid)

        if APP_ENV == DEV:
            self._slideThread.start()
            return
        self._display.begin()
        self._display.clear()
        self._display.display()
        self._slideThread.start()

    # Add defilement slide in the buffer
    def addSlide(self, slide: Slide):
        for currentSlide in self._slides:
            if currentSlide.id == slide.id:
                return
        self._slides.append(slide)

    # Get the current slide
    def _getCurrentSlide(self):
        if self._slideIndex >= len(self._slides):
            self._slideIndex = 0
        slide = self._slides[self._slideIndex]
        self._slideIndex += 1
        if not slide.enable:
            self._getCurrentSlide()
        return slide

    # Auto change the slide
    def _changeSlide(self):
        currentSlide = self._getCurrentSlide()
        self._slideThread = threading.Timer(currentSlide.duration, lambda: self._changeSlide())
        if APP_ENV == DEV:
            self._slideThread.start()
            return
        self._display.clear()
        try:
            self._display.image(currentSlide.image)
        except SlideError:
            self._changeSlide()
        self._display.display()
        self._slideThread.start()

    # Stop the slide defilement ans show an image
    def showImageNow(self,  duration: int, image: Image):
        if self._slideThread.is_alive():
            self._slideThread.cancel()

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
        if self._showNowTimer and self._slideThread.is_alive():
            self._slideThread.cancel()
        if not self._slideThread.is_alive():
            self._changeSlide()
