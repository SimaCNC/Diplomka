from MCU_model import MCUcontroller
from Piezo_model import PiezoPohony


class Model:
    def __init__(self):
        self.mcu = MCUcontroller()
        self.piezo = PiezoPohony()
        