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
        
        self.x_old = 0
        self.y_old = 0
        self.z_old = 0

        self.x_ref = 0
        self.y_ref = 0
        self.z_ref = 0
        
        self.posledni_odpoved_piezopohony = None
    
        self.t1 = None
        self.t2 = None
        self.t3 = None

    def index_pozice(self):
        msg = "IN x y z;\n"
        self.piezo_serial.send_msg_simple(msg) 

    def precti_polohu_stojici(self, callback_fun):
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
                                self.x = round(float(match.group(1)), 3)
                                self.y = round(float(match.group(2)), 3)
                                self.z = round(float(match.group(3)), 3)
                                
                                # Vypocet relativni polohy
                                self.x_ref = round(self.x - self.x_old, 3)
                                self.y_ref = round(self.y - self.y_old, 3)
                                self.z_ref = round(self.z - self.z_old, 3)
                            
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
        
    def nastav_referenci(self):
        self.x_ref = 0.0
        self.y_ref = 0.0
        self.z_ref = 0.0
        
        if self.x is not None:
            self.x_old = self.x
        if self.y is not None:
            self.y_old = self.y
        if self.z is not None:
            self.z_old = self.z
    
    def msg_odpoved(self, callback_fun = None):
        """odpoved od piezopohonu"""
        
        def msg_odpoved_thread():
            while True:
                try:
                    self.posledni_odpoved_piezopohony = self.piezo_serial.get_msg_simple()
                    if self.posledni_odpoved_piezopohony:
                        print(f"[odpoved]: prichozi zprava {self.posledni_odpoved_piezopohony}")                        
                        if callback_fun:
                            callback_fun()
                    break
                except Exception as e:
                    print(f"[precti polohu] chyba pri cteni nebo parsovani dat {e}")  
                    break                
        
        self.t1 = threading.Thread(target=msg_odpoved_thread, daemon=True)
        self.t1.start()
    