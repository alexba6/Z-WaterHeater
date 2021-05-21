

class Display:
    def __init__(self):
        self.power = 0
        print("Display init")

    def start(self):
        print('Display started !')

    def set_power(self, power):
        self.power = power

    def display_code(self, code):
        print(f"Code is : {code}")
