import threading
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from typing import List
from RPi import GPIO
import random
import string

from Z_WH.tools.meta import MetaData
from .displaymanager import DisplayManager, Slide, DISPLAY_SIZE
from .autoTimeSlot import AutoTimeSlotManager
from .tempLimit import TempLimitManager
from Z_WH.tools.log import Logger

ON, OFF, AUTO = 'on', 'off', 'auto'

outputLogger = Logger('output')
groupLogger = Logger('output')


class GroupManagerError(Exception):
    def __init__(self, message: str):
        self.message = message


# Manager a single output
class Output:
    def __init__(self, pin: int, out_id: str):
        self.pin = pin
        self.id = out_id
        self.__state = None

    # Init the output on the board
    def init(self) -> None:
        GPIO.setup(self.pin, GPIO.OUT)
        self.state = False

    # Get the current output state
    @property
    def state(self) -> bool:
        return self.__state

    # Change the output state
    @state.setter
    def state(self, state: bool) -> None:
        if self.__state != state:
            outputLogger.info(f"Relay {self.pin} is {state}")
            print(f"> Relay {self.pin} is {state}")
            GPIO.setup(self.pin, GPIO.LOW if state else GPIO.HIGH)
            self.__state = state


class Group:
    def __init__(self, groupId: str, outputs: List[Output], name: str):
        self.id: str = groupId
        self.outputs: List[Output] = outputs
        self.name = name


class GroupManager:
    def __init__(self, outputs: List[Output]):
        self._outputs = outputs
        self._groups: List[Group] = []
        self._enableGroup: str or None = None

        self._metaGroups = MetaData('output-groups')

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        for outputs in self._outputs:
            outputs.init()

    # Load the group from the database
    def init(self):
        self.loadGroupMeta()

    # Load the group meta data
    def loadGroupMeta(self):
        groupsMeta = self._metaGroups.data
        if groupsMeta:
            for groupMeta in groupsMeta:
                self._groups.append(Group(
                    groupMeta.get('id'),
                    [self.getOutput(outputId) for outputId in groupMeta.get('outputsId')],
                    groupMeta.get('name')
                ))
        else:
            for output in self._outputs:
                self._addGroup([output], f"G - {output.id.upper()}")
            self.saveGroupMeta()

    # Save the groups meta data
    def saveGroupMeta(self):
        self._metaGroups.data = [
            {
                'id': group.id,
                'outputsId': [output.id for output in group.outputs],
                'name': group.name
            } for group in self._groups
        ]

    # Get group with his id
    def getGroup(self, groupId: str) -> Group:
        for group in self._groups:
            if group.id == groupId:
                return group
        raise GroupManagerError('Invalid group id')

    # Get output with her id
    def getOutput(self, outputId) -> Output or None:
        for output in self._outputs:
            if output.id == outputId:
                return output
        return None

    # Check if the output id are allowed
    def _checkOutputId(self, outputsId: List[str]):
        for outputId in outputsId:
            if outputId not in [output.id for output in self._outputs]:
                raise GroupManagerError('Output id not found !')

    # Delete group
    def deleteGroup(self, groupId: int):
        for i in range(len(self._groups)):
            if self._groups[i].id == groupId:
                groupLogger.info(f"Group {groupId} deleted")
                self._groups.pop(i)
                self.saveGroupMeta()
                return
        raise GroupManagerError('Group not found !')

    # Add group
    def _addGroup(self, outputs: List[Output], name: str) -> Group:
        group = Group(
            ''.join(map(
                lambda i: random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits),
                range(8)
            )),
            outputs,
            name
        )
        self._groups.append(group)
        return group

    # Add group with output id
    def addGroup(self, outputsId: List[str], name: str) -> Group:
        self._checkOutputId(outputsId)
        group = self._addGroup(
            [self.getOutput(outputId) for outputId in outputsId],
            name
        )
        groupLogger.info(f"Group {group.id} added")
        self.saveGroupMeta()
        return group

    # Update group
    def updateGroup(self, groupId: str, outputsId: List[str] = None, name: str = None):
        group = self.getGroup(groupId)
        if outputsId:
            self._checkOutputId(outputsId)
            group.outputs = [self.getOutput(outputId) for outputId in outputsId]
        if name:
            group.name = name
        groupLogger.info(f"Group {group.id} updated")
        self.saveGroupMeta()

    # Get all the group
    def getGroups(self):
        return self._groups

    # Switch on one of the group
    def switchOn(self, groupIp: str):
        if groupIp == self._enableGroup:
            return
        group: Group or None = self.getGroup(groupIp)
        self._enableGroup = groupIp

        for output in self._outputs:
            output.state = output in group.outputs

    # Switch off all the groups
    def switchOff(self):
        if self._enableGroup is None:
            return
        self._enableGroup = None
        for output in self._outputs:
            output.state = False


