from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from model.Serial_model import SerialCtrl

class Piezo_model():
    def __init__(self, piezo_serial : 'SerialCtrl'):
        self.piezo_serial = piezo_serial
        pass



