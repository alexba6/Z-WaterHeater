from os import path, makedirs
import datetime

LOG_DIR = './data/log'

if not path.exists(LOG_DIR):
    makedirs(LOG_DIR, exist_ok=True)


class Logger:
    def __init__(self, logFileName: str, *allowLoggers: str):
        self.logPath = path.join(LOG_DIR, f'{logFileName}.log')
        self.allowLogger = ['error', 'info', 'warning']
        for allowLogger in allowLoggers:
            self.allowLogger.append(allowLogger)

    def __getattr__(self, item):
        logType = str(item).lower()
        if logType not in self.allowLogger:
            raise Exception('Cannot write this type of log !')

        def write_log(message):
            message = str(message)
            with open(self.logPath, 'a', encoding='utf-8') as logFile:
                date = datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")
                logFile.write(f"[{date}] - {logType.upper()} - {message}\n")

        return write_log
