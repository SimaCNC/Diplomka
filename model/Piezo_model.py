from typing import TYPE_CHECKING
import threading
import re

if TYPE_CHECKING:
    from model.Serial_model import SerialCtrl

class Piezo_model():
    def __init__(self, piezo_serial : 'SerialCtrl'):
        self.piezo_serial = piezo_serial
        
        self.x = None
        self.y = None
        self.z = None
        self.is_homed = None

    

    def index_pozice(self):
        msg = "IN x y z;\n"
        self.piezo_serial.send_msg_simple(msg)

    def precti_polohu(self, callback_fun):
        """precte pozadavek na pozici, zpracuje a zavola callback"""
        msg = "RP x y z\n"
        def precti_polohu_thread():
            self.piezo_serial.send_msg_simple(msg)
            while True:
                try:
                    raw = self.piezo_serial.ser.readline().decode(errors='ignore').strip()
                    if raw:
                        print(f"[precti polohu] prijakot: {raw}")
                        if raw.startswith("$RP"):
                            match = re.search(r"\$RP x([-\d.]+) y([-\d.]+) z([-\d.]+)", raw)
                            if match:
                                self.x = round(float(match.group(1)), 2)
                                self.y = round(float(match.group(2)), 2)
                                self.z = round(float(match.group(3)), 2)
                                if callback_fun:
                                    callback_fun()
                            else:
                                print("[precti polohu] format prijateho retezce neodpovida ocekavenemu")
                            break
                except Exception as e:
                    print(f"[precti polohu] chyba pri cteni nebo parsovani dat {e}")  
                    break         
        self.t1 = threading.Thread(target=precti_polohu_thread, daemon=True)
        self.t1.start()