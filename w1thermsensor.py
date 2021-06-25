
class AsyncW1ThermSensor:
    def __init__(self, sensorType, sensor_id):
        self.type = sensorType
        self.id = sensor_id
        self._t = 22.7

    @classmethod
    def get_available_sensors(cls):
        # You can update the response to virtualize some sensor in development mode
        return [
            AsyncW1ThermSensor(None, '020f91775390'),
            AsyncW1ThermSensor(None, '071d91527342')
        ]

    async def get_temperature(self, unit=None):
        return self._t

    def __getattr__(self, name):
        def t(*args):
            return None
        return t


class Default:
    def __getattr__(self, name):
        def t(*args):
            return None
        return t


Unit = Default()
Sensor = Default()
