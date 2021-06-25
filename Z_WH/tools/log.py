from typing import List
from os import path, makedirs
import datetime


class Logger:
    def __init__(self, log_dir: str, allow_logger: List[str]):
        self.log_dir = log_dir
        self.allow_logger = allow_logger
        self.start()

    def start(self):
        if not path.exists(self.log_dir):
            makedirs(self.log_dir, exist_ok=True)

    def __getattr__(self, item):
        log_type = str(item).lower()

        if log_type not in self.allow_logger:
            raise Exception('Cannot write this type of log !')

        def write_log(message):
            message = str(message)
            log_path = path.join(self.log_dir, f'{log_type}.log')
            with open(log_path, 'a', encoding='utf-8') as log_file:
                date = datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")
                log_file.write(f"[{date}] - {message}\n")

        return write_log


logger = Logger(
    './data/log',
    ['error', 'warning', 'info', 'auth']
)
