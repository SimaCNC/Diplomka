from tkinter import *
from tkinter import messagebox
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from view.main_view import ComGUI
    from model.Serial_model import SerialCtrl
    from model.Piezo_model import Piezo_model
    from model.MCU_model import MCU_model
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
        
#CONTROLLER PIEZO A MCU PRIPOJENI K COM SERIOVA KOMUNIKACE, trida ComGui()     
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
                
            else:
                ErrorMsg = f"Piezo\nChyba v připojení pomocí sériové komunikace k {self.com.vybrany_com_piezo.get()}"
                messagebox.showerror("Piezo CHYBA", ErrorMsg)
        
        else:
            self.piezo_model.piezo_serial.SerialClose()
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