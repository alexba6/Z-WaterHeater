from typing import List
from RPi import GPIO
from ..tools.meta import MetaData
from ..config import DEBUG
from ..tools.random_key import generate_key

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


# Manager a single output
class Output:
    def __init__(self, pin: int, name: str):
        self.pin = pin
        self.name = name
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


# Manage outputs with group
class Group:
    def __init__(self, group_id: str, group_name: str, outputs: List[Output]):
        self.id: str = group_id
        self.__name: str = group_name
        self.state: bool = False
        self.outputs: List[Output] = outputs

    # Get the name of the group
    @property
    def name(self) -> str:
        return self.__name

    # Change the name of the group
    @name.setter
    def name(self, value: str):
        if len(value) > 15:
            raise Exception('Max length of a group name is 15 !')
        self.__name = value


# Manage all the groups
class GroupManager:
    def __init__(self, outputs: List[Output]):
        self.groups: List[Group] = []
        self.outputs: List[Output] = outputs
        self.meta = MetaData('group_manager')

        groups_meta = self.meta.data
        if groups_meta:
            try:
                for group in groups_meta:
                    self.group_load(
                        group['id'],
                        group['name'],
                        group['outputs_name']
                    )
            except Exception as error:
                if DEBUG:
                    print(error)

    # Load a new group instance in the buffer
    def group_load(self, group_id: str, name: str, outputs_name: List[str]):
        self.groups.append(
            Group(
                group_id,
                name,
                [self.get_output_from_name(output_name) for output_name in outputs_name]
            )
        )

    # Add a new group
    def group_add(self, name: str, outputs_name: List[str]):
        if self.get_group_by('name', name):
            Exception('There is already an other group with this name !')
        while True:
            random_id = generate_key(5)
            if not self.get_group_by('id', random_id):
                break
        self.group_load(random_id, name, outputs_name)
        self.save_meta()

    # Update name or outputs of a group
    def group_update(self, group: Group, **kwargs):
        new_name = kwargs.get('name')
        outputs_name = kwargs.get('outputs_name')

        self.check_output_name(outputs_name)

        if new_name:
            if self.get_group_by('name', new_name):
                raise Exception('There is already an other group with this name !')
            group.name = new_name

        if outputs_name:
            group.outputs = [self.get_output_from_name(output_name) for output_name in outputs_name]

        self.save_meta()

    # Del a group
    def group_del(self, group_id: str):
        group = self.get_group_by('id', group_id)
        if not group:
            raise Exception('Group does not exist !')

        for i in range(len(self.groups)):
            if self.groups[i].id == group_id:
                self.groups.pop(i)
                break
        self.save_meta()

    # Get the information about all the groups
    def groups_info(self):
        return [{
            'id': group_instance.id,
            'name': group_instance.name,
            'outputs_name': [out_instance.name for out_instance in group_instance.outputs],
            'state': group_instance.state
        } for group_instance in self.groups]

    # Find a group with a tag
    def get_group_by(self, tag: str, value: str):
        for group_instance in self.groups:
            if tag == 'name':
                if group_instance.name == value:
                    return group_instance
            elif tag == 'id':
                if group_instance.id == value:
                    return group_instance
        return None

    # Get an output instance from his name
    def get_output_from_name(self, name: str):
        for out_instance in self.outputs:
            if out_instance.name == name:
                return out_instance
        return None

    # Create default group
    def create_default_groups(self):
        self.groups = [
            Group(output.name, output.name.upper(), [output])
            for output in self.outputs
        ]
        self.save_meta()

    # Save the current group config into the mata data
    def save_meta(self):
        self.meta.data = [
            {
                'id': group_instance.id,
                'name': group_instance.name,
                'outputs_name': [outputs_instance.name for outputs_instance in group_instance.outputs]
            }
            for group_instance in self.groups
        ]

    # Check if the output name exist
    def check_output_name(self, outputs_name: List[str]):
        valid_outputs_name = [output.name for output in self.outputs]
        for output_name in outputs_name:
            if output_name not in valid_outputs_name:
                raise Exception('Invalid output name !')

    # Switch the state off a group
    def switch_group(self, group: Group, state: bool):
        for group_instance in self.groups:
            if group_instance.id == group.id:
                group_instance.state = state
                for out_instance in self.outputs:
                    if out_instance in group_instance.outputs:
                        out_instance.state = state
                    else:
                        out_instance.state = not state
            else:
                group_instance.state = False


group_manager = GroupManager([
    Output(16, 'out_1'),
    Output(18, 'out_2')
])


# Create default group if does not exists
def start():
    if len(group_manager.groups_info()) == 0:
        group_manager.create_default_groups()
