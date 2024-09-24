from opentrons import robot, instruments, containers

class Tool:
    def __init__(self,type: str,*args, **kwargs):
        self.type = type.lower()
        if self.type == "pipette":
            self.instrument = instruments.Pipette(*args, **kwargs)

class Machine:
    def __init__(self):
        self.tools = {'a': None, 'b': None}
    def add_tool(self, type, *args, **kwargs):
        self.tools[kwargs['axis']] = Tool(type, *args, **kwargs)


