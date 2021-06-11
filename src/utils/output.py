import sqlalchemy
from typing import List
from RPi import GPIO
from src.config.database import Session
from src.models.OutputGroup import OutputGroup


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


# Manager a single output
class Output:
    def __init__(self, pin: int, out_id: str):
        self.pin = pin
        self.id = out_id
        self.__state = None
        self.init()
        self.state = False

    # Init the output on the board
    def init(self) -> None:
        GPIO.setup(self.pin, GPIO.OUT)

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
        self._current_group_id_on: str = None

    # Init the default groups if the database is empty
    def init(self):
        if len(self._groups) == 0:
            with Session() as session:
                for output in self._outputs:
                    group = OutputGroup()
                    group.name = output.id
                    group.output = [output.id]
                    session.add(group)
                session.commit()

    # Load the group from the database
    def load(self):
        with Session() as session:
            self._groups = session.query(OutputGroup).all()

    # Find a group with his id
    def _findGroup(self, group_id: int) -> OutputGroup:
        for group in self._groups:
            if group.id == group_id:
                return group
        raise Exception('Cannot find the group !')

    # Find an output with her id
    def _findOutput(self, output_id) -> Output:
        for output in self._outputs:
            if output.id == output_id:
                return output
        raise Exception('Cannot find the output !')

    # Switch on one of the group
    def switchOn(self, group_id: int):
        if group_id == self._current_group_id_on:
            return
        self._current_group_id_on = group_id
        outputs_id = self._findGroup(group_id).outputs_id
        for output in self._outputs:
            if output.id in outputs_id:
                output.state = True
            else:
                output.state = False

    # Switch off all the groups
    def switchOff(self):
        if self._current_group_id_on is None:
            return
        self._current_group_id_on = None
        for output in self._outputs:
            output.state = False


group_manager = GroupManager([
    Output(16, 'out 1'),
    Output(18, 'out 2')
])
