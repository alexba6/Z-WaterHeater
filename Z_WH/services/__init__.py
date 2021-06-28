from Z_WH.config.output import AVAILABLE_OUTPUTS

from .autoTimeSlot import AutoTimeSlotManager
from .displaymanager import DisplayManager
from .output import GroupManager, OutputManager, Output
from .tempSensor import TempSensorManager
from .tempSaver import TempSaverManager
from .verificationCodeManager import VerificationCodeManager
from .mail import MailManager
from .notification import NotificationManager
from .user import UserManager
from .tempLimit import TempLimitManager


mailManager = MailManager()
notificationManager = NotificationManager(mailManager)

userManager = UserManager(notificationManager)

displayManager = DisplayManager()

tempSensorManager = TempSensorManager(notificationManager)
tempSaverManager = TempSaverManager(tempSensorManager)

tempLimitManager = TempLimitManager(tempSensorManager)

autoTimeSlotManager = AutoTimeSlotManager()

verificationCodeManager = VerificationCodeManager(displayManager)

groupManager = GroupManager([Output(*availableOutput) for availableOutput in AVAILABLE_OUTPUTS])

outputManager = OutputManager(groupManager, displayManager, autoTimeSlotManager, tempLimitManager)


def initAllServices():
    mailManager.init()
    notificationManager.init()

    userManager.init()

    displayManager.init()

    tempSensorManager.init()
    tempSaverManager.init()

    tempLimitManager.init()

    autoTimeSlotManager.init()

    groupManager.init()
    outputManager.init()
