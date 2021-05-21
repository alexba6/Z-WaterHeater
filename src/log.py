from os import path, mkdir
import datetime

_LOG_DIR = './log'


class _Log:
    def __init__(self, log_type):
        self._log_type = log_type

    def add(self, msg):
        log_path = path.join(_LOG_DIR, f"{self._log_type}.log")
        with open(log_path, 'a', encoding='utf-8') as log_file:
            date = datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")
            log_file.write(f"[{date}] - {msg}")


if not path.exists(_LOG_DIR):
    mkdir(_LOG_DIR)


error_logger = _Log('error')
warning_logger = _Log('warning')
info_logger = _Log('info')
authentication_logger = _Log('auth')

