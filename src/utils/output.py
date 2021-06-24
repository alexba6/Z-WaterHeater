from typing import List
from RPi import GPIO
from src.config.database import Session
from src.models.OutputGroup import OutputGroup


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


class GroupManager:
    def __init__(self, outputs: List[Output]):
        self._outputs = outputs
        self._groups: List[OutputGroup] = []
        self._enableGroup: str or None = None

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        for outputs in self._outputs:
            outputs.init()

    # Load the group from the database
    def init(self):
        with Session() as session:
            self._groups: List[OutputGroup] = session.query(OutputGroup).all()
        if len(self._groups) == 0:
            with Session() as session:
                for output in self._outputs:
                    group = OutputGroup()
                    group.name = f'G-{output.id}'
                    group.output = [output.id]
                    self._groups.append(group)
                    session.add(group)
                session.commit()

    # Get group with his id
    def getGroup(self, groupId: int) -> OutputGroup or None:
        for group in self._groups:
            if group.id == groupId:
                return group
        return None

    # Get output with her id
    def getOutput(self, output_id) -> Output or None:
        for output in self._outputs:
            if output.id == output_id:
                return output
        return None

    # Switch on one of the group
    def switchOn(self, groupIp: int):
        group: OutputGroup or None = self.getGroup(groupIp)
        if group is None:
            raise GroupManagerError('Invalid group id')

        if groupIp == self._enableGroup:
            return
        self._enableGroup = groupIp

        outputsId = group.outputs_id
        for output in self._outputs:
            output.state = output.id in outputsId

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
