import random
import datetime

INVALID_CODE, EXPIRED_CODE, VALID_CODE = 'invalid', 'expire', 'ok'


class CodeGenerator:
    def __init__(self, code_size=6):
        self.code = None
        self.created_at = None
        self.expiration_time = None
        self.code_size = code_size

    def start_code(self, expiration_time=60):
        self.code = str(random.randint(10**(self.code_size - 1), 10**self.code_size))
        self.created_at = datetime.datetime.now()
        self.expiration_time = expiration_time
        print(self.code)

    def code_expire(self):
        if not self.created_at:
            return True
        return (datetime.datetime.now() - self.created_at).total_seconds() > self.expiration_time

    def verify_code(self, code):
        date = datetime.datetime.now()
        if not self.code or (date-self.created_at).total_seconds() > self.expiration_time:
            return EXPIRED_CODE
        if len(code) > self.code_size or code != self.code:
            return INVALID_CODE
        self.code = None
        return VALID_CODE


code_generator = CodeGenerator()
