from .state_interface import StateInterface


class ClosedState(StateInterface):
    def __init__(self, hardware):
        self.hardware = hardware

    def handle(self):
        self.hardware.close_gate()
        self.hardware.red_on()
