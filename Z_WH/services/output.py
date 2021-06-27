import threading
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from typing import List
from RPi import GPIO
import random
import string

from Z_WH.tools.meta import MetaData
from .auto import AutoTimeSlotManager
from .displaymanager import DisplayManager


ON, OFF, AUTO = 'on', 'off', 'auto'


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
    def getGroup(self, groupId: int) -> Group or None:
        for group in self._groups:
            if group.id == groupId:
                return group
        return None

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
        self.saveGroupMeta()
        return group

    # Update group
    def updateGroup(self, groupId: int, outputsId: List[str] = None, name: str = None):
        group = self.getGroup(groupId)
        if not group:
            raise GroupManagerError('Group not found !')
        if outputsId:
            self._checkOutputId(outputsId)
            group.outputs = [self.getOutput(outputId) for outputId in outputsId]
        if name:
            group.name = name
        self.saveGroupMeta()

    # Get all the group
    def getGroups(self):
        return self._groups

    # Switch on one of the group
    def switchOn(self, groupIp: int):
        group: Group or None = self.getGroup(groupIp)
        if group is None:
            raise GroupManagerError('Invalid group id')

        if groupIp == self._enableGroup:
            return
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
            autoTimeSlotManager: AutoTimeSlotManager
    ):
        self._groupManager = groupManager
        self._displayManager = displayManager
        self._autoTimeSlotManager = autoTimeSlotManager

        self.mode: str = AUTO
        self.enableGroupId: int or None = None

        self._autoCheckTimer = None
        self._autoStartTimer = None

        self._autoStartTime: float = 60*60*12

        self._meta = MetaData('out-manager')

        self._autoThread()

    def init(self):
        self.loadMeta()

        def screenCallBack():
            text = self.mode.upper()
            if self.enableGroupId:
                text += ' : ' + self._groupManager.getGroup(self.enableGroupId).name
            image = Image.new('1', self._displayManager.displaySize)
            draw = ImageDraw.Draw(image)
            ImageFont.load_default()
            font = ImageFont.truetype('Z_WH/assets/font/coolvetica.ttf', 32)
            draw.text((0, 0), text, font=font, fill=255)
            return image

        self._displayManager.addSlide(1.5, screenCallBack)

    # Load the meta data
    def loadMeta(self):
        if self._meta.data:
            autoStartTime = self._meta.data.get('autoStartTime')
            if autoStartTime:
                self._autoStartTime = autoStartTime

    # Save the meta data
    def saveMeta(self):
        self._meta = {
            'autoStartTime': self._autoStartTime
        }

    # Get configuration
    def getConfig(self):
        return {
            'autoStartTime': self._autoStartTime
        }

    # Update the configuration
    def saveConfig(self, **kwargs):
        if kwargs.get('autoStartTime'):
            self._autoStartTime = kwargs['autoStartTime']
        self.saveMeta()

    # Check the output group for the auto mode
    def _autoThread(self):
        self._autoCheckTimer = threading.Timer(1, lambda: self._autoThread())
        self._autoCheckTimer.start()

        groupIp = self._autoTimeSlotManager.groupEnableNow()
        if self.enableGroupId == groupIp:
            return
        if groupIp:
            self._groupManager.switchOn(groupIp)
        else:
            self._groupManager.switchOff()
        self.enableGroupId = groupIp

    # Switch the group
    def switch(self, mode: str, groupId: int = None):
        if mode == self.mode:
            return
        if mode not in [ON, OFF, AUTO]:
            raise OutManagerError('Invalid mode')

        def stopTimer():
            if self._autoCheckTimer and self._autoCheckTimer.is_alive():
                self._autoCheckTimer.cancel()
            if self._autoStartTime and self._autoStartTimer.is_alive():
                self._autoStartTimer.cancel()

        if mode == ON:
            self._groupManager.switchOn(groupId)
            self.enableGroupId = groupId
        if mode == OFF:
            self._groupManager.switchOff()
            self.enableGroupId = None
        if mode == AUTO:
            stopTimer()
            self._autoThread()

        if mode in [ON, OFF]:
            stopTimer()
            self._autoStartTimer = threading.Timer(self._autoStartTime, lambda: self._autoThread())
            self._autoStartTimer.start()

        self.mode = mode
