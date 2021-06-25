# Z-WaterHeater

## Overview
**Z-WaterHeater** is a home automation for water heater.


## Hardware

You need a raspberry-pi and these devices:
+ DS18B20 temperature sensor on one-wire bus *( 5 max )*
+ Oled I2C display *( 128px x 32px )*
+ Relay board

You can change the `output.py` file for the relay GPIO :

```python
groupManager = GroupManager([
    Output(20, 'out 1') # Output (GPIO pin, output id)
])
```

## Softwares

**Python** <br>
It's required to have python 3.8 or more  installed on your system.
[Download Python](https://www.python.org/downloads/)

### Installation

Fist set the environment variables in `.env` file :
```ini
# Env mode
APP_ENV = <app env mode>
DEBUG = <run in debug>

# API
API_PORT = <api port>
API_HOST = <api host>

# JWT
JWT_KEY = <json web token key>
```

Then run the app with :

```sh 
python3 main.py
```

### Production

Before run the app on the raspberry-pi, you have to delete `RPi.py` and `w1thermsensor.py`use for the development.
You need also to turn the environment `APP_ENV` in production mode.

*Made by [Alexis Baylet](https://github.com/Alexis-ba6)*