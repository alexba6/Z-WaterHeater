from os import path, mkdir
import json

METADATA_PATH = './meta'


class MetaData:
    def __init__(self, name):
        self.name = name
        self.path = path.join(METADATA_PATH, f"{name}.json")
        self._data_cache = {}
        if path.exists(self.path):
            try:
                with open(self.path, 'r', encoding='utf-8') as file:
                    self._data_cache = json.load(file)
            except:
                pass

    @property
    def data(self):
        return self._data_cache

    @data.setter
    def data(self, data):
        with open(self.path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(data))
        self._data_cache = data

    def add_property(self, name, value):
        self._data_cache[name] = value
        self.data = self._data_cache


if not path.exists(METADATA_PATH):
    mkdir(METADATA_PATH)
