from typing import TYPE_CHECKING
import threading

if TYPE_CHECKING:
    from model.Serial_model import SerialCtrl

class MCU_model():
    def __init__(self, mcu_serial : 'SerialCtrl'):
        self.mcu_serial = mcu_serial 
        
        self.posledni_odpoved_MCU = None
        self.teplota_okoli = None
        self.typ_mereni = {
            "A/D" : "A/D",
            "OSC" : "OSC"
        }        
        
     
    def msg_odpoved(self, callback_fun = None):
        """ odpoved od MCU"""
        
        def msg_odpoved_thread():
            while True:
                try:
                    self.posledni_odpoved_MCU = self.mcu_serial.get_msg_simple()
                    if self.posledni_odpoved_MCU:
                        print(f"[MCU_model]: prichozi zprava {self.posledni_odpoved_MCU}")                      
                    if callback_fun:
                        callback_fun() 
                    break
                except Exception as e:
                    print(f"[MCU_model] chyba pri cteni nebo parsovani dat {e}")  
                    break
        self.t1 = threading.Thread(target=msg_odpoved_thread, daemon=True)
        self.t1.start()
        
        
    def precti_teplotu(self):
        self.mcu_serial.send_msg_simple("#T")
        self.msg_odpoved(self.zapsat_teplotu)
        
    def zapsat_teplotu(self):
        self.teplota_okoli = self.posledni_odpoved_MCU
        
            
        
        