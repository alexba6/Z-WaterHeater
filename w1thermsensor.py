class AsyncW1ThermSensor:
    def __init__(self, sensorType, sensor_id):
        self.type = sensorType
        self.id = sensor_id
        self._t = 55
        self.a = True
        self.c = 0

    @classmethod
    def get_available_sensors(cls):
        # You can update the response to virtualize some sensor in development mode
        return [
            AsyncW1ThermSensor(None, '020f91775390'),
            AsyncW1ThermSensor(None, '071d91527342')
        ]

    async def get_temperature(self, unit=None):
        if self.a:
            self._t -= 0.5
        else:
            self._t += 0.5

        if self._t > 60:
            self.a = True
        if self._t < 52:
            self.a = False

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


class W1ThermSensorError(Exception):
    def __init__(self):
        pass


Unit = Default()
Sensor = Default()
