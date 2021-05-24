from ..tools.meta import MetaData
from ..config import APP_ENV, PROD, DEBUG

if APP_ENV == PROD:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)


class Output:
    def __init__(self, pin, name):
        self.pin = pin
        self.name = name
        self.__state = None
        if APP_ENV == PROD:
            GPIO.setup(self.pin, GPIO.OUT)

        self.state = False

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, state):
        if type(state) != bool:
            raise Exception('State must be a boolean')
        if self.__state != state:
            print(f"Relay {self.pin} is {state}")
            if APP_ENV == PROD:
                if state:
                    GPIO.output(self.pin, GPIO.LOW)
                else:
                    GPIO.output(self.pin, GPIO.HIGH)
            self.__state = state


class Group:
    def __init__(self, name, outputs):
        for out_instance in outputs:
            if not isinstance(out_instance, Output):
                raise Exception('Output must be an instance of Output !')
        self.__name = name
        self.state = False
        self.outputs = outputs

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if len(value) > 15:
            raise Exception('Max length of a group name is 15 !')
        self.__name = value


class GroupManager:
    def __init__(self):
        self.groups = []
        self.outputs = [Output(16, 'out_1'), Output(18, 'out_2')]
        self.meta = MetaData('group_manager')
        data = self.meta.data
        if data:
            try:
                for group_name in data:
                    self.group_add(
                        group_name,
                        data[group_name]['outputs_name']
                    )
            except Exception as error:
                if DEBUG:
                    print(error)

    # Check if the group exist
    def exist_groups(self, name):
        for group_instance in self.groups:
            if group_instance.name == name:
                return True
        return False

    # Get a group instance from his name
    def get_group_from_name(self, name):
        for group_instance in self.groups:
            if group_instance.name == name:
                return group_instance

    # Get an output instance from his name
    def get_output_from_name(self, name):
        for out_instance in self.outputs:
            if out_instance.name == name:
                return out_instance
        return None

    # Save the current group config into the matadata
    def save_meta(self):
        data = {}
        for group_instance in self.groups:
            data[group_instance.name] = {
                'outputs_name': [out_instance.name for out_instance in group_instance.outputs]
            }
        self.meta.data = data

    # Add a new group
    def group_add(self, name, outputs_name):
        if self.get_group_from_name(name):
            raise Exception('There is already an other group with this name !')
        self.groups.append(Group(name, [self.get_output_from_name(output_name) for output_name in outputs_name]))
        self.save_meta()

    # Del a group
    def group_del(self, name):
        group = self.get_group_from_name(name)
        if not group:
            raise Exception('Group does not exist !')

        for i in range(len(self.groups)):
            if self.groups[i].name == name:
                print(i)
                self.groups.pop(i)
        self.save_meta()

    # Update name or outputs of a group
    def group_update(self, old_name, **kwargs):
        group = self.get_group_from_name(old_name)
        if not group:
            raise Exception('Group does not exist !')

        new_name = kwargs.get('new_name')
        outputs_name = kwargs.get('outputs_name')

        if new_name:
            if self.get_group_from_name(new_name):
                raise Exception('There is already an other group with this name !')
            group.name = new_name

        if outputs_name:
            group.outputs = [self.get_output_from_name(output_name) for output_name in outputs_name]

        self.save_meta()

    # Switch the state off a group
    def switch_group(self, name, state):
        for group_instance in self.groups:
            if group_instance.name == name:
                group_instance.state = state
                for out_instance in self.outputs:
                    if out_instance in group_instance.outputs:
                        out_instance.state = state
                    else:
                        out_instance.state = not state
            else:
                group_instance.state = False

    # Get the information about all the groups
    def groups_info(self):
        return [{
            'name': group_instance.name,
            'outputs_name': [out_instance.name for out_instance in group_instance.outputs],
            'state': group_instance.state
        } for group_instance in self.groups]


group_manager = GroupManager()

def start():
    if len(group_manager.groups_info()) == 0:
        for available_out in group_manager.outputs:
            group_manager.group_add(available_out.name.upper(), [available_out.name])
