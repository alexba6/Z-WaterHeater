import random
import datetime
import threading
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from .display import display


class VerificationCodeError(Exception):
    def __init__(self, status: str,  message: str):
        self.status = status
        self.message = message


class VerificationCode:
    def __init__(self):
        self._code: str or None = None
        self._generatedAt: datetime.datetime or None = None
        self._expirationTime: int or None = None
        self._codeAttempt: int = 0
        self._displayTimer = None

    def generateCode(self, expiration: int = 60):
        date = datetime.datetime.now()
        if self._generatedAt is not None and (date-self._generatedAt).total_seconds() < self._expirationTime:
            raise VerificationCodeError('ALREADY_AVAILABLE', 'Already valid code available')

        self._code = "".join(map(str, random.sample(range(10), 6)))
        self._generatedAt = datetime.datetime.now()
        self._expirationTime = expiration

        image = Image.new('1', display.displaySize)

        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('src/assets/font/coolvetica.ttf', 30)
        draw.text((10, 1), f'{self._code}', font=font, fill=255)

        display.showImageNow(expiration, image)

        self._displayTimer = threading.Timer(expiration, lambda: display.startSlide())
        self._displayTimer.start()

    def _clearCode(self):
        self._expirationTime = 0
        if self._displayTimer and self._displayTimer.is_alive():
            self._displayTimer.cancel()

    def verifyCode(self, code: str):
        date = datetime.datetime.now()
        self._codeAttempt += 1

        if self._codeAttempt > 3:
            self._expirationTime = 0
            raise VerificationCodeError('TOO_MANY_ATTEMPT', 'Too many attempt')

        if (date-self._generatedAt).total_seconds() > self._expirationTime:
            raise VerificationCodeError('EXPIRED_CODE', 'Expired code')

        if code != self._code:
            raise VerificationCodeError('INVALID_CODE', 'Invalid code')

        self._expirationTime = 0


verificationCode = VerificationCode()
