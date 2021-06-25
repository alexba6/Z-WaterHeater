from typing import List
from RPi import GPIO
import random
import string

from Z_WH.tools.meta import MetaData


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
        self.groupId: str = groupId
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
                'id': group.groupId,
                'outputsId': [output.id for output in group.outputs],
                'name': group.name
            } for group in self._groups
        ]

    # Get group with his id
    def getGroup(self, groupId: int) -> Group or None:
        for group in self._groups:
            if group.groupId == groupId:
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
            if self._groups[i].groupId == groupId:
                self._groups.pop(i)
                self.saveGroupMeta()
                return
        raise GroupManagerError('Group not found !')

    # Add group
    def _addGroup(self, outputs: List[Output], name: str):
        self._groups.append(Group(
            ''.join(map(
                lambda i: random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits),
                range(8)
            )),
            outputs,
            name
        ))

    # Add group with output id
    def addGroup(self, outputsId: List[str], name: str):
        self._checkOutputId(outputsId)
        self._addGroup(
            [self.getOutput(outputId) for outputId in outputsId],
            name
        )
        self.saveGroupMeta()

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


groupManager = GroupManager([
    Output(20, 'out 1'),
    Output(21, 'out 2')
])
