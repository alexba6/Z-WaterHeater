from os import path, makedirs
import json

from .log import logger

METADATA_PATH = './data/meta'


class MetaData:
    def __init__(self, name: str):
        self.name: str = name
        self.path: str = path.join(METADATA_PATH, f"{name}.json")
        self._dataCache = None
        if path.exists(self.path):
            try:
                with open(self.path, 'r', encoding='utf-8') as file:
                    self._dataCache = json.load(file)
            except Exception as error:
                logger.error(error)

    @property
    def data(self):
        return self._dataCache

    @data.setter
    def data(self, data):
        with open(self.path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(data, sort_keys=True, indent=3, separators=(',', ': ')))
        self._dataCache = data


if not path.exists(METADATA_PATH):
    makedirs(METADATA_PATH, exist_ok=True)
