

class Temp:
    def __init__(self, sensor_id: str):
        self._sensor_id: str = sensor_id
        self._temp: float = None

    def refresh(self):
        with open(f'/sys/bus/w1/device/{self._sensor_id}/w1_slave') as file:
            self._temp = float(file.read().split("\n")[1].split(" ")[9][2:]) / 1000
