from typing import List
from sqlalchemy import Column, Integer, String
import json
from .base_entity import BaseEntity


class OutputGroup(BaseEntity):
    __tablename__ = 'output_group'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    outputs_id = Column(String)

    @property
    def output(self) -> List[str]:
        return json.loads(self.outputs_id)

    @output.setter
    def output(self, outputs):
        for output in outputs:
            if output not in ['out 1', 'out 2']:
                raise Exception('INVALID_OUTPUTS')
        self.outputs_id = json.dumps(outputs)
