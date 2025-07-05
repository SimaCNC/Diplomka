from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from model.Serial_model import SerialCtrl

class Piezo_model():
    def __init__(self, piezo_serial : 'SerialCtrl'):
        self.piezo_serial = piezo_serial
        pass


    def index_pozice(self):
        msg = "IN x y z;\n"
        self.piezo_serial.send_msg_simple(msg)

    