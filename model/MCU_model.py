from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from model.Serial_model import SerialCtrl

class MCU_model():
    def __init__(self, mcu_serial : 'SerialCtrl'):
        self.mcu_serial = mcu_serial