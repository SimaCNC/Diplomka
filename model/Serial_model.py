import serial.tools.list_ports

class SerialCtrl():
    
    def __init__(self):
        self.com_list = []
        self.sync_cnt = 200
        self.ser = None
        self.status = False
        
    #METODA PRO VYPSANI AKTUALNICH DOSTUPNYCH COM PORTU
    def getCOMlist(self):
        ports = serial.tools.list_ports.comports()
        self.com_list = [com[0] for com in ports]
        self.com_list.insert(0, "-")
        
    #METODA PRO OTEVRENI SERIOVEHO PORTU SE ZVOLENYM BAUDEM A PORTEM
    def SerialOpen(self, port, baud):
        try:
            if self.ser is None or not self.ser.is_open:
                self.ser = serial.Serial(port=port, baudrate=baud, timeout=0.1)
                self.status = True
                print(f"Port {port} byl otevren s baudratem {baud}")
                
            else:
                print(f"Port {port} byl jiz drive otevren")
                self.status = True
                
        except Exception as e:
            print(f"Chyba pri otevirani portu {port}: {e}")
            self.status = False
                   
    
    #METODA PRO ZAVRENI ZVOLENEHO SERIOVEHO PORTU
    def SerialClose(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            self.status = False
            print(f"Port {self.ser.port} byl uzavren")
        else:
            print(f"Port nebyl otevren, nelze zavrit")
            
            
    # METODY PRO POSILANI - PIEZO
    def send_msg_simple(self, msg : str):
        print(msg)
        self.ser.write(msg.encode())
        
            
            
            
                   