class OutManagerError(Exception):
    def __init__(self, message: str):
        self.message = message


class OutputManager:
    def __init__(
            self,
            groupManager: GroupManager,
            displayManager: DisplayManager,
            autoTimeSlotManager: AutoTimeSlotManager,
            tempLimitManager: TempLimitManager
    ):
        self._groupManager = groupManager
        self._displayManager = displayManager
        self._autoTimeSlotManager = autoTimeSlotManager
        self._tempLimitManager = tempLimitManager

        self.mode: str = AUTO
        self._enableGroupId: str or None = None

        self._startTimer = None

        self.autoStartTime: float = 60 * 60 * 12

        self._meta = MetaData('out-manager')

        self._slide: Slide = Slide(duration=1.5)
        self._slide.newId()

    def init(self):
        self.loadMeta()
        self._tempLimitManager.changeStateCallback = lambda state: self._onLimitStateChangeCallback()
        self._checkTimeSlotThread()
        self._displayManager.addSlide(self._slide)

    def _reloadScreen(self):
        text = 'Off'
        if self._enableGroupId:
            text = self._groupManager.getGroup(self._enableGroupId).name
        image = Image.new('1', DISPLAY_SIZE)
        draw = ImageDraw.Draw(image)
        ImageFont.load_default()
        draw.text(
            ((DISPLAY_SIZE[0] / 2) - ((len(text) * 9) / 2), 3),
            text,
            font=ImageFont.truetype('Z_WH/assets/font/coolvetica.ttf', 20),
            fill=255
        )
        self._slide.image = image

    # Load the meta data
    def loadMeta(self):
        if self._meta.data:
            autoStartTime = self._meta.data.get('autoStartTime')
            if autoStartTime:
                self.autoStartTime = autoStartTime

    # Save the meta data
    def saveMeta(self):
        self._meta = {
            'autoStartTime': self.autoStartTime
        }

    # Get configuration
    def getConfig(self):
        return {
            'autoStartTime': self.autoStartTime
        }

    # Update the configuration
    def saveConfig(self, **kwargs):
        if kwargs.get('autoStartTime'):
            self.autoStartTime = kwargs['autoStartTime']
        self.saveMeta()

    def _onLimitStateChangeCallback(self):
        self.enableGroupId(self._enableGroupId)

    def enableGroupId(self, groupId: str or None):
        self._reloadScreen()
        if groupId is None or not self._tempLimitManager.isEnable:
            self._groupManager.switchOff()
        else:
            self._groupManager.switchOn(groupId)
        self._enableGroupId = groupId

    # Check the output group for the auto mode
    def _checkTimeSlotThread(self):
        threading. \
            Timer(1, lambda: self._checkTimeSlotThread()). \
            start()

        if self.mode != AUTO:
            return
        try:
            self.enableGroupId(self._autoTimeSlotManager.groupEnableNow())
        except GroupManagerError:
            self.enableGroupId(None)

    def _enableAutoStartTimer(self):
        if self._startTimer and self._startTimer.is_alive():
            self._startTimer.cancel()

        def callback():
            self.mode = AUTO
        self._startTimer = threading.Timer(self.autoStartTime, callback)
        self._startTimer.start()

    def switchON(self, groupId: str):
        self.enableGroupId(groupId)
        self._enableAutoStartTimer()
        self.mode = ON

    def switchOFF(self):
        self._groupManager.switchOff()
        self.enableGroupId(None)
        self._enableAutoStartTimer()
        self.mode = OFF

    def switchAUTO(self):
        if self._startTimer and self._startTimer.is_alive():
            self._startTimer.cancel()
        self.mode = AUTO
