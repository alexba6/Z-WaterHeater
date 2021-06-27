from Z_WH.config.output import AVAILABLE_OUTPUTS

from .auto import AutoTimeSlotManager
from .displaymanager import DisplayManager
from .output import GroupManager, OutputManager, Output
from .tempSensor import TempSensorManager
from .tempSaver import TempSaverManager
from .verificationCodeManager import VerificationCodeManager


displayManager = DisplayManager()

tempSensorManager = TempSensorManager()
tempSaverManager = TempSaverManager(tempSensorManager)

autoTimeSlotManager = AutoTimeSlotManager()

verificationCodeManager = VerificationCodeManager(displayManager)

groupManager = GroupManager([Output(*availableOutput) for availableOutput in AVAILABLE_OUTPUTS])
outputManager = OutputManager(groupManager, displayManager, autoTimeSlotManager)


def initAllServices():
    displayManager.init()

    tempSensorManager.init()
    tempSaverManager.init()

    autoTimeSlotManager.init()

    groupManager.init()
    outputManager.init()
