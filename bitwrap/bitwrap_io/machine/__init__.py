"""
load xml definitions as a bitwrap machine
"""
from bitwrap_io.machine.ptnet import PTNet

class Machine(object):
    """ Use a petri-net as a state machine """

    def __init__(self, name):
        self.name = name
        self.net = PTNet(name)
        self.machine = self.net.to_machine()
