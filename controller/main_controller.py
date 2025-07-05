from tkinter import *
from tkinter import messagebox
import threading

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from view.main_view import RootGUI, ComGUI
    from model.Piezo_model import Piezo_model
    from model.MCU_model import MCU_model
    from view.main_view import PiezoGUI
    import tkinter as Tk
    
class MainController():
    
    def __init__(self, root : 'Tk', com : 'ComGUI', piezo_model : 'Piezo_model', mcu_model : 'MCU_model'):
        self.root = root
        self.com = com
        self.piezo_model = piezo_model
        self.mcu_model = mcu_model
        
#----OVLADANI INIT
    def M_init_view_data(self):
        pass
#----OVLADANI INIT   
        
#CONTROLLER PIEZO A MCU PRIPOJENI K COM SERIOVA KOMUNIKACE, trida ComGui() 36  
    def M_serial_connect_piezo(self):
        if self.com.btn_connect_piezo["text"] in "Připojit" :
            #Zacatek seriove komunikace - pripojeni metodou SerialOpen
            self.piezo_model.piezo_serial.SerialOpen(self.com.vybrany_com_piezo.get(), int(self.com.vybrany_bd_piezo.get()))
            
            #jestli je pripojeni uspesne:
            if self.piezo_model.piezo_serial.status:
                self.com.btn_connect_piezo["text"] = "Odpojit"
                self.com.btn_refresh_piezo["state"] = "disable"
                self.com.drop_bd_piezo["state"] = "disable"
                self.com.drop_com_piezo["state"] = "disable"
                InfoMsg = f"Piezo\nÚspěšně připojeno pomocí sériové komunikace k {self.com.vybrany_com_piezo.get()}"
                messagebox.showinfo("Piezo info", InfoMsg)
                
                #Vytvoreni PiezoGUI:
                from view.main_view import PiezoGUI
                self.piezo_gui = PiezoGUI(self.root, self, self.piezo_model)
                
            else:
                ErrorMsg = f"Piezo\nChyba v připojení pomocí sériové komunikace k {self.com.vybrany_com_piezo.get()}"
                messagebox.showerror("Piezo CHYBA", ErrorMsg)
        
        else:
            self.piezo_model.piezo_serial.SerialClose()
            self.piezo_gui.PiezoGUIClose()
            InfoMsg = f"Piezo\nÚspěšně odpojeno pomocí sériové komunikace k {self.com.vybrany_com_piezo.get()}"
            messagebox.showinfo("Piezo info", InfoMsg)  
            self.com.btn_connect_piezo["text"] = "Připojit"
            self.com.btn_refresh_piezo["state"] = "active"
            self.com.drop_bd_piezo["state"] = "active"
            self.com.drop_com_piezo["state"] = "active"
                
    def M_serial_connect_MCU(self):
        if self.com.btn_connect_MCU["text"] in "Připojit" :
            #Zacatek seriove komunikace - pripojeni metodou SerialOpen
            self.mcu_model.mcu_serial.SerialOpen(self.com.vybrany_com_MCU.get(), int(self.com.vybrany_bd_MCU.get()))
            
            #jestli je pripojeni uspesne:
            if self.mcu_model.mcu_serial.status:
                self.com.btn_connect_MCU["text"] = "Odpojit"
                self.com.btn_refresh_MCU["state"] = "disable"
                self.com.drop_bd_MCU["state"] = "disable"
                self.com.drop_com_MCU["state"] = "disable"
                InfoMsg = f"MCU\nÚspěšně připojeno pomocí sériové komunikace k {self.com.vybrany_com_MCU.get()}"
                messagebox.showinfo("MCU info", InfoMsg)
                
            else:
                ErrorMsg = f"MCU\nChyba v připojení pomocí sériové komunikace k {self.com.vybrany_com_MCU.get()}"
                messagebox.showerror("MCU CHYBA", ErrorMsg)
        
        else:
            self.mcu_model.mcu_serial.SerialClose()
            InfoMsg = f"MCU\nÚspěšně odpojeno pomocí sériové komunikace k {self.com.vybrany_com_MCU.get()}"
            messagebox.showinfo("MCU info", InfoMsg)  
            self.com.btn_connect_MCU["text"] = "Připojit"
            self.com.btn_refresh_MCU["state"] = "active"
            self.com.drop_bd_MCU["state"] = "active"
            self.com.drop_com_MCU["state"] = "active"
            
#CONTROLLER PIEZO A MCU PRIPOJENI K COM SERIOVA KOMUNIKACE, trida ComGui()   


#CONTROLLER PIEZO OVLADANI, trida PiezoGUI() 151
    #obas je pouziti slov/promennych home a index matouci - jedna se o totez jsou to synonyma
    def M_C_Index(self):
        print("VOLANI HOME")
        self.piezo_model.index_pozice()
        send = "RI x y z\n"
        expect = "$RI x1 y1 z1" 
        self.piezo_model.t1 = threading.Thread(target=self.piezo_model.piezo_serial.get_msg_stream, args=(send, expect, self.M_C_Index_done,), daemon=True)
        self.piezo_model.t1.start()
        
    def M_C_Index_done(self, msg):
        print(f"zprava z piezo: {msg}")
        if msg == "$RI x1 y1 z1":
            # self.piezo_gui.publish_PiezoGUI_home_done()
            self.root.after(0, self.piezo_gui.publish_PiezoGUI_home_done)
        else:
            print("Neuspesne")
        #POSLAT PRES SERIAL POZADAVEK O ZASLANI NA HOME POZICI!
    
    def M_C_Reference(self):
        pass




#CONTROLLER PIEZO OVLADANI